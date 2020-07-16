import re
import io
from google.cloud import storage

# from google.cloud import vision_v1 as vision  # Alpha API
from google.cloud import vision

from . import config

#
# Initialization block, get bucket, create vision_client and storage_client
#
BUCKET = config.BUCKET_NAME

vision_client = vision.ImageAnnotatorClient.from_service_account_json(
    config.KEYFILE_PATH
)
storage_client = storage.Client.from_service_account_json(config.KEYFILE_PATH)

#
# detect document data from a local image with the given path.
#


def detect_document(path):
    with io.open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = vision_client.text_detection(image=image)
    return response


breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType

ingredients_labels = "INGREDIENTS"


def extract_all_ingredients_blocks(annotation):
    """
    WIP/experimental function to grab paragraphs that start with 'ingredients'
    """
    ingredients_block = None
    text_block = None
    for page in annotation.pages:
        print(len(page.blocks))
        for block in page.blocks:
            paragraph_str = ""
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        paragraph_str += symbol.text
                        if symbol.property.detected_break.type == breaks.SPACE:
                            paragraph_str += " "
                        if symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                            paragraph_str += " \n"
                        if symbol.property.detected_break.type == breaks.LINE_BREAK:
                            paragraph_str += "\n"
            if paragraph_str.lower().startswith("ingredients"):
                return paragraph_str


def extract_ingredients_and_allergens(response):
    allergen_phrases = [
        "may contain",
        "made in a facility that also processes",
        "careful",
        "phenylketonurics",
    ]
    full_text = response.full_text_annotation.text.lower().replace("\n", " ")
    regex = r"ingredients.? (.*?)(\*?(?:{}|contains(?! ?.%)):? .*)?$".format(
        "|".join(allergen_phrases)
    )  # TODO: Fix regular expression
    try:
        match = re.match(regex, full_text)
        ingredients, allergens = match.groups()
        allergens = allergens or ""
        return ingredients, allergens
    except AttributeError as e:
        print("Failed!")
        print(full_text)
        return "", ""
