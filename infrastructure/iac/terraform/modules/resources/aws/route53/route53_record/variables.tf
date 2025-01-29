variable environment {}
variable zone_id {}
variable name {}
variable type {}
variable records {
  type    = list(string)
  default = []
}
variable ttl {
  default = null
}
variable aliases {
  type = list(object({
    name                   = string
    zone_id                = string
    evaluate_target_health = bool
  }))
  default = []
}