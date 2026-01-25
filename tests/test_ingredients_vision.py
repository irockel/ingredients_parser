import pytest
import os
from ingredients_parser import ingredients_vision


def test_detect_document_from_anytizers_png():
    imagepath = "tests/static/cropped_ingredients"
    if not os.path.exists(imagepath):
        pytest.skip(f"{imagepath} not found")
    for file_name in filter(
        lambda x: x.endswith(".jpg"), sorted(os.listdir(imagepath))
    ):
        print(file_name)
        ocr_results = ingredients_vision.detect_text_easyocr(imagepath + "/" + file_name)
        extracted = ingredients_vision.extract_ingredients_and_allergens(ocr_results)
        print(extracted[0])
        print(extracted[1])
        print("")


@pytest.mark.skip
def test_detect_document_from_abuelita_png():
    pass
