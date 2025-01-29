resource "aws_cloudfront_origin_access_identity" "cloudfront_origin_access_identity" {
  comment = var.comment
}