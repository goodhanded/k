resource "aws_iam_role_policy" "iam_role_policy" {
  name = "${var.environment}-${var.name}"
  role = var.role
  policy = var.policy
}