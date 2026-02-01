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
