resource "aws_lambda_function" "api" {
  function_name = "${var.project_name}-api"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app.repository_url}:latest"

  timeout     = 30
  memory_size = 512

  environment {
    variables = {
      OCR_TYPE = "rekognition"
    }
  }

  # Lifecycle ignore_changes for image_uri can be useful if updates are done via CLI
  # lifecycle {
  #   ignore_changes = [image_uri]
  # }
}

resource "aws_lambda_function_url" "api_url" {
  function_name      = aws_lambda_function.api.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = false
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["*"]
    expose_headers    = ["*"]
    max_age           = 86400
  }
}
