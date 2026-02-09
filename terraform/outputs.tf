output "ecr_repository_url" {
  value = module.ingredients_parser.ecr_repository_url
}

output "frontend_s3_url" {
  value = module.ingredients_parser.frontend_url
}

output "cloudfront_domain_name" {
  value = module.ingredients_parser.cloudfront_domain_name
}

output "cloudfront_distribution_id" {
  value = module.ingredients_parser.cloudfront_distribution_id
}

output "frontend_s3_bucket" {
  value = module.ingredients_parser.frontend_s3_bucket
}

output "github_actions_role_arn" {
  value = module.ingredients_parser.github_actions_role_arn
}

output "http_api_invoke_url" {
  value = module.ingredients_parser.http_api_invoke_url
}

output "cognito_user_pool_id" {
  value = module.ingredients_parser.cognito_user_pool_id
}

output "cognito_user_pool_client_id" {
  value = module.ingredients_parser.cognito_user_pool_client_id
}

output "cognito_domain" {
  value = module.ingredients_parser.cognito_domain
}
