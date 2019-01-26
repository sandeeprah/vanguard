from math import *
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy
from techlib.mathutils import roundit
from techlib.electrical.phase import phase_parameters

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    solve_using = doc['input']['solve_using']['_val']

    VLL = float(doc['input']['VLL']['_val'])
    pf = float(doc['input']['pf']['_val'])

    I = nan
    kW = nan
    kVA = nan
    kVAr = nan

    try:
        if (solve_using == 'current'):
            I = float(doc['input']['I']['_val'])
            I, kW, kVA, kVAr = phase_parameters(VLL, pf, I=I)
        elif(solve_using == 'active_power'):
            kW = float(doc['input']['kW']['_val'])
            I, kW, kVA, kVAr = phase_parameters(VLL, pf, kW=kW)
        elif(solve_using == 'apparent_power'):
            kVA = float(doc['input']['kVA']['_val'])
            I, kW, kVA, kVAr = phase_parameters(VLL, pf, kVA=kVA)
        elif(solve_using == 'reactive_power'):
            kVAr = float(doc['input']['kVAr']['_val'])
            I, kW, kVA, kVAr = phase_parameters(VLL, pf, kVAr=kVAr)
        else:
            raise Exception("Invalid Option for Solving")

    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append("Failed to calculate phase parameters. Check Inputs")


    I = roundit(I)
    kW = roundit(kW)
    kVA = roundit(kVA)
    kVAr = roundit(kVAr)

    doc['result'].update({'I':{'_val' : str(I)}})
    doc['result'].update({'kW':{'_val' : str(kW)}})
    doc['result'].update({'kVA':{'_val' : str(kVA)}})
    doc['result'].update({'kVAr':{'_val' : str(kVAr)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
