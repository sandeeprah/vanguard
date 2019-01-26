import requests
import json
import os
from copy import deepcopy
from techlib.schemautils import sDocPrj
from clappets.document.utils import load_schema
from clappets.utils import load_function
from clappets import units
from collections import OrderedDict


def run_tests():

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(THIS_FOLDER, 'doc.json')

    # load the input json to a python dictionary named input_json and print
    doc0 = json.load(open(input_filename), object_pairs_hook=OrderedDict)
    print ("Check for valid Json File")
    print(json.dumps(doc0, indent=4))

    # check if json confirms to basic Schema for project document
    #validate the input using the schema
    print("Testing the data with the sDocPrj schema")
    common_schema = sDocPrj()
    parsed_data = common_schema.load(doc0)
    print("Parsed Data from sDocPrj: ")
    print("=========================")
    print(json.dumps(parsed_data.data, indent=4))
    print("Errors from sDocPrj:")
    print("========")
    print(json.dumps(parsed_data.errors, indent=4))
    doc1 = parsed_data.data


    schemaModuleFile = os.path.join(THIS_FOLDER, "schema.py")
    docSchema = load_schema(schemaModuleFile)
    parsed_data = docSchema.load(doc1)
    print("Parsed Data from docSchema: ")
    print("===========================")
    print(json.dumps(parsed_data.data, indent=4))
    print("Errors from docSchema:")
    print("========")
    print(json.dumps(parsed_data.errors, indent=4))
    doc2 = parsed_data.data

    '''
    macroModuleFile = os.path.join(THIS_FOLDER, "macro.py")
    calculate = load_function(macroModuleFile, 'calculate')
    doc3 = deepcopy(doc2)
    calculate(doc3)
    print("Calculation Done ")
    print(json.dumps(doc3, indent=4))



    data={
        "doc" : doc0
    }

    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    url = "http://127.0.0.1:5000/api/document/calculate/"
    response = requests.post(url, data=data_json, headers=headers)
    print("Checking REST API")
    print("REST API Response Code : " + str(response.status_code))
    print(response.text)


    '''
