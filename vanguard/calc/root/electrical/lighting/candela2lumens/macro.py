import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from copy import deepcopy
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.electrical.lighting import candela2lumens, lumens2candela

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    convert = doc['input']['convert']['_val']
    apex_angle = float(doc['input']['apex_angle']['_val'])

    if (convert=='cd2lm'):
        candela = float(doc['input']['candela']['_val'])
        lumens = candela2lumens(candela, apex_angle)
        lumens = roundit(lumens)
        doc['result'].update({'lumens':{'_val':str(lumens)}})
    else:
        lumens = float(doc['input']['lumens']['_val'])
        candela = lumens2candela(lumens, apex_angle)
        candela = roundit(candela)
        doc['result'].update({'candela':{'_val':str(candela)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
