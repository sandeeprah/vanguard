import math
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from fluids.piping import nearest_pipe
from techlib.mechanical.piping.pipe import t_pressure, getY, getS, getE

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    calculation_option = doc['input']['calculation_option']['_val']

    '''

    '''

    try:
        if (calculation_option=='NPS'):
            NPS = parseFloat(doc['input']['NPS']['_val'])
            Schedule = doc['input']['Schedule']['_val']
            NPS, d, D, tn = nearest_pipe(NPS = NPS, schedule = Schedule)
        if (calculation_option=='d'):
            d = parseFloat(doc['input']['d']['_val'])
            Schedule = doc['input']['Schedule']['_val']
            NPS, d, D, tn = nearest_pipe(Di = d, schedule = Schedule)
        if (calculation_option=='D'):
            D = parseFloat(doc['input']['D']['_val'])
            Schedule = doc['input']['Schedule']['_val']
            NPS, d, D, tn = nearest_pipe(Do = D, schedule = Schedule)
    except Exception as e:
        doc['errors'].append(str(e))
        NPS = math.nan
        d = math.nan
        D = math.nan
        tn = math.nan

    P = parseFloat(doc['input']['P']['_val'])
    Tdesign = parseFloat(doc['input']['Tdesign']['_val'])
    materialSpec = doc['input']['materialSpec']['_val']
    weldType = doc['input']['weldType']['_val']
    W = parseFloat(doc['input']['W']['_val'])
    ca = parseFloat(doc['input']['ca']['_val'])
    h = parseFloat(doc['input']['h']['_val'])
    ut = parseFloat(doc['input']['ut']['_val'])

    t_ut = tn*ut/100 # thickness lost due to undertolerance
    T = tn - t_ut  # guaranteed thickness available as a minimum


    c = ca + h  # get sum total of all corrosion and threading allowance


    S = getS(materialSpec, Tdesign)
    Y = getY(materialSpec, Tdesign)
    E = getE(weldType)
    t = t_pressure(P,D,S,E,W,Y)  # pressure design thickness
    tm = t + c  # min required thickness
    if (T >= tm):
        acceptability = "OK"
    else:
        acceptability = "Not OK"

    doc['result'].update({'NPS':{'_val' : str(roundit(NPS))}})
    doc['result'].update({'d':{'_val' : str(roundit(d)), '_dim':'length'}})
    doc['result'].update({'D':{'_val' : str(roundit(D)), '_dim':'length'}})
    doc['result'].update({'tn':{'_val' : str(roundit(tn)), '_dim':'length'}})
    doc['result'].update({'t_ut':{'_val' : str(roundit(t_ut)), '_dim':'length'}})
    doc['result'].update({'T':{'_val' : str(roundit(T)), '_dim':'length'}})
    doc['result'].update({'S':{'_val' : str(roundit(S)), '_dim':'pressure'}})
    doc['result'].update({'Y':{'_val' : str(roundit(Y))}})
    doc['result'].update({'E':{'_val' : str(E)}})
    doc['result'].update({'t':{'_val' : str(roundit(t)), '_dim':'length'}})
    doc['result'].update({'c':{'_val' : str(roundit(c)), '_dim':'length'}})
    doc['result'].update({'tm':{'_val' : str(roundit(tm)), '_dim':'length'}})
    doc['result'].update({'acceptability':{'_val' : acceptability}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
