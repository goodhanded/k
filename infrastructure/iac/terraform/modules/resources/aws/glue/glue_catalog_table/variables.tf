variable "name" {
  description = "The name of the table."
  type        = string
}

variable "database_name" {
  description = "The name of the database."
  type        = string
}

variable "location" {
  description = "The S3 location where the table data is stored."
  type        = string
}

variable "columns" {
  description = "List of columns for the table."
  type        = list(object({ name = string, type = string }))
  default     = []
}

variable "partition_keys" {
  description = "List of partition keys for the table."
  type        = list(object({ name = string, type = string }))
  default     = []
}

variable "file_format" {
  description = "The file format for the Glue table (csv/parquet)"
  type        = string
  default     = "parquet"
}