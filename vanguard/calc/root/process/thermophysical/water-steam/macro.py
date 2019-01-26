import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]


    state = doc['input']['state']['_val']

    try:
        if (state=='Saturated_P'):
            P = float(doc['input']['P']['_val'])
            Q = float(doc['input']['Q']['_val'])
            phase = CP.PhaseSI('P', P, 'Q', Q, 'Water')
            Tsat = round(CP.PropsSI('T','P', P, 'Q', Q, 'Water'),1)
            rho = round(CP.PropsSI('D','P', P, 'Q', Q, 'Water'),4)
            v = round(1/rho,4)
            h = round(CP.PropsSI('H','P', P, 'Q', Q, 'Water'),1)
            u = round(CP.PropsSI('U','P', P, 'Q', Q, 'Water'),1)
            s = round(CP.PropsSI('S','P', P, 'Q', Q, 'Water'),1)
            doc['result'].update({'Psat':{'_val' : '', '_dim':'pressure'}})
            doc['result'].update({'Tsat':{'_val' : str(Tsat), '_dim':'temperature'}})

        if (state=='Saturated_T'):
            T = float(doc['input']['T']['_val'])
            Q = float(doc['input']['Q']['_val'])
            phase = CP.PhaseSI('T', T, 'Q', Q, 'Water')
            Psat = round(CP.PropsSI('P','T', T, 'Q', Q, 'Water'),1)
            rho = round(CP.PropsSI('D','T', T, 'Q', Q, 'Water'),4)
            v = round(1/rho,4)
            h = round(CP.PropsSI('H','T', T, 'Q', Q, 'Water'),1)
            u = round(CP.PropsSI('U','T', T, 'Q', Q, 'Water'),1)
            s = round(CP.PropsSI('S','T', T, 'Q', Q, 'Water'),1)
            doc['result'].update({'Psat':{'_val' : str(Psat), '_dim':'pressure'}})
            doc['result'].update({'Tsat':{'_val' : '', '_dim':'temperature'}})

        if (state=='Superheated_or_Compressed'):
            T = float(doc['input']['T']['_val'])
            P = float(doc['input']['P']['_val'])
            phase = CP.PhaseSI('T', T, 'P', P, 'Water')
            rho = round(CP.PropsSI('D','T', T, 'P', P, 'Water'),4)
            v = round(1/rho,1)
            h = round(CP.PropsSI('H','T', T, 'P', P, 'Water'),1)
            u = round(CP.PropsSI('U','T', T, 'P', P, 'Water'),1)
            s = round(CP.PropsSI('S','T', T, 'P', P, 'Water'),1)
            doc['result'].update({'Psat':{'_val' : '', '_dim':'pressure'}})
            doc['result'].update({'Tsat':{'_val' : '', '_dim':'temperature'}})
    except Exception as e:
        raise e
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate Water/Steam Properties. Check Inputs')
        phase = ""
        Psat = math.nan
        Tsat = math.nan
        rho = math.nan
        v = math.nan
        h = math.nan
        u = math.nan
        s = math.nan


    doc['result'].update({'phase':{'_val' : str(phase)}})
    doc['result'].update({'rho':{'_val' : str(rho), '_dim':'density'}})
    doc['result'].update({'v':{'_val' : str(v), '_dim':'specificVolume'}})
    doc['result'].update({'h':{'_val' : str(h), '_dim':'specificEnergy'}})
    doc['result'].update({'u':{'_val' : str(u), '_dim':'specificEnergy'}})
    doc['result'].update({'s':{'_val' : str(s), '_dim':'specificHeat'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
