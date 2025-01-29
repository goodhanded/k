variable rule {}
variable arn {}
variable role_arn {}
variable input_transformer {
  description = "Configuration for the input transformer"
  type = object({
    input_paths     = map(string)
    input_template  = string
  })
  default = null
}
variable event_bus_name { default = null }