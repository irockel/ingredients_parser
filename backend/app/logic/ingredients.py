import re
from typing import List, Dict, Any, Tuple

def extract_ingredients_and_allergens(ocr_results: List[Dict[str, Any]]) -> Tuple[str, str]:
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
