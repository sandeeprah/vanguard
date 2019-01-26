import math
import CoolProp.CoolProp as CP
from fluids.control_valve import size_control_valve_g
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit

from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    T = float(doc['input']['T']['_val'])
    MW = float(doc['input']['MW']['_val'])
    mu = float(doc['input']['mu']['_val'])
    gamma = float(doc['input']['gamma']['_val'])
    Z = float(doc['input']['Z']['_val'])
    P1 = float(doc['input']['P1']['_val'])
    P2 = float(doc['input']['P2']['_val'])
    Q = float(doc['input']['Q']['_val'])
    D1 = float(doc['input']['D1']['_val'])
    D2 = float(doc['input']['D2']['_val'])
    d = float(doc['input']['d']['_val'])
    FL = float(doc['input']['FL']['_val'])
    Fd = float(doc['input']['Fd']['_val'])
    xT = float(doc['input']['xT']['_val'])

    MW_ = MW*1000
    try:
        Cmetric = size_control_valve_g(T, MW_, mu, gamma, Z, P1, P2, Q, D1, D2, d, FL, Fd, xT)
    except Exception:
        Cmetric = math.nan

    Cmetric = roundit(Cmetric)
    doc['result'].update({'Cmetric':{'_val' : str(Cmetric)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']


    return True
