variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "oauth_client_id" {
  description = "The oauth client id"
  sensitive = true
}

variable "oauth_client_secret" {
  description = "The oauth client secret"
  sensitive = true
}