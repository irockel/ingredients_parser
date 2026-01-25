import os
import base64
import tempfile
from werkzeug.utils import secure_filename
from ingredients_parser import ingredients_vision, nutrition_vision, nutrition_parser
from flask import jsonify, render_template, Flask, request


# Helper function that computes the filepath to save files to
def get_file_path(filename):
    # Note: tempfile.gettempdir() points to an in-memory file system
    # on GCF. Thus, any files in it must fit in the instance's memory.
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)


app = Flask(__name__)


@app.route("/")
def upload_file():
    return render_template("index.html")


@app.route("/ingredients", methods=["GET", "POST"])
def ingredients_parser():
    """ Parses a 'multipart/form-data' upload request
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """

    # This code will process each non-file field in the form
    fields = {}
    data = request.form.to_dict()
    for field in data:
        fields[field] = data[field]
        print("Processed field: %s" % field)

    # This code will process each file uploaded
    files = request.files.to_dict()
    result_dict = {}

    for file_name, file in files.items():
        file_path = get_file_path(file_name)
        file.save(file_path)
        
        # Extract ingredients using EasyOCR
        ocr_results_ingredients = ingredients_vision.detect_text_easyocr(file_path)
        ingredients, allergens = ingredients_vision.extract_ingredients_and_allergens(
            ocr_results_ingredients
        )

        # Extract nutrition info using EasyOCR
        ocr_results_nutrition = nutrition_vision.detect_text_easyocr(file_path)
        nutrition = nutrition_parser.parse_easyocr_nutrition(ocr_results_nutrition)
        nutrition_text = "\n".join(nutrition)

        file_dict = {
            "ingredients": ingredients, 
            "allergens": allergens,
            "nutrition": nutrition_text
        }

        print("Processed file: %s" % file_name)

    # Clear temporary directory
    for file_name in files:
        file_path = get_file_path(file_name)
        with open(file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())

        return render_template(
            "ingredients.html",
            ingredients=file_dict.get("ingredients") or "",
            allergens=file_dict.get("allergens") or "",
            nutrition=file_dict.get("nutrition") or "",
            image_data=encoded_image.decode("utf-8"),
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
