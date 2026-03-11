terraform {
  backend "s3" {
    key            = "terraform.tfstate"
    dynamodb_table = "terraform-state-lock"
    encrypt        = "true"
  }
}