resource "aws_s3_bucket_notification" "s3_bucket_notification" {
  bucket = var.bucket
  eventbridge = var.eventbridge
  dynamic "topic" {
    for_each = var.topics
    content {
      topic_arn     = topic.value.topic_arn
      events        = topic.value.events
      filter_prefix = topic.value.filter_prefix
      filter_suffix = topic.value.filter_suffix
    }
  }
  dynamic "lambda_function" {
    for_each = var.lambda_functions
    content {
      lambda_function_arn = lambda_function.value.lambda_function_arn
      events              = lambda_function.value.events
      filter_prefix       = lambda_function.value.filter_prefix
      filter_suffix       = lambda_function.value.filter_suffix
    }
  }
}