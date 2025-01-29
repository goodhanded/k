resource "aws_sfn_state_machine" "sfn_state_machine" {
  name       = "${var.environment}-${var.name}"
  role_arn   = var.role_arn
  definition = var.definition
  type       = "STANDARD"
}