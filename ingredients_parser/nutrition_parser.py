import json


def get_blocks(api_result):
    api_dict = json.loads(api_result)
    blocks = api_dict["responses"][0]["fullTextAnnotation"]["pages"][0]["blocks"]
    tables = [*filter(lambda x: x["blockType"] == "TABLE", blocks)]
    key_value_pairs = [*filter(lambda x: x["blockType"] == "KEY_VALUE_PAIR", blocks)]
    return tables, key_value_pairs


def y_starting_coordinate(block):  # for sorting
    return block["boundingBox"]["normalizedVertices"][0]["y"]


def process_table(table_block):
    table = table_block["table"]
    # Difference between text and mergedText?
    # TODO sort
    header_rows = []
    for row in table["headerRows"]:
        header_rows.append([i.get("text") for i in row["cells"]])
    body_rows = []
    for row in table["bodyRows"]:
        sorted_cells = sorted(
            row["cells"], key=lambda x: y_starting_coordinate(x["textBlock"])
        )
        body_rows.append([i.get("text") for i in row["cells"]])
    return header_rows, body_rows


def process_key_value_pairs(key_value_pair_blocks):
    sorted_key_value_pair_blocks = sorted(
        key_value_pair_blocks, key=y_starting_coordinate
    )
    return [
        (
            item["keyValuePair"]["keyBlock"]["mergedText"],
            item["keyValuePair"]["valueBlock"]["mergedText"],
        )
        for item in sorted_key_value_pair_blocks
    ]
