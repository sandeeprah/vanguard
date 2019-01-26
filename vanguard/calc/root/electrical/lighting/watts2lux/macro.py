import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from copy import deepcopy
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.electrical.lighting import watts2lumens, lumens2watts, lumens2lux, lux2lumens

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    convert = doc['input']['convert']['_val']
    area_basis = doc['input']['area_basis']['_val']

    luminous_efficacy = float(doc['input']['luminous_efficacy']['_val'])

    if (convert=='watts2lux'):
        watts = float(doc['input']['watts']['_val'])
        lumens = watts2lumens(watts, luminous_efficacy)
        lumens = roundit(lumens)

        if (area_basis=='radius'):
            radius = float(doc['input']['radius']['_val'])
            lux = lumens2lux(lumens, radius=radius)
        else:
            area = float(doc['input']['area']['_val'])
            lux = lumens2lux(lumens, area=area)

        lux = roundit(lux)
        doc['result'].update({'lux':{'_val':str(lux)}})
    else:
        lux = float(doc['input']['lux']['_val'])
        if (area_basis=='radius'):
            radius = float(doc['input']['radius']['_val'])
            lumens = lux2lumens(lux, radius=radius)
        else:
            area = float(doc['input']['area']['_val'])
            lumens = lux2lumens(lux, area=area)

        watts = lumens2watts(lumens, luminous_efficacy)
        watts = roundit(watts)
        doc['result'].update({'watts':{'_val':str(watts)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
