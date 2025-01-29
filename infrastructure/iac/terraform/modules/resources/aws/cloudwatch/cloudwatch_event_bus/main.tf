resource "aws_cloudwatch_event_bus" "cloudwatch_event_bus" {
  name = "${var.environment}-${var.name}"
}