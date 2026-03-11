variable "resource_prefix" {
  type        = string
  description = "The naming prefix to add to all resources for uniqueness"
}

variable "aws_account_number" {
  type        = number
  description = "The AWS account number for this environment"
}

variable "policy_name" {
  type        = string
  description = "The name of the IAM Policy"
}

variable "policy_description" {
  type        = string
  description = "The description of the IAM Policy"
}

variable "role_name" {
  type        = string
  description = "The IAM Role that will contain the given policy"
}

variable "policy" {
  type        = string
  description = "The managd IAM policy that will be attached to the role"
}