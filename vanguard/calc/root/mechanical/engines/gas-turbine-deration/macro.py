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

    Piso = float(doc['input']['Piso']['_val'])
    Tsite = float(doc['input']['Tsite']['_val'])
    Hsite = float(doc['input']['Hsite']['_val'])
    RHsite = float(doc['input']['RHsite']['_val'])
    delPinlet = float(doc['input']['delPinlet']['_val'])
    delPoutlet = float(doc['input']['delPoutlet']['_val'])
    fueltype = doc['input']['fueltype']['_val']


    # 0.4% power reduction for every 1 deg Fahrenheit temp rise above 59 deg Fahrenheit
    Tiso = 288.15
    deltaT = Tsite - Tiso
    Ltemperature = 1 - 0.004*deltaT*9/5
    Ltemperature = roundit(Ltemperature)
    Lhumidity = 1

    # 3.3 % power reduction for 1000 ft elevation rise above sea level
    Laltitude = 1 - (Hsite*3.2808/1000)*0.033
    Laltitude = roundit(Laltitude)

    P_atm = 101325
    x =  humidityratio(Tsite, P_atm, RHsite)
    Lhumidity = humidity_correction(x)
    Lhumidity = roundit(Lhumidity)

    # 0.5% reduction in power due to 1 inch Hg.
    #delPinlet
    Linlet =  1 - (delPinlet*39.3701*0.5)/100
    Linlet = roundit(Linlet)
    Loutlet = 1 - (delPoutlet*39.3701*0.15)/100
    Loutlet = roundit(Loutlet)
    if (fueltype=='distillate'):
        Lfuel = 1 - 0.025
    else:
        Lfuel = 1.0

    Ltotal = Ltemperature*Lhumidity*Laltitude*Linlet*Loutlet*Lfuel
    Ltotal = roundit(Ltotal)

    Psite = Piso*Ltotal


    doc['result'].update({'Psite':{'_val':str(Psite), '_dim':'power'}})
    doc['result'].update({'Ltemperature':{'_val':str(Ltemperature)}})
    doc['result'].update({'Lhumidity':{'_val':str(Lhumidity)}})
    doc['result'].update({'Laltitude':{'_val':str(Laltitude)}})
    doc['result'].update({'Linlet':{'_val':str(Linlet)}})
    doc['result'].update({'Loutlet':{'_val':str(Loutlet)}})
    doc['result'].update({'Lfuel':{'_val':str(Lfuel)}})
    doc['result'].update({'Ltotal':{'_val':str(Ltotal)}})


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
