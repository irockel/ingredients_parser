output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "lambda_function_url" {
  value = aws_lambda_function_url.api_url.function_url
}

output "frontend_s3_url" {
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
