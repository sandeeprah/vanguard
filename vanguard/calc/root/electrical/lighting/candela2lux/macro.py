import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from copy import deepcopy
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.electrical.lighting import candela2lux, lux2candela

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    convert = doc['input']['convert']['_val']
    distance = float(doc['input']['distance']['_val'])

    if (convert=='cd2lux'):
        candela = float(doc['input']['candela']['_val'])
        lux = candela2lux(candela, distance)
        lux = roundit(lux)
        doc['result'].update({'lux':{'_val':str(lux)}})
    else:
        lux = float(doc['input']['lux']['_val'])
        candela = lux2candela(lux, distance)
        candela = roundit(candela)
        doc['result'].update({'candela':{'_val':str(candela)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
