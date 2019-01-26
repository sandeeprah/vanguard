import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS, unitConvert
from techlib.mathutils import roundit
from copy import deepcopy
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt, cSt2SSU

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    convert = doc['input']['convert']['_val']

    if (convert=='nu2mu'):
        nu = float(doc['input']['nu']['_val'])
        rho = float(doc['input']['rho']['_val'])
        mu = kin2dynVisc(nu, rho)
        ssu = ""
    elif (convert=='nu2ssu'):
        nu = float(doc['input']['nu']['_val'])
        nu_cSt = unitConvert(nu, 'kinViscosity', 'm2/s', 'cSt')
        ssu = cSt2SSU(nu_cSt)
        mu = ""
    elif(convert=='mu2nu'):
        mu = float(doc['input']['mu']['_val'])
        rho = float(doc['input']['rho']['_val'])
        nu = dyn2kinVisc(mu, rho)
        nu_cSt = unitConvert(nu, 'kinViscosity', 'm2/s', 'cSt')
        ssu = cSt2SSU(nu_cSt)
    elif(convert=='mu2ssu'):
        mu = float(doc['input']['mu']['_val'])
        rho = float(doc['input']['rho']['_val'])
        nu = dyn2kinVisc(mu,rho)
        nu_cSt = unitConvert(nu, 'kinViscosity', 'm2/s', 'cSt')
        ssu = cSt2SSU(nu_cSt)
    elif(convert=='ssu2nu'):
        ssu = float(doc['input']['ssu']['_val'])
        nu_cSt = SSU2cSt(ssu)
        nu = unitConvert(nu_cSt, 'kinViscosity',  'cSt', 'm2/s')
        mu=""
    elif(convert=='ssu2mu'):
        ssu = float(doc['input']['ssu']['_val'])
        rho = float(doc['input']['rho']['_val'])
        nu_cSt = SSU2cSt(ssu)
        nu = unitConvert(nu_cSt, 'kinViscosity',  'cSt', 'm2/s')
        mu = kin2dynVisc(nu, rho)

    nu = roundit(nu)
    mu = roundit(mu)
    ssu = roundit(ssu)

    doc['result'].update({'nu':{'_val':str(nu), '_dim':'kinViscosity'}})
    doc['result'].update({'mu':{'_val':str(mu), '_dim':'dynViscosity'}})
    doc['result'].update({'ssu':{'_val':str(ssu)}})


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
