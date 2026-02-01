output "ecr_repository_url" {
  value = module.ingredients_parser.ecr_repository_url
}

output "lambda_function_url" {
  value = module.ingredients_parser.lambda_function_url
}

output "frontend_s3_url" {
  value = module.ingredients_parser.frontend_s3_url
}

output "frontend_s3_bucket" {
  value = module.ingredients_parser.frontend_s3_bucket
}

output "github_actions_role_arn" {
  value = module.ingredients_parser.github_actions_role_arn
}
