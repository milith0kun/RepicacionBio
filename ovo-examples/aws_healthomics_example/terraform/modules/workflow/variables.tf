variable "resource_prefix" {
  type        = string
  description = "The naming prefix to add to all resources for uniqueness"
}

variable "aws_account_number" {
  type        = number
  description = "The AWS account number for this environment"
}

variable "bucket" {
  type        = string
  description = "Location of the zipped workflow"
}

variable "workflow_module" {
  type        = string
  description = "Module containing the workflow definition, e.g. 'ovo'"
}

variable "workflow_name" {
  type        = string
  description = "The workflow name"
}

variable "dependencies" {
  type        = string
  description = "Workflow dependency modules that should be packaged in the workflow zip, separated by space"
  default     = ""
}
