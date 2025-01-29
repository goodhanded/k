resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment" {
  policy_arn = var.policy_arn
  role       = var.role
}