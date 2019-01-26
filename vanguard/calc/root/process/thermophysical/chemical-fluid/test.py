import requests
import json
import os
from techlib.schemautils import sDocPrj
from clappets.document.utils import load_schema
from clappets.utils import load_function
from clappets import units
from collections import OrderedDict


def run_tests():

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(THIS_FOLDER, 'doc.json')

    # load the input json to a python dictionary named input_json and print
    input_json = json.load(open(input_filename), object_pairs_hook=OrderedDict)
    print ("Check for valid Json File")
#    print(json.dumps(input_json, indent=4))


    # check if json confirms to basic Schema for project document
    #validate the input using the schema
    print("Testing the data with the sDocPrj schema")
    common_schema = sDocPrj()
    parsed_data = common_schema.load(input_json)
    print("Parsed Data from sDocPrj: ")
    print("=========================")
    print(json.dumps(parsed_data.data, indent=4))
    print("Errors from sDocPrj:")
    print("========")
    print(json.dumps(parsed_data.errors, indent=4))
    data1 = parsed_data.data


    schemaModuleFile = os.path.join(THIS_FOLDER, "schema.py")
    docSchema = load_schema(schemaModuleFile)
    parsed_data = docSchema.load(data1)
    print("Parsed Data from docSchema: ")
    print("===========================")
    print(json.dumps(parsed_data.data, indent=4))
    print("Errors from docSchema:")
    print("========")
    print(json.dumps(parsed_data.errors, indent=4))
    data2 = parsed_data.data


    macroModuleFile = os.path.join(THIS_FOLDER, "macro.py")
    calculate = load_function(macroModuleFile, 'calculate')
    doc = data2
    calculate(doc)
    print("Calculation Done ")
    print(json.dumps(doc, indent=4))
