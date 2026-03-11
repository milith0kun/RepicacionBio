
module "s3-bucket" {
  source = "./modules/s3"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
}

data "aws_iam_policy_document" "omics_workflow_service_role_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["s3:GetObject"]
    resources = ["${module.s3-bucket.s3_bucket_arn}/*",
    "arn:aws:s3:::omics-us-east-1/*"]
  }

  statement {
    effect  = "Allow"
    actions = ["s3:ListBucket"]
    resources = [module.s3-bucket.s3_bucket_arn,
    "arn:aws:s3:::omics-us-east-1"]
  }

  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["${module.s3-bucket.s3_bucket_arn}/*"]
  }

  statement {
    effect = "Allow"
    actions = ["logs:DescribeLogStreams",
      "logs:CreateLogStream",
    "logs:PutLogEvents"]
    resources = ["arn:aws:logs:us-east-1:${var.aws_account_number}:log-group:/aws/omics/WorkflowLog:log-stream:*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:us-east-1:${var.aws_account_number}:log-group:/aws/omics/WorkflowLog:*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["ecr:*"]
    resources = ["arn:aws:ecr:us-east-1:${var.aws_account_number}:repository/*"]
  }

  statement {
    effect = "Allow"
    actions = ["ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
    "ecr:BatchCheckLayerAvailability"]
    resources = ["arn:aws:ecr:us-east-1:${var.aws_account_number}:repository/*"]
  }
}

data "aws_iam_policy_document" "omic_workflow_service_role_trust_policy_doc" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["omics.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "omics_workflow_service_role" {
  //
  // TODO add ovo- prefix
  //
  name               = "${var.resource_prefix}-omics-workflow-service-role"
  assume_role_policy = data.aws_iam_policy_document.omic_workflow_service_role_trust_policy_doc.json
}

module "iam-omics-workflow-service-role-policy" {
  source = "./modules/iam"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
  //
  // TODO add ovo- prefix
  //
  policy_name        = "${var.resource_prefix}-omics-workflow-service-role-policy"
  policy_description = "OVO Omics Workflow Service Role Policy"
  policy             = data.aws_iam_policy_document.omics_workflow_service_role_policy_doc.json
  role_name          = aws_iam_role.omics_workflow_service_role.name
}

module "workflow-rfdiffusion-end-to-end" {
  source = "./modules/workflow"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
  bucket             = module.s3-bucket.s3_bucket_name
  workflow_module    = "ovo"
  workflow_name      = "rfdiffusion-end-to-end"
  dependencies       = "ovo"
}

module "workflow-proteinqc" {
  source = "./modules/workflow"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
  bucket             = module.s3-bucket.s3_bucket_name
  workflow_module    = "ovo"
  workflow_name      = "proteinqc"
  dependencies       = "ovo"
}

module "workflow-pyrosetta-interface-metrics" {
  source = "./modules/workflow"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
  bucket             = module.s3-bucket.s3_bucket_name
  workflow_module    = "ovo"
  workflow_name      = "pyrosetta-interface-metrics"
}

module "workflow-bindcraft" {
  source = "./modules/workflow"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
  bucket             = module.s3-bucket.s3_bucket_name
  workflow_module    = "ovo"
  workflow_name      = "bindcraft"
}

module "workflow-promb" {
  source = "./modules/workflow"

  resource_prefix    = var.resource_prefix
  aws_account_number = var.aws_account_number
  bucket             = module.s3-bucket.s3_bucket_name
  workflow_module    = "ovo_promb"
  workflow_name      = "promb"
}
