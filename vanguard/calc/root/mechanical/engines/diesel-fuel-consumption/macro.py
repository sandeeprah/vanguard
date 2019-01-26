import CoolProp.CoolProp as CP
from fluids.control_valve import size_control_valve_g
from techlib.units import treeUnitConvert, SI_UNITS, unitConvert
from techlib.mathutils import roundit
from fluids.safety_valve import API520_B, API520_N, API520_SH, API520_round_size, API520_A_steam
from techlib.fluids.safety_valve  import API520_A_l_cert, API526_letter,  Reynolds
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.thermochem.psychrometry import Pws, humidityratio

from copy import deepcopy
import math

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    Prated = float(doc['input']['Prated']['_val'])
    print(Prated)
    Fuel_rate_specific = float(doc['input']['Fuel_rate_specific']['_val'])
    print(Fuel_rate_specific)
    Fuel_flow_rate = Fuel_rate_specific*Prated
    print(Fuel_flow_rate)
#    Fuel_flow_rate = roundit(Fuel_flow_rate)
    #Fuel_flow_rate = 1
    doc['result'].update({'Fuel_flow_rate':{'_val':str(Fuel_flow_rate), '_dim':'flow'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True



def humidity_correction(x):
    x1 = 0.0063256
    y1 = 1.00
    x2 = 0.03
    y2 = 0.997
    y = y1 + (y2-y1)*(x-x1)/(x2-x1)
    return y
