resource "aws_cognito_user_pool_client" "cognito_user_pool_client" {
  name = "${var.environment}-${var.name}"

  user_pool_id = var.user_pool_id

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  generate_secret = false
}