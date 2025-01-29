resource "aws_cognito_user_group" "cognito_user_group" {
  name         = "${var.environment}-${var.name}"
  user_pool_id = var.user_pool_id
  description  = var.description
  role_arn     = var.role_arn
  precedence   = var.precedence
}