set -euxo pipefail

WORKFLOW_BUCKET=$1

mkdir -p .model_weights
cd .model_weights

git clone https://github.com/dauparas/ProteinMPNN.git
cd ProteinMPNN
for weight in soluble_model_weights vanilla_model_weights ca_model_weights; do
  aws s3 sync ${weight} s3://${WORKFLOW_BUCKET}/mpnn/model_parameters/${weight}/
done

cd ../.. && rm -rf .model_weights
