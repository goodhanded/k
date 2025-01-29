resource "azurerm_windows_web_app" "windows_web_app" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = var.service_plan_id

  site_config {
    always_on                = var.app_settings.always_on
  }

  tags = var.tags
}