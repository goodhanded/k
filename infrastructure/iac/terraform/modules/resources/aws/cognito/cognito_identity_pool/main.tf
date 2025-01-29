resource "aws_cognito_identity_pool" "cognito_identity_pool" {
  identity_pool_name               = "${var.environment}-${var.identity_pool_name}"
  allow_unauthenticated_identities = var.allow_unauthenticated_identities

  cognito_identity_providers {
    client_id               = var.client_id
    provider_name           = var.provider_name
    server_side_token_check = var.server_side_token_check
  }
}