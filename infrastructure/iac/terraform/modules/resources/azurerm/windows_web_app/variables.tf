variable name {
  type = string
}
variable location {
  type    = string
  default = "East US"
}
variable resource_group_name {
  type = string
}
variable service_plan_id {
  type = string
}
variable site_config {
  type    = map(string)
  default = null
}
variable app_settings {
  type    = map(string)
  default = {}
}
variable tags {
  type    = map(string)
  default = {}
}