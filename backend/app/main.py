import os
import tempfile
import base64
import secrets
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from mangum import Mangum
from typing import Dict, Any

from app.logic.ingredients import extract_ingredients_and_allergens
from app.logic.nutrition import parse_nutrition

app = FastAPI(title="Nutrition & Ingredients Parser API")

# Enable CORS for local development and S3 deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic(auto_error=False)

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("BASIC_USER_ID")
    correct_password = os.getenv("BASIC_USER_PASSWORD")
    
    # If not configured, we allow it for local testing if no env vars are set
    if not correct_username or not correct_password:
        return credentials.username if credentials else "local_user"

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )

    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Initialize OCR provider lazily
_provider = None

def get_provider():
    global _provider
    if _provider is None:
        ocr_type = os.getenv("OCR_TYPE", "easyocr").lower()
        if ocr_type == "rekognition":
            from app.ocr.rekognition_provider import RekognitionProvider
            _provider = RekognitionProvider()
        else:
            from app.ocr.easyocr_provider import EasyOCRProvider
            _provider = EasyOCRProvider()
    return _provider

# Mangum handler for AWS Lambda with lifespan disabled for compatibility
handler = Mangum(app, lifespan="off")

@app.get("/")
async def root(username: str = Depends(get_current_user)):
    return {
        "message": "Nutrition & Ingredients Parser API is running",
        "ocr_provider": os.getenv("OCR_TYPE", "easyocr").lower(),
        "user": username
    }

@app.post("/process")
async def process_image(
    file: UploadFile = File(...),
    username: str = Depends(get_current_user)
):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Perform OCR
        provider = get_provider()
        ocr_results = provider.detect_text(tmp_path)
        
        # Extract ingredients and allergens
        ingredients, allergens = extract_ingredients_and_allergens(ocr_results)
        
        # Extract nutrition info
        nutrition = parse_nutrition(ocr_results)
        nutrition_text = "\n".join(nutrition)
        
        # Prepare image for return (encoded as base64) - as in the original app
        with open(tmp_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        return {
            "ingredients": ingredients,
            "allergens": allergens,
            "nutrition": nutrition_text,
            "image_data": encoded_image,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
