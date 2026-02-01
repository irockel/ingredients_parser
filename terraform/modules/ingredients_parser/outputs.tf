output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "lambda_function_url" {
  value = aws_lambda_function_url.api_url.function_url
}

output "frontend_s3_url" {
  value = "http://${aws_s3_bucket_website_configuration.frontend.website_endpoint}"
}

output "frontend_s3_bucket" {
  value = aws_s3_bucket.frontend.id
}

output "github_actions_role_arn" {
  value = aws_iam_role.github_actions.arn
}
