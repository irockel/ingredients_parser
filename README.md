[![Python CI](https://github.com/irockel/ingredients_parser/actions/workflows/ci.yml/badge.svg)](https://github.com/irockel/tda/actions/workflows/build.yml)
[![Renovate](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/irockel/ingredients_parser/issues?q=is%3Aissue+is%3Aopen+label%3Adependencies)
[![Dependencies](https://img.shields.io/librariesio/github/irockel/ingredients_parser)](https://libraries.io/github/irockel/ingredients_parser)
[![License](https://img.shields.io/github/license/irockel/ingredients_parser)](LICENSE)
# 🥗 Nutrition & Ingredients Parser

A lightweight FastAPI application that extracts **ingredients**, **allergens**, and **nutrition information** from product 
packaging images using **[EasyOCR](https://github.com/JaidedAI/EasyOCR)** if running locally. The application can also be installed as Lamdba on AWS. If
deployed to AWS it will use AWS Rekognition for text extraction.

<div style="text-align: center;"><img src="./ingredients_scan.png" alt="Ingredients Parser Result Screen" width="400"></div>

## 🚀 Features

- **Ingredient Extraction**: Automatically identifies and lists ingredients from a cropped image.
- **Allergen Detection**: Specifically highlights potential allergens (e.g., "Contains: Milk", "May contain: Nuts").
- **Nutrition Parsing**: Extracts nutrition facts for easy digitization.
- **OCR Powered**: Utilizes EasyOCR for robust, offline-capable text recognition.
- **Web Interface**: Simple, user-friendly Tailwind-CSS UI for uploading and viewing results.

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- [Optional] GPU for faster OCR processing (defaults to CPU)
- AWS CLI configured (if using Rekognition)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ingredients_parser
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   pip install pytest  # Required for running tests
   ```

4. **Run the application locally**:
   ```bash
   ./run_local.sh
   ```
   This will start the FastAPI backend on port 8000 and a simple web server for the frontend on port 3000.

5. **Access the UI**:
   Navigate to [http://localhost:3000/](http://localhost:3000/) in your browser.

### Switching OCR Provider

The backend supports both EasyOCR and AWS Rekognition. You can switch between them using the `OCR_TYPE` environment variable.

- **EasyOCR (Default)**: `export OCR_TYPE=easyocr`
- **AWS Rekognition**: `export OCR_TYPE=rekognition`

Note: Using Rekognition requires `boto3` to be configured with valid AWS credentials.

### AWS Deployment (Terraform)

The infrastructure is managed using Terraform and includes an ECR repository, a Lambda function (with Function URL), an S3 bucket for the static frontend, and a **CloudFront distribution** with TLS (ACM) for secure, high-performance delivery. It uses a **remote state** stored in S3 for better collaboration and state persistence.

1. **Prerequisites**:
   - Docker installed and running.
   - AWS CLI configured with appropriate permissions.
   - You need to be logged in to your AWS Account and this has to be enabled in the session.
   - Terraform installed.
   - **S3 Bucket for Remote State**: An S3 bucket is required to store the Terraform state. By default, it expects `de-grimmfrost-terraform-state`.
   - **Route 53 Hosted Zone**: A hosted zone for your domain (e.g., `grimmfrost.de`) must already exist in your AWS account.

2. **Initialize and Create ECR Repository**:
   ```bash
   cd terraform
   terraform init
   terraform apply
   cd ..
   ```
   This will fail with the configuration of the Lambda. Run the `deploy_lambda.sh` once to have an initial image in the ECR Repository.

3. **Build and Push the Lambda Image**:
   ```bash
   ./deploy_lambda.sh
   ```
   *Note: On the first run, the script will push the image to ECR but skip the Lambda code update since the function hasn't been created yet.*

4. **Deploy the Rest of the Infrastructure**:
   ```bash
   cd terraform
   terraform apply
   cd ..
   ```

5. **Configure and Deploy Frontend**:
   - Get the Lambda URL from Terraform outputs: `cd terraform && terraform output lambda_function_url`
   - Update `API_URL` in `frontend/index.html` with this value.
   - The frontend is now accessible via the custom domain configured in Terraform (default: `https://ingredients.grimmfrost.de`).
   - Sync the frontend to S3:
   ```bash
   aws s3 sync frontend/ s3://$(cd terraform && terraform output -raw frontend_s3_bucket)/
   ```
   - **GitHub Actions Note**: After the first successful deployment, copy the `cloudfront_distribution_id` from Terraform outputs and update the `CLOUDFRONT_DISTRIBUTION_ID` in `.github/workflows/ci.yml` to enable automatic cache invalidation on future pushes.

6. **Access the App**:
   Use the `frontend_s3_url` (CloudFront URL with custom domain) from Terraform outputs to open the application in your browser.

## 📁 Project Structure

- `backend/`: FastAPI application, OCR logic, and providers.
- `frontend/`: Static HTML/JS frontend, ready for S3 deployment.
- `terraform/`: Infrastructure as Code for usage on AWS.
- `tests/`: Test suites for OCR and parsing logic.

## 🧪 Testing

The project uses `pytest` for testing. To run the tests, use:

```bash
pytest tests/test_ingredients_vision.py
```

*Note: If `easyocr` or `torch` are not installed, these tests will be skipped automatically.*

Sample images for testing can be found in `tests/static/cropped_ingredients`.

## 📝 Usage Notes

- For best results, ensure the image is **cropped** to the relevant section of the product packaging (ingredients or nutrition table).
- The current version is optimized for English text.

---
*Built with Python, Flask, and EasyOCR.*

 

 
