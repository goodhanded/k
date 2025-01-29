resource "aws_ses_receipt_rule" "ses_receipt_rule" {
  name          = "${var.environment}-${var.name}"
  rule_set_name = var.rule_set_name
  recipients    = var.recipients
  enabled       = var.enabled
  scan_enabled  = var.scan_enabled
  tls_policy    = var.tls_policy

  dynamic "s3_action" {
    for_each = var.s3_actions
    content {
      bucket_name       = s3_action.value.bucket_name
      object_key_prefix = lookup(s3_action.value, "object_key_prefix", null)
      kms_key_arn       = lookup(s3_action.value, "kms_key_arn", null)
      position          = s3_action.value.position
      topic_arn         = lookup(s3_action.value, "topic_arn", null)
    }
  }

  dynamic "lambda_action" {
    for_each = var.lambda_actions
    content {
      function_arn    = lambda_action.value.function_arn
      invocation_type = lambda_action.value.invocation_type
      position        = lambda_action.value.position
      topic_arn       = lookup(lambda_action.value, "topic_arn", null)
    }
  }

  dynamic "sns_action" {
    for_each = var.sns_actions
    content {
      topic_arn = sns_action.value.topic_arn
      position  = sns_action.value.position
    }
  }

  dynamic "bounce_action" {
    for_each = var.bounce_actions
    content {
      message          = bounce_action.value.message
      sender           = bounce_action.value.sender
      smtp_reply_code  = bounce_action.value.smtp_reply_code
      status_code      = lookup(bounce_action.value, "status_code", null)
      topic_arn        = lookup(bounce_action.value, "topic_arn", null)
      position         = bounce_action.value.position
    }
  }

  dynamic "stop_action" {
    for_each = var.stop_actions
    content {
      scope    = stop_action.value.scope
      position = stop_action.value.position
      topic_arn = lookup(stop_action.value, "topic_arn", null)
    }
  }

  dynamic "workmail_action" {
    for_each = var.workmail_actions
    content {
      organization_arn = workmail_action.value.organization_arn
      position         = workmail_action.value.position
      topic_arn        = lookup(workmail_action.value, "topic_arn", null)
    }
  }

  # Add Header Action
  dynamic "add_header_action" {
    for_each = var.add_header_actions
    content {
      header_name  = add_header_action.value.header_name
      header_value = add_header_action.value.header_value
      position     = add_header_action.value.position
    }
  }
}
