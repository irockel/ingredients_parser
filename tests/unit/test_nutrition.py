import pytest
from app.logic.nutrition import parse_nutrition

def test_parse_nutrition_sorting():
    ocr_results = [
        {"text": "Line 2", "boundingBox": [[0, 20], [10, 20], [10, 30], [0, 30]]},
        {"text": "Line 1", "boundingBox": [[0, 0], [10, 0], [10, 10], [0, 10]]},
        {"text": "Line 3", "boundingBox": [[0, 40], [10, 40], [10, 50], [0, 50]]}
    ]
    results = parse_nutrition(ocr_results)
    assert results == ["Line 1", "Line 2", "Line 3"]

def test_parse_nutrition_empty():
    results = parse_nutrition([])
    assert results == []
