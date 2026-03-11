# OVO AWS deployment

This repository contains the configuration and Terraform scripts for deploying OVO into AWS HealthOmics.

## Continuous deployment

Continuous deployment pipeline defined in the GitHub action: [.github/workflows/terraform.yml](.github/workflows/terraform.yml)

## Initial deployment

Initialize ovo submodule:

```bash
git submodule init
git submodule update
```

Build and deploy docker containers:

```
export RESOURCE_PREFIX="dev"
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=123

scripts/build_and_deploy_containers.sh
```

Load the additional data (*run once per account*):
```
bash load_mpnn_model_data.sh ${ENVIRONMENT}-healthomics-analysis
bash load_rfdiffusion_model_data.sh ${ENVIRONMENT}-healthomics-analysis
# alphafold models are in a public repo
```

## Local development

### Without backend - local debugging

Initialize terraform:

```bash
cd ./terraform/
cp backend_override.tf.template backend_override.tf
terraform init
```

Build a workflow zip file:

```bash
cd ./terraform/
terraform apply -target=module.workflow-rfdiffusion-end-to-end.data.archive_file.zip_workflow
```
