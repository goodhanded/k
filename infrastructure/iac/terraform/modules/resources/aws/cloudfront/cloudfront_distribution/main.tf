resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  origin {
    domain_name = var.domain_name
    origin_id   = var.origin_id
    origin_access_control_id = var.origin_access_control_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${var.environment}-distribution"
  default_root_object = "index.html"
  aliases             = var.aliases

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }

  custom_error_response {
    error_caching_min_ttl   = 0
    error_code              = 404
    response_code           = 200
    response_page_path      = "/index.html"
  }

  custom_error_response {
    error_caching_min_ttl   = 0
    error_code              = 403
    response_code           = 200
    response_page_path      = "/index.html"
  }
}