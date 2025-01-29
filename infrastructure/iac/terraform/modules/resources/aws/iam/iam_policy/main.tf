resource "aws_iam_policy" "iam_policy" {
  name        = "${var.environment}-${var.name}"
  path        = var.path
  description = var.description
  policy      = var.policy
}