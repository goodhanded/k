data "aws_caller_identity" "current" {}

locals {
  source_code_hash = filemd5("../../src/${replace(var.function_name, "-", "_")}/handler.py") # Important: must modify handler.py to trigger rebuild. 
  repo_name = "${var.function_name}-repo"
}

module "lambda_function" {
  source = "../lambda_function"
  function_name    = var.function_name
  environment      = var.environment 
  role             = var.role
  timeout          = var.timeout
  memory_size      = var.memory_size
  image_uri        = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.environment}-${local.repo_name}:latest"
  package_type     = "Image"
  architectures    = var.architectures
  environment_variables = var.env_vars

  depends_on = [
    null_resource.build_and_push,
    module.ecr_repo
  ]
}

resource "null_resource" "build_and_push" {
  triggers = {
    source_code_hash = local.source_code_hash # This only changes when handler.py is updated. When modifying other files, add or remove a line break from handler.py to trigger build and deployment.
  }

  provisioner "local-exec" {
    command = "../../scripts/build.sh ${var.function_name} ${var.environment} ${var.platform}"
  }

  depends_on = [
    module.ecr_repo
  ]
}

module "ecr_repo" {
  source = "../../ecr/ecr_repository"
  name = local.repo_name
  environment = var.environment
}