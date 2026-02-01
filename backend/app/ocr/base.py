from abc import ABC, abstractmethod
from typing import List, Dict, Any

class OCRProvider(ABC):
    @abstractmethod
    def detect_text(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Detects text in an image and returns a list of dictionaries.
        Each dictionary should contain 'text', 'confidence', and 'boundingBox'.
        """
        pass
