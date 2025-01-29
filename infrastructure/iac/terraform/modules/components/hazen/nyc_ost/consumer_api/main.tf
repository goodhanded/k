module "app_service_plan" {
  source              = "../../../../resources/azurerm/service_plan"
  name                = "${var.name}-service-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = var.os_type
  sku_name            = var.sku_name
  tags                = var.tags
}

module "web_app" {
  source              = "../../../../resources/azurerm/windows_web_app"
  name                = "${var.name}-app-service"
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = module.app_service_plan.id

  app_settings = {
    always_on         = var.always_on
  }

  tags = var.tags
}