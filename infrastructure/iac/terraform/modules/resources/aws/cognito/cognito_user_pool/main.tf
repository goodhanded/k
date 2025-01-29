resource "aws_cognito_user_pool" "cognito_user_pool" {
  name = "${var.environment}-${var.name}"

  password_policy {
    temporary_password_validity_days = 7
    minimum_length                   = 8
    require_uppercase                = true
    require_lowercase                = true
    require_numbers                  = true
    require_symbols                  = true
  }

  auto_verified_attributes = ["email"]
  mfa_configuration        = "OFF"

  // Adding custom attributes for Name and Title
  schema {
    name                     = "Name"
    attribute_data_type      = "String"
    mutable                  = true
    required                 = false
    string_attribute_constraints {
      min_length             = 2
      max_length             = 100
    }
  }

  schema {
    name                     = "Title"
    attribute_data_type      = "String"
    mutable                  = true
    required                 = false
    string_attribute_constraints {
      min_length             = 2
      max_length             = 100
    }
  }
}