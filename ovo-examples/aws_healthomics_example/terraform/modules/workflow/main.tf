locals {
  workflow_dir = "${path.module}/../../../${var.workflow_module}/${var.workflow_module}/pipeline/workflows/${var.workflow_name}"

  # Generate HealthOmics param schema JSON from workflow scheme JSON
  workflow_schema        = yamldecode(file("${local.workflow_dir}/nextflow_schema.json"))
  aws_parameter_template = jsondecode(file("${path.module}/aws-parameter-template.json"))
  workflow_schema_as_params = {
    for k, v in local.workflow_schema["properties"] :
    k => {
      description = try(v["description"], k)
      optional    = !(contains(local.workflow_schema["required"], k))
    }
  }
  parameter_template = merge(local.workflow_schema_as_params, local.aws_parameter_template)

  custom_config_path = "${path.module}/../../../workflows/${var.workflow_module}/${var.workflow_name}/nextflow.config"
  temp_source_dir    = "${path.module}/${var.workflow_module}-${var.workflow_name}-workflow"
  zip_local_path     = "${path.module}/${var.workflow_module}-${var.workflow_name}-workflow.zip"
}

resource "null_resource" "prepare_workflow_dir" {
  triggers = {
    always_run = timestamp() # Forces re-creation
  }

  provisioner "local-exec" {
    command = (var.dependencies != ""
      # Workflow has dependencies
      # 1. Copy all dependent modules into the temp source dir (ovo/workflow-name, ovo_other_package/another-workflow-name, etc)
      # 2. Append nextflow.config file from this repo's workflow directory to the original nextflow.config in its workflow directory
      ? "rm -rf ${local.temp_source_dir}; mkdir -p ${local.temp_source_dir}; echo '${jsonencode(local.parameter_template)}' | jq > ${local.temp_source_dir}/params.json; for dir in ${var.dependencies}; do cp -r ${path.module}/../../../$dir/$dir/pipeline/workflows/ ${local.temp_source_dir}/$dir; done; echo '' >> ${local.temp_source_dir}/${var.workflow_module}/${var.workflow_name}/nextflow.config; cat ${local.custom_config_path} >> ${local.temp_source_dir}/${var.workflow_module}/${var.workflow_name}/nextflow.config;"
      # Workflow has no dependencies
      # 1. Copy workflow directory (with main.nf file) into the temp source dir
      # 2. Append nextflow.config file from this repo's /workflows/module/workflow-name directory to the original nextflow.config in the workflow directory
      : "rm -rf ${local.temp_source_dir}; cp -r ${local.workflow_dir} ${local.temp_source_dir}; echo '' >> ${local.temp_source_dir}/nextflow.config; cat ${local.custom_config_path} >> ${local.temp_source_dir}/nextflow.config;"
    )
  }
}

data "archive_file" "zip_workflow_dir" {
  depends_on  = [null_resource.prepare_workflow_dir]
  type        = "zip"
  source_dir  = local.temp_source_dir
  output_path = local.zip_local_path
}

resource "aws_s3_object" "zipped_workflow_to_s3" {
  depends_on = [data.archive_file.zip_workflow_dir]
  bucket     = var.bucket
  key        = "ovo_workflow_definitions/${var.workflow_module}-${var.workflow_name}-${data.archive_file.zip_workflow_dir.output_md5}.zip"
  source     = local.zip_local_path
  etag       = data.archive_file.zip_workflow_dir.output_md5
}

resource "awscc_omics_workflow" "workflow" {
  depends_on         = [aws_s3_object.zipped_workflow_to_s3]
  name               = "${var.resource_prefix}_${var.workflow_module}_${var.workflow_name}"
  parameter_template = local.parameter_template
  main               = var.dependencies != "" ? "${var.workflow_module}/${var.workflow_name}/main.nf" : "main.nf"
  definition_uri     = "s3://${var.bucket}/ovo_workflow_definitions/${var.workflow_module}-${var.workflow_name}-${data.archive_file.zip_workflow_dir.output_md5}.zip"
}

output "workflow_id" {
  value = awscc_omics_workflow.workflow.workflow_id
}

output "workflow_arn" {
  value = awscc_omics_workflow.workflow.arn
}
