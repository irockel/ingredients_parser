[![Python CI](https://github.com/irockel/ingredients_parser/actions/workflows/ci.yml/badge.svg)](https://github.com/irockel/tda/actions/workflows/build.yml)
[![Renovate](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/irockel/ingredients_parser/issues?q=is%3Aissue+is%3Aopen+label%3Adependencies)
[![Dependencies](https://img.shields.io/librariesio/github/irockel/ingredients_parser)](https://libraries.io/github/irockel/ingredients_parser)
[![License](https://img.shields.io/github/license/irockel/ingredients_parser)](LICENSE)
# 🥗 Nutrition & Ingredients Parser

A lightweight Flask application that extracts **ingredients**, **allergens**, and **nutrition information** from product packaging images using **[EasyOCR](https://github.com/JaidedAI/EasyOCR)**.

![ingredients_scan](ingredients_scan.png)

## 🚀 Features

- **Ingredient Extraction**: Automatically identifies and lists ingredients from a cropped image.
- **Allergen Detection**: Specifically highlights potential allergens (e.g., "Contains: Milk", "May contain: Nuts").
- **Nutrition Parsing**: Extracts nutrition facts for easy digitization.
- **OCR Powered**: Utilizes EasyOCR for robust, offline-capable text recognition.
- **Web Interface**: Simple, user-friendly Flask-based UI for uploading and viewing results.

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- [Optional] GPU for faster OCR processing (defaults to CPU)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ingredients_parser
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Access the UI**:
   Navigate to [http://localhost:5000/](http://localhost:5000/) in your browser.

## 🐳 Docker Support

To run the application using Docker:

1. **Build the image**:
   ```bash
   docker build -t ingredients-parser .
   ```

2. **Run the container**:
   ```bash
   docker run --name ingredients-parser -p 5000:5000 ingredients-parser
   ```

## 🧪 Testing

The project uses `pytest` for testing. To run the tests, use:

```bash
pytest tests/test_ingredients_vision.py
```

Sample images for testing can be found in `tests/static/cropped_ingredients`.

## 📝 Usage Notes

- For best results, ensure the image is **cropped** to the relevant section of the product packaging (ingredients or nutrition table).
- The current version is optimized for English text.

---
*Built with Python, Flask, and EasyOCR.*

 

 
