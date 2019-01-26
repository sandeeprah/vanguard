from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.process import storage as st

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    Pu = parseFloat(doc['input']['Pu']['_val'])
    Pl = parseFloat(doc['input']['Pl']['_val'])
    Qout = parseFloat(doc['input']['Qout']['_val'])
    Tmax = parseFloat(doc['input']['Tmax']['_val'])
    margin = parseFloat(doc['input']['margin']['_val'])

    sizing_basis = doc['input']['sizing_basis']['_val']
    if (sizing_basis=='buffer_time'):
        t = parseFloat(doc['input']['t']['_val'])
        V = st.receiverVolumeHoldUp(Qout=Qout,t=t,Pu=Pu, Pl=Pl, Tmax=Tmax, margin=margin)
    elif(sizing_basis=='switching_frequency'):
        Qin = parseFloat(doc['input']['Qin']['_val'])
        fs = parseFloat(doc['input']['fs']['_val'])
        chi = (Qout/Qin)
        Qout_worst = 0.5*Qin
        V = st.receiverVolumeSwitching(fs=fs,Qin=Qin,Qout=Qout,Pu=Pu,Pl=Pl,Tmax=Tmax,margin=margin)
        Vrec = st.receiverVolumeSwitching(fs=fs,Qin=Qin,Qout=Qout_worst,Pu=Pu,Pl=Pl,Tmax=Tmax,margin=margin)
        doc['result'].update({'chi':{'_val' : str(roundit(chi))}})
        doc['result'].update({'Vrec':{'_val' : str(roundit(Vrec)), '_dim':'volume'}})
    else:
        doc[errors].append('Invalid value for "Sizing Basis"')

    doc['result'].update({'V':{'_val' : str(roundit(V)), '_dim':'volume'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
