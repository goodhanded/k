resource "aws_appsync_datasource" "appsync_datasource" {
  api_id           = var.api_id
  name             = replace("${var.environment}_${var.name}", "-", "_")
  type             = var.type
  service_role_arn = var.service_role_arn

  dynamic "dynamodb_config" {
    for_each = var.dynamodb_config != null ? [var.dynamodb_config] : []
    content {
      region                 = dynamodb_config.value.region
      table_name             = dynamodb_config.value.table_name
      use_caller_credentials = dynamodb_config.value.use_caller_credentials
    }
  }

  dynamic "lambda_config" {
    for_each = var.lambda_config != null ? [var.lambda_config] : []
    content {
      function_arn = lambda_config.value.function_arn
    }
  }
}
