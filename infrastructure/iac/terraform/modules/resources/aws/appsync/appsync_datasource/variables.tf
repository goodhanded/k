variable api_id {}
variable environment {}
variable name {}
variable type {
  type = string
  default = "AMAZON_DYNAMODB"
}
variable service_role_arn {}
variable dynamodb_config {
  type = object({
    region = string
    table_name = string
    use_caller_credentials = bool
  })
  default = null
}
variable lambda_config {
  type = object({
    function_arn = string 
  })
  default = null
}