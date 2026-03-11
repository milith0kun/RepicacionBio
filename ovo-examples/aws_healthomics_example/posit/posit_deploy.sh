#!/bin/bash

set -euxo pipefail

if [ -z "$POSIT_APP_ID" ]; then
  echo "Please set POSIT_APP_ID to the Posit app ID that you want to deploy"
  exit 2
fi

if [ -z "$POSIT_API_KEY" ]; then
  echo "Please set POSIT_API_KEY to key generated on Posit"
  exit 2
fi
  
if [ -z "$POSIT_SERVER" ]; then
  echo "Please set POSIT_SERVER to the full server url (without trailing slash)"
  exit 2
fi

if [ -z "$OVO_CONFIG_DIR" ]; then
  echo "Please set OVO_CONFIG_DIR to be used in Posit"
  exit 2
fi


export OVO_MODULE_PATH=./ovo/
export EXTRA_REQUIREMENTS_PATH=./posit/extra_requirements.txt

make_bundle () {
  rm -rf bundle
  # copy ovo module, use rsync instead of cp to avoid copying node_modules
  rsync -a "$OVO_MODULE_PATH/ovo" bundle/ --exclude node_modules --exclude test-results --no-links
  cp "$OVO_MODULE_PATH/pyproject.toml" ./bundle/
  # install ovo in dev mode to make sure that we use the most recently deployed files, since the environment is reused when dependency versions don't explicitly change
  echo "-e . # hash $(shasum -a 256 ./bundle/pyproject.toml)" > bundle/requirements.txt
  # copy plugin modules
  mkdir bundle/plugins
  
  # ovo_proteindj
  rsync -a "ovo_proteindj/ovo_proteindj" bundle/plugins/ovo_proteindj --exclude node_modules --exclude test-results --no-links
  cp ovo_proteindj/pyproject.toml bundle/plugins/ovo_proteindj
  echo "-e plugins/ovo_proteindj/" >> bundle/requirements.txt

  # ovo_promb
  rsync -a "ovo_promb/ovo_promb" bundle/plugins/ovo_promb --exclude node_modules --exclude test-results --no-links
  cp ovo_promb/pyproject.toml bundle/plugins/ovo_promb
  echo "-e plugins/ovo_promb/" >> bundle/requirements.txt

  # add any extra requirements
  cat "$EXTRA_REQUIREMENTS_PATH" >> bundle/requirements.txt
  cat bundle/requirements.txt

  ls -l bundle
}

posit_login () {
  which rsconnect
  rsconnect add \
    --name posit \
    --api-key $POSIT_API_KEY \
    --server $POSIT_SERVER
}

posit_deploy () {
  rsconnect deploy streamlit \
    --name posit \
    --app-id "$POSIT_APP_ID" \
    --title "OVO De-novo protein design app" \
    --entrypoint ovo/run_app.py \
    --environment OVO_CONFIG_DIR \
    bundle
}

make_bundle

posit_login

posit_deploy

