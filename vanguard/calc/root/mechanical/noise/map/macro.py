import math
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    emissionPoints = doc['input']['emissionPoints']['_list']
    mapArea = doc['input']['mapArea']

    x1 = float(mapArea['x1']['_val'])
    x2 = float(mapArea['x2']['_val'])
    x_step = float(mapArea['x_step']['_val'])
    y1 = float(mapArea['y1']['_val'])
    y2 = float(mapArea['y2']['_val'])
    y_step = float(mapArea['y_step']['_val'])

    x_list = []
    x = x1
    while x < x2 :
        x_list.append(x)
        x = x + x_step

    y_list = []
    y = y1
    while y < y2 :
        y_list.append(y)
        y = y + y_step

    immisionPoints = []
    for x in x_list :
        for y in y_list:
            immisionPoints.append({'x':x, 'y':y})

    noiseField_list = noise_utils.noiseMap(emissionPoints=emissionPoints, immisionPoints=immisionPoints)

    for np in noiseField_list:
        np['x'] = str(np['x'])
        np['y'] = str(np['y'])
        np['noise'] = str(np['noise'])


    noiseField = {
      "_coldim":{
        "x":"length",
        "y":"length"
      },
      "_list" : []
    }
    noiseField['_list']= noiseField_list

#    doc['result']['noiseField']['_list'] = noiseField
    doc['result'].update({'noiseField':noiseField})

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
