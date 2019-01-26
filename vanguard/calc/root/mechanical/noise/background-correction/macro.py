import math
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    correction_option = doc['input']['correction_option']['_val']

    if (correction_option == 'spectrum'):
        totalSpectrum = doc['input']['totalSpectrum']
        backgroundSpectrum = doc['input']['backgroundSpectrum']
        sourceSpectrum = noise_utils.correctSpectrum(totalSpectrum=totalSpectrum, backgroundSpectrum=backgroundSpectrum)

        for key,value in sourceSpectrum.items():
            sourceSpectrum[key] = str(value)

        doc['result']['sourceSpectrum'] = sourceSpectrum
        
    else:
        totalNoise = parseFloat(doc['input']['totalNoise']['_val'])
        backgroundNoise = parseFloat(doc['input']['backgroundNoise']['_val'])
        sourceNoise = noise_utils.correctBackNoise(noiseTotal=totalNoise, noiseBackground=backgroundNoise)
        doc['result']['sourceNoise']['_val'] = str(sourceNoise)

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
