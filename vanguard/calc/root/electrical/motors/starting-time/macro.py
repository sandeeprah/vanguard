from math import *
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy
from techlib.mathutils import roundit
from techlib.electrical.motor.core import motor_starting_time

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    try:
        Nr = float(doc['input']['Nr']['_val'])
        Jm = float(doc['input']['Jm']['_val'])
        Cs = float(doc['input']['Cs']['_val'])
        Cm = float(doc['input']['Cm']['_val'])
        load_type = doc['input']['load_type']['_val']
        Cl = float(doc['input']['Cl']['_val'])
        Jl = float(doc['input']['Jl']['_val'])

        Tacc = motor_starting_time(Nr,Jm,Jl,Cs,Cm,Cl,load_type)

    except Exception as e:
        Tacc = nan
        doc['errors'].append(str(e))
        doc['errors'].append("Failed to calculate phase parameters. Check Inputs")

    Tacc = roundit(Tacc)

    doc['result'].update({'Tacc':{'_val' : str(Tacc)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
