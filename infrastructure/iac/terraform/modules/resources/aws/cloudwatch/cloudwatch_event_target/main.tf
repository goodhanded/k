resource "aws_cloudwatch_event_target" "cloudwatch_event_target" {
  rule = var.rule
  arn  = var.arn
  role_arn = var.role_arn
  event_bus_name = var.event_bus_name

  dynamic "input_transformer" {
    for_each = var.input_transformer != null ? [var.input_transformer] : []
    content {
      input_paths = input_transformer.value.input_paths
      input_template = input_transformer.value.input_template
    }
  }
}