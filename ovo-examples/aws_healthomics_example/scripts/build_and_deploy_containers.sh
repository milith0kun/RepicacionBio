#!/bin/bash

DEFAULT_TAGS="\
ligandmpnn
dssp
proteinsol
pep-patch
esm
python-structure
rfdiffusion
proteinmpnn-fastrelax
colabdesign
bindcraft
"

TAGS=${TAGS:-$DEFAULT_TAGS}

MODULE=${MODULE:-ovo}

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "AWS_ACCOUNT_ID is not set"
    exit 1
fi

if [ -z "$AWS_REGION" ]; then
    echo "AWS_REGION is not set"
    exit 1
fi

if [ -z "$RESOURCE_PREFIX" ]; then
    echo "RESOURCE_PREFIX is not set"
    exit 1
fi

set -euxo pipefail

SCRIPT_DIR=$(dirname $0)
SCRIPT_DIR=$(realpath $SCRIPT_DIR)

# run from ovo-containers submodule directory
cd ovo-containers

if [ -z ${NO_BUILD:-} ]; then
  export DOCKER_DEFAULT_PLATFORM=linux/x86_64
  docker-compose build ${TAGS}
fi

ECR_REGISTRY=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

aws ecr get-login-password --region $AWS_REGION | \
    docker login --password-stdin --username AWS ${ECR_REGISTRY}

cd $SCRIPT_DIR

for tag in $TAGS; do
    repo_name=${RESOURCE_PREFIX}-ovo-${tag}
    if aws ecr describe-repositories --repository-names ${repo_name} --region ${AWS_REGION} | cat; then
        echo "Repository ${repo_name} exists"
    else
        echo "Repository ${repo_name} does not exist, creating"

        # create the repo
        aws ecr create-repository \
            --repository-name ${repo_name} \
            --region ${AWS_REGION} | cat

        # set omics permissions
        aws ecr set-repository-policy \
          --repository-name ${repo_name} \
          --policy-text file://repository-policy.json | cat
    fi

    docker tag ovo-${tag}:latest $ECR_REGISTRY/${repo_name}:latest
    docker push $ECR_REGISTRY/${repo_name}:latest
done
