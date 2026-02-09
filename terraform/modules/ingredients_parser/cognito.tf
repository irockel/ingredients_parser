resource "aws_cognito_user_pool" "this" {
  name = "${var.project_name}-users"

  password_policy {
    minimum_length                   = 8
    require_lowercase                = true
    require_numbers                  = true
    require_symbols                  = false
    require_uppercase                = true
    temporary_password_validity_days = 7
  }

  auto_verified_attributes = ["email"]
  
  admin_create_user_config {
    allow_admin_create_user_only = true
  }
}

resource "aws_cognito_user_pool_domain" "this" {
  domain       = var.cognito_domain_prefix
  user_pool_id = aws_cognito_user_pool.this.id
}

locals {
  default_callback_urls = [
    "https://${var.subdomain}.${var.domain_name}/",
    "http://localhost:5173/",
    "http://localhost:8000/",
    "http://localhost/"
  ]
  default_logout_urls = local.default_callback_urls
}

resource "aws_cognito_user_pool_client" "this" {
  name         = "${var.project_name}-client"
  user_pool_id = aws_cognito_user_pool.this.id

  allowed_oauth_flows_user_pool_client = true
  supported_identity_providers         = ["COGNITO"]

  # Use implicit flow to return id_token directly to static frontend
  allowed_oauth_flows = ["implicit"]
  allowed_oauth_scopes = [
    "email",
    "openid",
    "profile"
  ]

  callback_urls = length(var.cognito_app_callback_urls) > 0 ? var.cognito_app_callback_urls : local.default_callback_urls
  logout_urls   = length(var.cognito_app_logout_urls) > 0 ? var.cognito_app_logout_urls : local.default_logout_urls

  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_USER_PASSWORD_AUTH"
  ]
}

