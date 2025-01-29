resource "aws_sqs_queue" "sqs_queue" {
  name                              = "${var.environment}-${var.name}"
  delay_seconds                     = var.delay_seconds
  max_message_size                  = var.max_message_size
  message_retention_seconds         = var.message_retention_seconds
  receive_wait_time_seconds         = var.receive_wait_time_seconds
  redrive_policy                    = var.redrive_policy
  visibility_timeout_seconds        = var.visibility_timeout_seconds
  kms_data_key_reuse_period_seconds = var.kms_data_key_reuse_period_seconds
  kms_master_key_id                 = var.kms_master_key_id
  fifo_queue                        = var.fifo_queue
  content_based_deduplication       = var.content_based_deduplication
} 