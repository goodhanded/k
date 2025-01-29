resource "aws_ses_receipt_rule_set" "ses_receipt_rule_set" {
  rule_set_name = "${var.environment}-${var.name}"
}