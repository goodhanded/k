resource "aws_cognito_identity_pool_roles_attachment" "cognito_identity_pool_roles_attachment" {
  identity_pool_id = var.identity_pool_id

  roles = {
    "authenticated" = var.role_arn
  }

  role_mapping {
    identity_provider         = var.identity_provider
    ambiguous_role_resolution = "AuthenticatedRole"
    type                      = "Rules"

    mapping_rule {
      claim      = "cognito:groups"
      match_type = "Equals"
      role_arn   = var.role_arn
      value      = var.group_name
    }
  }
}