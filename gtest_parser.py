import json
import sys
from jinja2 import FileSystemLoader, Environment

TEMPLATE_FILE = "gtest_template.html"

def process_input(input_file):
    data = None
    with open(input_file) as gtest_json:
        data = json.load(gtest_json)

    return data

def create_html(data):
    templateLoader = FileSystemLoader(searchpath="./")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)

    with open("gtest_output.html", "w") as output_html:
        output_html.write(template.render(test_suites=data['testsuites']))

if __name__ == "__main__":
    json_data = process_input(sys.argv[1])
    create_html(json_data)
