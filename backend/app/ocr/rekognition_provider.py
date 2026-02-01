import boto3
from typing import List, Dict, Any
from app.ocr.base import OCRProvider

class RekognitionProvider(OCRProvider):
    def __init__(self, region_name='us-east-1'):
        self.client = boto3.client('rekognition', region_name=region_name)

    def detect_text(self, image_path: str) -> List[Dict[str, Any]]:
        with open(image_path, 'rb') as image:
            response = self.client.detect_text(Image={'Bytes': image.read()})
        
        formatted_results = []
        for detection in response['TextDetections']:
            # We only care about LINE types for consistency with EasyOCR results if possible,
            # or we can take everything. EasyOCR returns lines usually.
            # Rekognition has 'LINE' and 'WORD'.
            if detection['Type'] == 'LINE':
                # Convert Rekognition bounding box to EasyOCR style if needed, 
                # but for now let's just keep what it gives or adapt.
                # Rekognition gives: {'Width': ..., 'Height': ..., 'Left': ..., 'Top': ...}
                # EasyOCR gives: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                
                box = detection['Geometry']['BoundingBox']
                # Note: Rekognition coordinates are normalized (0 to 1)
                # For now, let's just store them. We might need image dimensions to un-normalize if needed by parser.
                # However, the current parser seems to use them for sorting.
                
                # Mocking the bbox structure for now to keep parser happy if it expects 4 points
                left = box['Left']
                top = box['Top']
                right = box['Left'] + box['Width']
                bottom = box['Top'] + box['Height']
                
                bbox = [[left, top], [right, top], [right, bottom], [left, bottom]]
                
                formatted_results.append({
                    "text": detection['DetectedText'],
                    "confidence": detection['Confidence'] / 100.0,
                    "boundingBox": bbox
                })
        return formatted_results
