#!/bin/bash

# Configuration
REGION=$(aws configure get region)
REGION=${REGION:-eu-central-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]; then
    echo "Error: Failed to get AWS Account ID. Is AWS CLI configured?"
    exit 1
fi

REPO_NAME="ingredients-parser"
IMAGE_TAG="latest"
IMAGE_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_TAG}"
LAMBDA_NAME="ingredients-parser-api"

echo "🚀 Starting code deployment for $LAMBDA_NAME"
echo "📍 Region: $REGION"
echo "🆔 Account: $ACCOUNT_ID"

# 1. Build the Docker image
echo "📦 Building Docker image..."
# Determine architecture (default to arm64 if on Mac M-series, otherwise could use buildx)
ARCH=$(uname -m)
if [ "$ARCH" == "arm64" ]; then
    PLATFORM="linux/arm64"
else
    PLATFORM="linux/amd64"
fi
echo "🏗️  Building for platform: $PLATFORM"
# We use buildx if available to ensure we can disable provenance/sbom attestations 
# which cause issues with Lambda media types
if docker buildx version > /dev/null 2>&1; then
    docker buildx build --platform $PLATFORM -t $REPO_NAME -f backend/Dockerfile.lambda --provenance=false --sbom=false --load .
else
    docker build --platform $PLATFORM -t $REPO_NAME -f backend/Dockerfile.lambda .
fi

# 2. Authenticate Docker to ECR
echo "🔐 Authenticating Docker to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

# 3. Tag and Push the image
echo "📤 Pushing image to ECR..."
docker tag ${REPO_NAME}:latest $IMAGE_URI
docker push $IMAGE_URI

# 4. Update Lambda Function code (only if it exists)
if aws lambda get-function --function-name $LAMBDA_NAME > /dev/null 2>&1; then
    # Wait for any existing update to complete before starting a new one
    echo "⏳ Checking if Lambda is ready for update..."
    aws lambda wait function-updated --function-name $LAMBDA_NAME

    echo "🔄 Updating Lambda function code..."
    aws lambda update-function-code --function-name $LAMBDA_NAME --image-uri $IMAGE_URI
    
    # Wait for the current function code update to complete before updating configuration
    echo "⏳ Waiting for Lambda function update to complete..."
    aws lambda wait function-updated --function-name $LAMBDA_NAME

    # Optional: Update environment variables if provided in the local environment
    if [ ! -z "$BASIC_USER_ID" ] && [ ! -z "$BASIC_USER_PASSWORD" ]; then
        echo "🔐 Updating Basic Auth configuration..."
        aws lambda update-function-configuration --function-name $LAMBDA_NAME \
            --environment "Variables={OCR_TYPE=rekognition,BASIC_USER_ID=$BASIC_USER_ID,BASIC_USER_PASSWORD=$BASIC_USER_PASSWORD}"
    fi
else
    echo "ℹ️  Lambda function $LAMBDA_NAME not found. Skipping code update (Terraform will create it)."
fi

echo "✅ Deployment successful!"
