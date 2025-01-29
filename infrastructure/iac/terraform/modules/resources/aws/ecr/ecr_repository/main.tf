resource "aws_ecr_repository" "ecr_repository" {
  name = "${var.environment}-${var.name}"
  force_delete = true
}