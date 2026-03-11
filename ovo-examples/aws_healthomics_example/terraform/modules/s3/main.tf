resource "aws_s3_bucket" "ovo_s3_bucket" {
  //
  // TODO rename
  //
  bucket = "${var.resource_prefix}-ovo-demo"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ovo_s3_bucket_encrypt" {
  bucket = aws_s3_bucket.ovo_s3_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "ovo_s3_bucket_block_public" {
  bucket = aws_s3_bucket.ovo_s3_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "ovo_s3_bucket_versioning" {
  bucket = aws_s3_bucket.ovo_s3_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.ovo_s3_bucket.id
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.ovo_s3_bucket.arn
}
