import os
import tempfile
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from .ocr.easyocr_provider import EasyOCRProvider
from .ocr.rekognition_provider import RekognitionProvider
from .logic.ingredients import extract_ingredients_and_allergens
from .logic.nutrition import parse_nutrition

app = FastAPI(title="Nutrition & Ingredients Parser API")

# Enable CORS for local development and S3 deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OCR provider based on environment variable
OCR_TYPE = os.getenv("OCR_TYPE", "easyocr").lower()
if OCR_TYPE == "rekognition":
    provider = RekognitionProvider()
else:
    provider = EasyOCRProvider()

@app.get("/")
async def root():
    return {"message": "Nutrition & Ingredients Parser API is running", "ocr_provider": OCR_TYPE}

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Perform OCR
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
