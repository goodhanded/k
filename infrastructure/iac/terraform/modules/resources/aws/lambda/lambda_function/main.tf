resource "aws_lambda_function" "lambda_function" {
  function_name    = "${var.environment}-${var.function_name}"
  role             = var.role
  timeout          = var.timeout
  memory_size      = var.memory_size
  layers           = var.layers
  source_code_hash = var.source_code_hash
  handler          = var.handler
  runtime          = var.runtime
  filename         = var.filename
  image_uri        = var.image_uri
  package_type     = var.package_type
  architectures    = var.architectures
  
  dynamic ephemeral_storage {
    for_each = var.ephemeral_storage != null ? [1] : []
    content {
      size = var.ephemeral_storage
    } 
  }

  dynamic environment {
    for_each = var.environment_variables != null ? [1] : []
    content {
      variables = var.environment_variables
    }
  }
}