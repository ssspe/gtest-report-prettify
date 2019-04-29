import json
import sys
from jinja2 import FileSystemLoader, Environment
import xml.etree.ElementTree as ET

# Constants
TEMPLATE_FILE = "gtest_template.html"
OUTPUT_FILE = "gtest_output.html"

def process_input(input_file):
    """ Processes the input file.
        Will return a JSON object to be used by the HTML parser.
        If the file is in XML format it will be turned into a JSON object.
    """

    data = None

    with open(input_file) as gtest_json:
        if input_file.endswith('.json'):
            data = json.load(gtest_json)
        elif input_file.endswith('.xml'):
            # Need to turn the XML into the same format as the JSON
            data = process_xml(gtest_json)
        else:
            print("Unknown file type.")
            return

    return data

def process_xml(xml):
    """ Processes the XML file.
        Will return a JSON object that matches that created by GTEST.
    """

    data = {'testsuites': []}
    tree = ET.parse(xml)
    root = tree.getroot()
    for child in root:
        testSuitename = child.attrib['name']
        totalTests = int(child.attrib['tests'])
        failed = int(child.attrib['failures'])

        tempTest = []
        for test in child:
            testName = test.attrib['name']
            testTime = test.attrib['time']

            # Getting all of the failure messages
            testFailures = []
            for failure in test:
                testFailure = failure.attrib['message']
                testFailures.append({
                    'failure': testFailure
                })

            # If there are no failures dont add it to the JSON
            if testFailures:
                tempTest.append({
                    'name': testName,
                    'time': testTime,
                    'failures': testFailures
                })
            else:
                tempTest.append({
                    'name': testName,
                    'time': testTime
                })

        tempTestSuite = {
            'name': testSuitename,
            'tests': totalTests,
            'failures': failed,
            'testsuite': tempTest
        }
        data['testsuites'].append(tempTestSuite)

    return data

def create_html(data):
    """ Turns the JSON object into a HTML file.
        Will grab the template and render it with our JSON object.
    """
    templateLoader = FileSystemLoader(searchpath="./")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)

    with open(OUTPUT_FILE, "w") as output_html:
        output_html.write(template.render(test_suites=data['testsuites']))

if __name__ == "__main__":
    json_data = process_input(sys.argv[1])
    create_html(json_data)
