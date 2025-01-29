resource "aws_appsync_resolver" "get_sales_rep_dashboard_resolver" {
  api_id      = var.api_id
  field       = var.field
  type        = var.type
  data_source = var.data_source
  request_template = var.request_template
  response_template = var.response_template
  kind = var.kind
  dynamic "pipeline_config" {
      for_each = length(var.functions) > 0 ? [1] : []
      content {
          functions = var.functions
          }
      }
}
