import pytest
import os
from backend.app.logic import ingredients
from backend.app.ocr.easyocr_provider import EasyOCRProvider

def test_detect_document_from_cropped_ingredients_png():
    image_path = "tests/static/cropped_ingredients"
    if not os.path.exists(image_path):
        pytest.skip(f"{image_path} not found")
    
    provider = EasyOCRProvider()
    
    for file_name in filter(
        lambda x: x.endswith(".jpg"), sorted(os.listdir(image_path))
    ):
        print(file_name)
        ocr_results = provider.detect_text(image_path + "/" + file_name)
        extracted = ingredients.extract_ingredients_and_allergens(ocr_results)
        print(extracted[0])
        print(extracted[1])
        print("")
