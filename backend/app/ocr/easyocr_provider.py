import easyocr
from typing import List, Dict, Any
from app.ocr.base import OCRProvider

class EasyOCRProvider(OCRProvider):
    def __init__(self, languages=['en'], gpu=False):
        self.reader = easyocr.Reader(languages, gpu=gpu)

    def detect_text(self, image_path: str) -> List[Dict[str, Any]]:
        results = self.reader.readtext(image_path)
        formatted_results = []
        for (bbox, text, prob) in results:
            formatted_results.append({
                "text": text,
                "confidence": prob,
                "boundingBox": bbox
            })
        return formatted_results
