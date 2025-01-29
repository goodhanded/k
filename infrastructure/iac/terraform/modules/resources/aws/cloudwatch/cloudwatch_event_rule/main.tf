resource "aws_cloudwatch_event_rule" "cloudwatch_event_rule" {
  name        = "${var.environment}-${var.name}"
  description = var.description
  event_pattern = var.event_pattern
  event_bus_name = var.event_bus_name
}