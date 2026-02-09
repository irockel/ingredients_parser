terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "~> 6.0"
      configuration_aliases = [aws.us_east_1]
    }
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ingredients-parser"
}

variable "github_repo" {
  description = "GitHub repository (username/repo)"
  type        = string
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
}

variable "subdomain" {
  description = "Subdomain for the application"
  type        = string
}

variable "cognito_domain_prefix" {
  description = "Cognito domain prefix for Hosted UI"
  type        = string
}

variable "cognito_app_callback_urls" {
  description = "Callback URLs for Cognito App Client"
  type        = list(string)
  default     = []
}

variable "cognito_app_logout_urls" {
  description = "Logout URLs for Cognito App Client"
  type        = list(string)
  default     = []
}