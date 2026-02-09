resource "aws_lambda_function" "api" {
  function_name = "${var.project_name}-api"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app.repository_url}:latest"
  architectures = ["arm64"]

  timeout     = 30
  memory_size = 512

  environment {
    variables = {
      OCR_TYPE = "rekognition"
    }
  }

  # Lifecycle ignore_changes is useful because CI/CD updates these values
  lifecycle {
    ignore_changes = [image_uri, environment]
  }
}

# Permission for API Gateway to invoke this Lambda will be defined in apigateway.tf
