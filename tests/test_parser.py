from pprint import pprint as print
from ingredients_parser import nutrition_parser as parser

with open("tests/static/doritos.json") as f:
    doritos_sample = f.read()

with open("tests/static/table.json") as f:
    table_sample = f.read()


def test_parse_vision_results():
    tables, key_value_pairs = parser.get_blocks(doritos_sample)
    print([*map(parser.process_table, tables)])
    # print(parser.process_key_value_pairs(key_value_pairs))
    tables, key_value_pairs = parser.get_blocks(table_sample)
    print([*map(parser.process_table, tables)])


# print(parser.process_key_value_pairs(key_value_pairs))
