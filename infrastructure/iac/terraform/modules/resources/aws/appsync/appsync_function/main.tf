resource "aws_appsync_function" "appsync_function" {
  api_id                    = var.app_id
  data_source               = var.datasource
  name                      = "${var.environment}_${var.name}"
  request_mapping_template  = var.request_template
  response_mapping_template = var.response_template
  function_version          = "2018-05-29"

}
