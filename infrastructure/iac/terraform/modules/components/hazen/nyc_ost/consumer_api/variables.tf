variable location {
  type = string
  default = "East US"
}

variable name {
  type = string
  default = "consumer-api"
}

variable resource_group_name {
  type = string
}

variable os_type {
  type = string
  default = "Windows"
}

variable sku_name {
  type = string
  default = "B1"
}

variable always_on {
  type = bool
  default = true  
}

variable tags {
  type = map(string)
  default = {}
}