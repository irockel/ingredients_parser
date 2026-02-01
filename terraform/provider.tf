terraform {
  backend "s3" {
    bucket         = "de-grimmfrost-terraform-state"
    key            = "ingredients-parser/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
