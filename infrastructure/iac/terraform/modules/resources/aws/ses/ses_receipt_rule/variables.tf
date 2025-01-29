variable environment {}

variable "name" {
  type        = string
  description = "The name of the rule"
}

variable "rule_set_name" {
  type        = string
  description = "The name of the rule set that the rule belongs to"
}

variable "recipients" {
  type        = list(string)
  description = "A list of email addresses or domains to match"
  default     = []
}

variable "enabled" {
  type        = bool
  description = "Whether the rule is active"
  default     = true
}

variable "scan_enabled" {
  type        = bool
  description = "Whether to enable spam and virus scanning"
  default     = true
}

variable "tls_policy" {
  type        = string
  description = "Whether to require TLS"
  default     = "Optional"
}

variable "s3_actions" {
  type = list(map(any))
  default = []
}

variable "lambda_actions" {
  type = list(map(any))
  default = []
}

variable "sns_actions" {
  type = list(map(any))
  default = []
}

variable "bounce_actions" {
  type = list(map(any))
  default = []
}

variable "stop_actions" {
  type = list(map(any))
  default = []
}

variable "workmail_actions" {
  type = list(map(any))
  default = []
}

variable "add_header_actions" {
  description = "A list of add_header_action configurations"
  type        = list(map(any))
  default     = []
}