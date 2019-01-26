from math import *
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy
from techlib.mathutils import roundit
from techlib.electrical.phase import PFC_compensation

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    try:
        P = float(doc['input']['P']['_val'])
        pf_actual = float(doc['input']['pf_actual']['_val'])
        pf_desired = float(doc['input']['pf_desired']['_val'])
        kVAr_comp = PFC_compensation(P, pf_actual, pf_desired)
    except Exception as e:
        kVAr_comp = nan
        doc['errors'].append(str(e))
        doc['errors'].append("Failed to calculate phase parameters. Check Inputs")

    kVAr_comp = roundit(kVAr_comp)

    doc['result'].update({'kVAr_comp':{'_val' : str(kVAr_comp)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
