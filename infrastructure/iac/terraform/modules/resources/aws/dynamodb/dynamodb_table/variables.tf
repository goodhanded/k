variable environment {
  description = "The environment name"
  type        = string
}
variable name {
  description = "The name of the table, this will be prefixed with the environment"
  type        = string
}
variable billing_mode {
  description = "Controls how you are charged for read and write throughput and how you manage capacity"
  type        = string
  default     = "PAY_PER_REQUEST"
  validation {
    condition     = var.billing_mode == "PROVISIONED" || var.billing_mode == "PAY_PER_REQUEST"
    error_message = "billing_mode must be either PROVISIONED or PAY_PER_REQUEST"
  }
}
variable hash_key {
  description = "The hash key of the table"
  type        = string
}
variable range_key {
  description = "The range key of the table; only required if the table has a range key"
  type        = string
  default = null
}
variable attributes {
  type = list(object({
    name = string
    type = string
  }))
}
variable global_secondary_indexes {
  description = "A list of maps defining global secondary indexes"
  type = list(object({
    name               = string
    hash_key           = string
    range_key          = optional(string)
    projection_type    = string
    non_key_attributes = optional(list(string))
    read_capacity      = optional(number)
    write_capacity     = optional(number)
  }))
  default = []
}
variable stream_enabled {
  description = "Enable DynamoDB Streams"
  type        = bool
  default     = false
}
variable stream_view_type {
  description = "When an item in the table is modified, StreamViewType determines what information is written to the table's stream"
  type        = string
  default     = null
}