resource "aws_ses_domain_dkim" "ses_domain_dkim" {
  domain = var.domain
}