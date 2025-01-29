resource "aws_glue_job" "job" {
  name              = "${var.environment}-${var.job_name}"
  role_arn          = var.role_arn
  glue_version      = var.glue_version
  execution_class   = var.execution_class
  number_of_workers = var.num_workers
  worker_type       = var.worker_type
  timeout           = var.timeout

  command {
    name = var.command_name
    script_location = var.script_location
  }

  default_arguments = var.default_arguments

  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }
}