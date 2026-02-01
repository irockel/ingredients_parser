module "ingredients_parser" {
  source = "./modules/ingredients_parser"

  providers = {
    aws           = aws
    aws.us_east_1 = aws.us_east_1
  }

  aws_region   = var.aws_region
  project_name = var.project_name
  github_repo  = var.github_repo
  domain_name  = var.domain_name
  subdomain    = var.subdomain
}
