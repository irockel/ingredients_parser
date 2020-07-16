FROM python:3

RUN mkdir ingredients_parser && mkdir templates
ADD main.py /
ADD requirements.txt /
ADD setup.cfg /
ADD setup.py /

ADD ingredients_parser/__init__.py ingredients_parser/
ADD ingredients_parser/config.py ingredients_parser/
ADD ingredients_parser/datastore.py ingredients_parser/
ADD ingredients_parser/ingredients_parser.py ingredients_parser/
ADD ingredients_parser/ingredients_vision.py ingredients_parser/
ADD ingredients_parser/nutrition_parser.py ingredients_parser/
ADD ingredients_parser/nutrition_vision.py ingredients_parser/
ADD ingredients_parser/vision_service_account.json ingredients_parser/
ADD templates/index.html templates/
ADD templates/ingredients.html templates/

RUN pip install -r requirements.txt

ENTRYPOINT python main.py



