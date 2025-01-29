resource "aws_s3_bucket_ownership_controls" "s3_bucket_ownership_controls" {
  bucket = var.bucket
  rule {
    object_ownership = var.object_ownership
  }
}