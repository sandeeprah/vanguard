from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.fluids import orifice as orf

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    Pi = parseFloat(doc['input']['Pi']['_val'])
    Pe = parseFloat(doc['input']['Pe']['_val'])
    Ti = parseFloat(doc['input']['Ti']['_val'])
    MW = parseFloat(doc['input']['MW']['_val'])
    k = parseFloat(doc['input']['k']['_val'])
    A = parseFloat(doc['input']['A']['_val'])
    Cd = parseFloat(doc['input']['Cd']['_val'])


    r = Pe/Pi
    f = k/(k-1)

    rho0 = orf.density(Pi,Ti,MW)
    v, G, isChoked = orf.mflow_reservoir_orifice(Pi, Ti, Pe, MW, k, A, Cd)
    Q = A*v
    doc['result'].update({'v':{'_val' : str(roundit(v)), '_dim':'speed'}})
    doc['result'].update({'Q':{'_val' : str(roundit(Q)), '_dim':'flow'}})
    doc['result'].update({'G':{'_val' : str(roundit(G)), '_dim':'massflow'}})
    doc['result'].update({'isChoked':{'_val' : isChoked}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
