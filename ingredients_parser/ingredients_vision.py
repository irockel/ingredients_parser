import re
import io
import easyocr
from . import config

# Initialize EasyOCR reader
# gpu=False because we might not have a GPU in the environment
reader = easyocr.Reader(['en'], gpu=False)

ingredients_labels = "INGREDIENTS"


def detect_text_easyocr(path):
    results = reader.readtext(path)
    # result is a list of tuples: (bbox, text, prob)
    # bbox is [[x, y], [x, y], [x, y], [x, y]]

    formatted_results = []
    for (bbox, text, prob) in results:
        formatted_results.append({
            "text": text,
            "confidence": prob,
            "boundingBox": bbox
        })
    return formatted_results


def extract_ingredients_and_allergens(ocr_results):
    allergen_phrases = [
        "may contain",
        "made in a facility that also processes",
        "careful",
        "phenylketonurics",
    ]
    
    # Concatenate all detected text into one string
    full_text = " ".join([item["text"] for item in ocr_results]).lower()
    
    regex = r"ingredients.? (.*?)(\*?(?:{}|contains(?! ?.%)):? .*)?$".format(
        "|".join(allergen_phrases)
    )
    
    try:
        match = re.search(regex, full_text)
        if match:
            ingredients, allergens = match.groups()
            allergens = allergens or ""
            return ingredients.strip(), allergens.strip()
        return "", ""
    except Exception as e:
        print(f"Failed! {e}")
        print(full_text)
        return "", ""
