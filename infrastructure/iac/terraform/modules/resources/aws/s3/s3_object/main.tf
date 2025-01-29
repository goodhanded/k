resource "aws_s3_object" "s3_object" {
  bucket = var.bucket
  key    = var.key
  source = var.path
  etag   = var.etag
  content = var.content
  source_hash = var.source_hash
}