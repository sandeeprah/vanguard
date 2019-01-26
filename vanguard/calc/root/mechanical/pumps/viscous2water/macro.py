import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from copy import deepcopy
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.mechanical.cfgpump.pump import viscSel

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    Qvis = float(doc['input']['Qvis']['_val'])
    Hvis = float(doc['input']['Hvis']['_val'])
    viscosity_basis = doc['input']['viscosity_basis']['_val']

    if (viscosity_basis=='kinematic'):
        nu = float(doc['input']['nu']['_val'])
    else:
        mu = float(doc['input']['mu']['_val'])
        rho = float(doc['input']['rho']['_val'])
        nu = dyn2kinVisc(mu, rho)


    try:
        Cq, Ch, Ceta = viscSel(Qvis, Hvis, nu)
        Cq = roundit(Cq)
        Ch = roundit(Ch)
        Ceta = roundit(Ceta)
    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate correction factors. Check Inputs')
        Cq = math.nan
        Ch = math.nan
        Ceta = math.nan



    doc['result'].update({'nu':{'_val':str(nu), '_dim':'kinViscosity'}})
    doc['result'].update({'Cq':{'_val':str(Cq)}})
    doc['result'].update({'Ch':{'_val':str(Ch)}})
    doc['result'].update({'Ceta':{'_val':str(Ceta)}})


    try:
        Qw = roundit(Qvis/Cq)
        doc['result'].update({'Qw':{'_val':str(Qw), '_dim':'flow'}})
    except Exception:
        doc['result'].update({'Qw':{'_val':' ', '_dim':'flow'}})

    try:
        Hw = roundit(Hvis/Ch)
        doc['result'].update({'Hw':{'_val':str(Hw), '_dim':'length'}})
    except Exception:
        doc['result'].update({'Hvis':{'_val':' ', '_dim':'length'}})



    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
