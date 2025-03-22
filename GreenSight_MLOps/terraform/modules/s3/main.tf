resource "aws_s3_bucket" "mlops_bucket" {
  bucket = var.bucket_name
  tags = {
    Project = var.project_name
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.mlops_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}
