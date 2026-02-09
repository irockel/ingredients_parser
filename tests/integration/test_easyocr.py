import pytest
import os
from app.ocr.easyocr_provider import EasyOCRProvider
from app.logic.ingredients import extract_ingredients_and_allergens

@pytest.fixture(scope="module")
def ocr_provider():
    try:
        return EasyOCRProvider()
    except (ImportError, ModuleNotFoundError) as e:
        pytest.skip(f"Skipping test because OCR provider dependencies are missing: {e}")

def get_test_images():
    image_dir = "tests/static/cropped_ingredients"
    if not os.path.exists(image_dir):
        return []
    return [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".jpg")]

@pytest.mark.parametrize("image_path", get_test_images())
def test_easyocr_detection(ocr_provider, image_path):
    results = ocr_provider.detect_text(image_path)
    assert isinstance(results, list)
    assert len(results) > 0
    
    for item in results:
        assert "text" in item
        assert "boundingBox" in item
        assert "confidence" in item

    ingredients, allergens = extract_ingredients_and_allergens(results)
    # At least check that they are strings
    assert isinstance(ingredients, str)
    assert isinstance(allergens, str)
