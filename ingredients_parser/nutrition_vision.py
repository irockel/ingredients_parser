import easyocr
import json
import os

from . import config

# Initialize EasyOCR reader
# gpu=False because we might not have a GPU in the environment
reader = easyocr.Reader(['en'], gpu=False)

def detect_text_easyocr(image_path):
    """
    Detect text using EasyOCR and return results in a format similar to what's needed.
    """
    results = reader.readtext(image_path)
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

if __name__ == "__main__":
    # Test with a local file if it exists
    test_image = "ingredients_scan.png"
    if os.path.exists(test_image):
        print(json.dumps(detect_text_easyocr(test_image), indent=2))
