resource "aws_cloudfront_origin_access_control" "cloudfront_origin_access_control" {
  origin_access_control_origin_type = "s3"
  name = "${var.environment}-${var.name}"
  signing_behavior = "always"
  signing_protocol = "sigv4"
}