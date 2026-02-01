from typing import List, Dict, Any

def parse_nutrition(ocr_results: List[Dict[str, Any]]) -> List[str]:
    """
    Simplistic parser for OCR results to extract nutrition info.
    We'll need to group text by Y-coordinate or use heuristics.
    """
    # Sort by Y-coordinate (top to bottom)
    # bbox is [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # we use the average Y of the top two points
    sorted_results = sorted(ocr_results, key=lambda x: (x['boundingBox'][0][1] + x['boundingBox'][1][1]) / 2)
    
    nutrition_info = []
    for item in sorted_results:
        text = item['text']
        # Very simple extraction: just return the lines
        nutrition_info.append(text)
        
    return nutrition_info
