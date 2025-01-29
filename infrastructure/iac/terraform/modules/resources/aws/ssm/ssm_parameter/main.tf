resource "aws_ssm_parameter" "ssm_parameter" {
  name  = "${var.environment}/${var.name}"
  type  = var.type
  value = var.value
}