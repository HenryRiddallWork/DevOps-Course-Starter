terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "cohort32-33_HenRid_ProjectExercise"
    storage_account_name = "henridterraformstateblob"
    container_name       = "henridterraformstatecontainer"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name     = "cohort32-33_HenRid_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-terraformed-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name     = "henryriddall1/azure_production_build:prod"
      docker_registry_url   = "https://docker.io"
    }
  }

  app_settings = {
    "MONGO_CONNECTION_STRING"             = azurerm_cosmosdb_account.db.primary_mongodb_connection_string
    "FLASK_APP"                           = "todo_app/app"
    "FLASK_DEBUG"                         = "false"
    "MONGO_DB_COLLECTION"                 = "todo_items"
    "MONGO_DB_NAME"                       = "todo_db"
    "OAUTH_CLIENT_ID"                     = var.oauth_client_id
    "OAUTH_CLIENT_SECRET"                 = var.oauth_client_secret
    "PREFERRED_URL_SCHEME"                = "https"
    "SECRET_KEY"                          = "secret-key"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}

resource "azurerm_cosmosdb_account" "db" {
  name                = "${var.prefix}-terraformed-mongodb-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  automatic_failover_enabled = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
      name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = "${var.prefix}-terraformed-mongodb-database"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.db.name
}