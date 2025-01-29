resource "aws_iam_role" "iam_role" {
  name = "${var.environment}-${var.name}"
  assume_role_policy = var.assume_role_policy
  
  dynamic inline_policy {
    for_each = var.inline_policy != null ? [1] : [0]
    content {
      policy = var.inline_policy
    }
  }
}