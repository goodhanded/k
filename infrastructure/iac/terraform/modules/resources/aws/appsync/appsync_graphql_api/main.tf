resource "aws_appsync_graphql_api" "appsync_graphql_api" {
  name                = "${var.environment}-${var.name}"
  schema              = var.schema
  authentication_type = var.authentication_type

  log_config {
      cloudwatch_logs_role_arn = var.cloudwatch_logs_role_arn
      field_log_level = var.field_log_level
      }

  user_pool_config {
    aws_region     = var.region
    default_action = var.default_action
    user_pool_id   = var.user_pool_id
  }
}
