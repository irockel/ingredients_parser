module "ingredients_parser" {
  source = "./modules/ingredients_parser"

  aws_region   = var.aws_region
  project_name = var.project_name
}
