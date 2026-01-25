import json

def parse_easyocr_nutrition(ocr_results):
    """
    Simplistic parser for EasyOCR results to extract nutrition info.
    Since EasyOCR doesn't return a table structure like Google Vision's Document AI,
    we'll need to group text by Y-coordinate or use heuristics.
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

def get_blocks(api_result):
    """
    Original function for Google Vision results. 
    Kept for compatibility if needed, but updated for EasyOCR usage.
    """
    # If api_result is already a list (from EasyOCR), just return it
    if isinstance(api_result, list):
        return api_result, []
    
    api_dict = json.loads(api_result)
    # The rest depends on Google Vision's format which we are moving away from.
    # We'll just return empty lists if it's not EasyOCR format.
    return [], []
