from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from fluids.piping import nearest_pipe
from techlib.mechanical.flare.flarestack  import flareDia, heatRelease, flameLength, vaporFlowrate, tipVelocity, flameDistortion

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    qm = parseFloat(doc['input']['qm']['_val'])
    MW = parseFloat(doc['input']['MW']['_val'])
    T = parseFloat(doc['input']['T']['_val'])
    Z = parseFloat(doc['input']['Z']['_val'])
    LHV = parseFloat(doc['input']['LHV']['_val'])
    p2 = parseFloat(doc['input']['p2']['_val'])
    Uinf = parseFloat(doc['input']['Uinf']['_val'])
    Ma2 = parseFloat(doc['input']['Ma2']['_val'])
    d_basis = doc['input']['d_basis']['_val']
    if (d_basis=='manual'):
        d = parseFloat(doc['input']['d_manual']['_val'])
    else:
        d = flareDia(qm, p2, Ma2, Z, T, MW)

    R = parseFloat(doc['input']['R']['_val'])
    tau = parseFloat(doc['input']['tau']['_val'])
    F = parseFloat(doc['input']['F']['_val'])
    K = parseFloat(doc['input']['K']['_val'])

    '''
    '''
    try:
        Q = heatRelease(qm,LHV)
        L = flameLength(Q)
        q_vap = vaporFlowrate(qm, MW, T)
        Uj = tipVelocity(q_vap, d)
        Uinf_by_Uj = Uinf/Uj
        Sdy_by_L, Sdx_by_L = flameDistortion(Uinf_by_Uj)
        Sdy = Sdy_by_L*L
        Sdx = Sdx_by_L*L
        D =     D = sqrt(tau*F*Q/(4*pi*K))
        R_prime = R - 0.5*Sdx
        H_prime = sqrt(D**2 - R_prime**2)
        H = H_prime - 0.5*Sdy
    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append('Flare Height could not be calculated. Check Inputs')
        d = nan
        Q = nan
        L = nan
        rho = nan
        Uj = nan
        Uinf_by_Uj = nan
        Sdy_by_L = nan
        Sdx_by_L = nan
        Sdy = nan
        Sdx = nan
        R_prime = nan
        H_prime = nan
        H = nan

    doc['result'].update({'d':{'_val' : str(roundit(d)), '_dim':'length'}})
    doc['result'].update({'Q':{'_val' : str(roundit(Q)), '_dim':'power'}})
    doc['result'].update({'L':{'_val' : str(roundit(L)), '_dim':'length'}})
    doc['result'].update({'q_vap':{'_val' : str(roundit(q_vap)), '_dim':'flow'}})
    doc['result'].update({'Uj':{'_val' : str(roundit(Uj)), '_dim':'speed'}})
    doc['result'].update({'Uinf_by_Uj':{'_val' : str(roundit(Uinf_by_Uj))}})
    doc['result'].update({'Sdy_by_L':{'_val' : str(roundit(Sdy_by_L))}})
    doc['result'].update({'Sdx_by_L':{'_val' : str(roundit(Sdx_by_L))}})
    doc['result'].update({'Sdy':{'_val' : str(roundit(Sdy)), '_dim':'length'}})
    doc['result'].update({'Sdx':{'_val' : str(roundit(Sdx)), '_dim':'length'}})
    doc['result'].update({'D':{'_val' : str(roundit(D)), '_dim':'length'}})
    doc['result'].update({'R_prime':{'_val' : str(roundit(R_prime)), '_dim':'length'}})
    doc['result'].update({'H_prime':{'_val' : str(roundit(H_prime)), '_dim':'length'}})
    doc['result'].update({'H':{'_val' : str(roundit(H)), '_dim':'length'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
