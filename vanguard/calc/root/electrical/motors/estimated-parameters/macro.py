from math import *
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy
from techlib.mathutils import roundit
from techlib.electrical.motor.core import motor_params, standard_iec_motor

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    try:
        motor_power = float(doc['input']['motor_power']['_val'])
        poles = float(doc['input']['poles']['_val'])
        motor_rating = standard_iec_motor(motor_power)
        motor_rating_kW = motor_rating/1000
        mtr = motor_params(motor_rating_kW, poles)
        Frame_Size = mtr['Frame_Size']
        Speed = mtr['Speed']
        eta_full = mtr['eta_full']
        eta_three_fourth = mtr['eta_three_fourth']
        eta_half = mtr['eta_half']
        pf = mtr['pf']
        In = mtr['In']
        Is_by_In = mtr['Is_by_In']
        Is = roundit(Is_by_In*In)
        Tn = mtr['Tn']
        Ti_by_Tn = mtr['Ti_by_Tn']
        Ti = roundit(Ti_by_Tn*Tn)
        Tb_by_Tn = mtr['Tb_by_Tn']
        Tb = roundit(Tb_by_Tn*Tn)

        J = mtr['J']
        weight = mtr['weight']

    except Exception as e:
        motor_rating = nan
        mtr = {}
        Speed = nan
        eta_full = nan
        eta_three_fourth = nan
        eta_half = nan
        pf = nan
        In = nan
        Is_by_In = nan
        Is = nan
        Tn = nan
        Ti_by_Tn = nan
        Ti = nan
        Tb_by_Tn = nan
        Tb = nan
        J = nan
        weight = nan

        doc['errors'].append(str(e))
        doc['errors'].append("Failed to estimate motor parameters. Check Inputs")


    doc['result'].update({'motor_rating':{'_val' : str(motor_rating), '_dim':'power'}})
    doc['result'].update({'Speed':{'_val' : str(Speed)}})
    doc['result'].update({'eta_full':{'_val' : str(eta_full)}})
    doc['result'].update({'eta_three_fourth':{'_val' : str(eta_three_fourth)}})
    doc['result'].update({'eta_half':{'_val' : str(eta_half)}})
    doc['result'].update({'pf':{'_val' : str(pf)}})
    doc['result'].update({'In':{'_val' : str(In)}})
    doc['result'].update({'Is':{'_val' : str(Is)}})
    doc['result'].update({'Is_by_In':{'_val' : str(Is_by_In)}})
    doc['result'].update({'Tn':{'_val' : str(Tn)}})
    doc['result'].update({'Ti':{'_val' : str(Ti)}})
    doc['result'].update({'Ti_by_Tn':{'_val' : str(Ti_by_Tn)}})
    doc['result'].update({'Tb':{'_val' : str(Tb)}})
    doc['result'].update({'Tb_by_Tn':{'_val' : str(Tb_by_Tn)}})
    doc['result'].update({'J':{'_val' : str(J)}})
    doc['result'].update({'weight':{'_val' : str(weight)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
