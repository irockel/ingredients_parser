import pytest
from app.logic.ingredients import extract_ingredients_and_allergens

def test_extract_ingredients_and_allergens_basic():
    ocr_results = [
        {"text": "Ingredients:", "boundingBox": []},
        {"text": "Water, Sugar, Salt.", "boundingBox": []}
    ]
    ingredients, allergens = extract_ingredients_and_allergens(ocr_results)
    assert ingredients == "water, sugar, salt."
    assert allergens == ""

def test_extract_ingredients_and_allergens_with_allergens():
    ocr_results = [
        {"text": "Ingredients:", "boundingBox": []},
        {"text": "Milk, Flour.", "boundingBox": []},
        {"text": "Contains: Wheat.", "boundingBox": []}
    ]
    ingredients, allergens = extract_ingredients_and_allergens(ocr_results)
    assert ingredients == "milk, flour."
    assert allergens == "contains: wheat."

def test_extract_ingredients_and_allergens_may_contain():
    ocr_results = [
        {"text": "Ingredients: Soy.", "boundingBox": []},
        {"text": "May contain peanuts.", "boundingBox": []}
    ]
    ingredients, allergens = extract_ingredients_and_allergens(ocr_results)
    assert ingredients == "soy."
    assert allergens == "may contain peanuts."

def test_extract_ingredients_and_allergens_no_match():
    ocr_results = [
        {"text": "This is some random text", "boundingBox": []}
    ]
    ingredients, allergens = extract_ingredients_and_allergens(ocr_results)
    assert ingredients == ""
    assert allergens == ""

def test_extract_ingredients_and_allergens_empty():
    ingredients, allergens = extract_ingredients_and_allergens([])
    assert ingredients == ""
    assert allergens == ""
