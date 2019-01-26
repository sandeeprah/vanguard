import math
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    noiseLevelList = doc['input']['noiseLevelList']
    noiseTotal = noise_utils.addNoise(noiseLevelList=noiseLevelList)

    doc['result'].update({'noiseTotal':{'_val' : str(noiseTotal)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    return True
