variable "resource_prefix" {
  type        = string
  description = "The naming prefix to add to all resources for uniqueness"
}

variable "aws_account_number" {
  type        = number
  description = "The AWS account number for this environment"
}