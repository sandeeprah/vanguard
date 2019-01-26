import math
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    source_option = doc['input']['source_option']['_val']
    SPL1 = parseFloat(doc['input']['SPL1']['_val'])
    R1 = parseFloat(doc['input']['R1']['_val'])
    R2 = parseFloat(doc['input']['R2']['_val'])

    if (source_option == 'point'):
        SPL2 = noise_utils.distAttenPoint(SPL1=SPL1, R1=R1, R2=R2)
    elif (source_option =='line'):
        SPL2 = noise_utils.distAttenLine(SPL1=SPL1, R1=R1, R2=R2)
    elif(source_option =='wall'):
        width = abs(parseFloat(doc['input']['width']['_val']))
        height = abs(parseFloat(doc['input']['height']['_val']))
        SPL2 = noise_utils.distAttenWall(SPL1=SPL1, R1=R1, R2=R2, width=width, height=height)
    else:
        SPL2 = math.nan


    doc['result'].update({'SPL2':{'_val' : str(SPL2)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    return True
