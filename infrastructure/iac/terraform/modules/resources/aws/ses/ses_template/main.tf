resource "aws_ses_template" "ses_template" {
  name    = "${var.environment}-${var.name}"
  subject = var.subject
  html    = var.html
  text    = var.text
}
