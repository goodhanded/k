locals {
  format_settings = {
    "csv" = {
      input_format  = "org.apache.hadoop.mapred.TextInputFormat"
      output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
      ser_de_lib    = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
      parameters = {
        "field.delim"            = ","
        "skip.header.line.count" = "1"
        "quoteChar"              = "\""
        "serialization.null.format" = ""
      }
    }
    "parquet" = {
      input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
      output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
      ser_de_lib    = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
      parameters = {}
    }
  }
}


resource "aws_glue_catalog_table" "glue_catalog_table" {
  name          = var.name
  database_name = var.database_name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL = "TRUE"
  }

  storage_descriptor {
    location      = var.location
    input_format  = local.format_settings[var.file_format].input_format
    output_format = local.format_settings[var.file_format].output_format

    ser_de_info {
      name                  = "SerDe"
      serialization_library = local.format_settings[var.file_format].ser_de_lib

      parameters = local.format_settings[var.file_format].parameters
    }

    dynamic "columns" {
      for_each = var.columns
      content {
        name     = columns.value.name
        type     = columns.value.type
      }
    }
  }

  dynamic "partition_keys" {
    for_each = var.partition_keys
    content {
      name     = partition_keys.value.name
      type     = partition_keys.value.type
    }
  }
}
