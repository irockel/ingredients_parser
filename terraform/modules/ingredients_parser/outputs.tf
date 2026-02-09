output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}


output "frontend_url" {
  value = "https://${var.subdomain}.${var.domain_name}"
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.s3_distribution.domain_name
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.s3_distribution.id
}

output "frontend_s3_bucket" {
  value = aws_s3_bucket.frontend.id
}

output "github_actions_role_arn" {
  value = aws_iam_role.github_actions.arn
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.this.id
}

output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.this.id
}

output "cognito_user_pool_client_audience" {
  description = "Audience (client ID) to configure API Gateway JWT authorizer"
  value       = aws_cognito_user_pool_client.this.id
}

output "cognito_domain" {
  value = aws_cognito_user_pool_domain.this.domain
}

