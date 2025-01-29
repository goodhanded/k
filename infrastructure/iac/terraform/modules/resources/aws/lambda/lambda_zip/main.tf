data "archive_file" "lambda_zip" {
  type         = "zip"
  source_file  = var.source_file
  output_path  = "${var.source_file}.zip"
}

module "lambda_function" {
  source = "../lambda_function"
  environment      = var.environment
  function_name    = var.function_name
  handler          = var.handler
  role             = var.role
  runtime          = var.runtime
  filename         = "${var.source_file}.zip"
  timeout          = var.timeout
  source_code_hash = filebase64sha256("${var.source_file}.zip")
  layers           = var.layers
  architectures    = null
  environment_variables = var.env_vars
  package_type = null
}