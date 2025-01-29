resource "aws_acm_certificate" "acm_certificate" {
  domain_name       = var.domain_name
  validation_method = var.validation_method

  subject_alternative_names = var.subject_alternative_names

  lifecycle {
    create_before_destroy = var.create_before_destroy
  }
}