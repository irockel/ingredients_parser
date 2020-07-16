import pytest
import os
from ingredients_parser import ingredients_vision


def test_detect_document_from_anytizers_png():
    imagepath = "tests/static/cropped_ingredients"
    for file_name in filter(
        lambda x: x.endswith(".jpg"), sorted(os.listdir(imagepath))
    ):
        print(file_name)
        result = ingredients_vision.detect_document(imagepath + "/" + file_name)
        extracted = ingredients_vision.extract_ingredients_and_allergens(result)
        print(extracted[0])
        print(extracted[1])
        print("")


@pytest.mark.skip
def test_detect_document_from_abuelita_png():
    result = ingredients_vision.extract_ingredients_text(
        "tests/static/abuelitaback.png"
    )
    print(result)
