import CoolProp.CoolProp as CP
from fluids.control_valve import size_control_valve_g
from techlib.units import treeUnitConvert, SI_UNITS, unitConvert
from techlib.mathutils import roundit
from fluids.safety_valve import API520_W, API520_Kv, API520_round_size
from techlib.fluids.safety_valve  import API520_A_l_cert, API526_letter, Reynolds
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt

from copy import deepcopy
import math

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    Pset = float(doc['input']['Pset']['_val'])
    Pover = float(doc['input']['Pover']['_val'])
    Psuper = float(doc['input']['Psuper']['_val'])
    Pbuiltup = float(doc['input']['Pbuiltup']['_val'])
    Psuper_is_const = doc['input']['Psuper_is_const']['_val']

    Q = float(doc['input']['Q']['_val'])
    rho = float(doc['input']['rho']['_val'])
    viscosity_basis = doc['input']['viscosity_basis']['_val']

    valve_design = doc['input']['valve_design']['_val']
    rupture_disc = doc['input']['rupture_disc']['_val']
    Kd_basis = doc['input']['Kd_basis']['_val']
    Kw_basis = doc['input']['Kw_basis']['_val']
    Kc_basis = doc['input']['Kc_basis']['_val']


    if (viscosity_basis=='Dynamic'):
        mu = float(doc['input']['mu']['_val'])
    if (viscosity_basis=='Kinematic'):
        nu = float(doc['input']['nu']['_val'])
        mu = kin2dynVisc(nu, rho)
    if (viscosity_basis=='SSU'):
        ssu = float(doc['input']['ssu']['_val'])
        nu_cst = SSU2cSt(ssu)
        nu = unitConvert(nu_cst, 'kinViscosity', 'cSt', 'm2/s')
        mu = kin2dynVisc(nu, rho)


    Patm = 101325 # atmospheric pressure
    P = Pset + (Pover/100)*Pset + Patm # relieving pressure
    Pback = Psuper + Pbuiltup

    if (Psuper_is_const == 'Yes'):
        Psuper_variable = 0
    else:
        Psuper_variable = Psuper

    valve_design_remark =""

    if (valve_design=='Conventional'):
        Puncompensated = Psuper_variable + Pbuiltup
        allowable_overpressure = Pset*(Pover/100)
        if (Puncompensated > allowable_overpressure):
            valve_design_remark = 'Not acceptable. Uncompensated backpressure exceeds allowable overpressure'
        else:
            if (Pback > allowable_overpressure):
                valve_design_remark ='Acceptable, subject to compensation of constant superimposed back pressure'
            else:
                valve_design_remark ='Acceptable'

    if (valve_design=='Balanced'):
        Pback_max = 0.5*Pset
        if (Pback > Pback_max):
            valve_design_remark ='Not Acceptable. Total backpressure exceeds 50% of set pressure'
        else:
            valve_design_remark ='Acceptable'

    if (valve_design=='Pilot-Operated'):
        valve_design_remark='Acceptable'



    if (Kd_basis=='Manual'):
        Kd = float(doc['input']['Kd_manual']['_val'])
    else:
        Kd = 0.65


    if (rupture_disc=='No'):
        Kc = 1
    else:
        if (Kc_basis=='Manual'):
            Kc = float(doc['input']['Kc_manual']['_val'])
        else:
            Kc = 0.9

    G = rho/1000
    Pb = Pback + Patm
    Pset_abs = Pset + Patm

    if (valve_design=='Balanced'):
        if (Kw_basis=='Manual'):
            Kw = float(doc['input']['Kw_manual']['_val'])
        else:
            try:
                Kw = API520_W(Pset_abs, Pb)
                Kw = roundit(Kw)
            except Exception as e:
                Kw = math.nan
                doc["errors"].append(str(e))
                doc["errors"].append("Failed to calculated, backpressure. Provide Manual input using manufacturer data")
    else:
        Kw = 1


    Kv = 1

    try:
        while True:
            A =  API520_A_l_cert(Q=Q, G=G, P=P, Pb=Pb, Kd=Kd, Kw=Kw, Kc=Kc, Kv=Kv)
            print(A)
            A_sel = API520_round_size(A)
            R = Reynolds(Q, G, mu, A_sel)
            Kv = API520_Kv(R)
            Kv = roundit(Kv)
            A = A/Kv
            if (A_sel >= A):
                break

        A_letter = API526_letter(A_sel)
    except Exception:
        A = math.nan
        A_sel = math.nan
        Kv = math.nan
        R = math.nan
        A_letter = ""
        doc['errors'].append("Failed to calculate discharge Area (A). Check Inputs")


    doc['result'].update({'valve_design_remark':{'_val':str(valve_design_remark)}})
    doc['result'].update({'R':{'_val':str(R)}})
    doc['result'].update({'Kd':{'_val':str(Kd)}})
    doc['result'].update({'Kw':{'_val':str(Kw)}})
    doc['result'].update({'Kc':{'_val':str(Kc)}})
    doc['result'].update({'Kv':{'_val':str(Kv)}})
    doc['result'].update({'A':{'_val':str(A), '_dim':'area'}})
    doc['result'].update({'A_sel':{'_val':str(A_sel), '_dim':'area'}})
    doc['result'].update({'A_letter':{'_val':str(A_letter)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
