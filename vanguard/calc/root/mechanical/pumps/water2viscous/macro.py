import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from copy import deepcopy
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.mechanical.cfgpump.pump import viscCorr

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    Qbep = float(doc['input']['Qbep']['_val'])
    Hbep = float(doc['input']['Hbep']['_val'])
    speed = float(doc['input']['speed']['_val'])
    viscosity_basis = doc['input']['viscosity_basis']['_val']

    if (viscosity_basis=='kinematic'):
        nu = float(doc['input']['nu']['_val'])
    else:
        mu = float(doc['input']['mu']['_val'])
        rho = float(doc['input']['rho']['_val'])
        nu = dyn2kinVisc(mu, rho)


    Q = float(doc['input']['Q']['_val'])

    try:
        Qratio = Q/Qbep
        Cq, Ch, Ceta = viscCorr(Qbep, Hbep, nu, speed, Qratio)
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
        Qvis = roundit(Q*Cq)
        doc['result'].update({'Qvis':{'_val':str(Qvis), '_dim':'flow'}})
    except Exception:
        doc['result'].update({'Qvis':{'_val':' ', '_dim':'flow'}})

    try:
        H = float(doc['input']['H']['_val'])
        Hvis = roundit(H*Ch)
        doc['result'].update({'Hvis':{'_val':str(Hvis), '_dim':'length'}})
    except Exception:
        doc['result'].update({'Hvis':{'_val':' ', '_dim':'length'}})

    try:
        eta = float(doc['input']['eta']['_val'])
        etavis = roundit(eta*Ceta)
        doc['result'].update({'etavis':{'_val':str(etavis)}})
    except Exception:
        doc['result'].update({'etavis':{'_val':' '}})






    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
