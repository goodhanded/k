resource "aws_sns_topic" "sns_topic" {
  name = replace("${var.environment}-${var.name}","_","-")
}