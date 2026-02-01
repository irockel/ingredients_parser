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
  default     = "irockel/ingredients_parser"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "grimmfrost.de"
}

variable "subdomain" {
  description = "Subdomain for the application"
  type        = string
  default     = "ingredients"
}
