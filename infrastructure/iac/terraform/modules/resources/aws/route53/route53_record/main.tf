resource "aws_route53_record" "route53_record" {
  zone_id = var.zone_id
  name    = var.name
  type    = var.type
  ttl     = var.ttl

  dynamic "alias" {
    for_each = length(var.aliases) > 0 ? var.aliases : []
    content {
      name                   = alias.value.name
      zone_id                = alias.value.zone_id
      evaluate_target_health = alias.value.evaluate_target_health
    }
  }

  records = length(var.records) > 0 ? var.records : null
}
