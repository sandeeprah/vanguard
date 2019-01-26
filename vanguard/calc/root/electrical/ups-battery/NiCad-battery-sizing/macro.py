from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
import pandas as pd
from collections import OrderedDict

from techlib.electrical.ups.utils import getAmpDataKnown, getAmpDataRandom, selectCellAh, getCellSize

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    Vmin = parseFloat(doc['input']['Vmin']['_val'])
    Vmax = parseFloat(doc['input']['Vmax']['_val'])
    Vnominal = parseFloat(doc['input']['Vnominal']['_val'])
    loads_known = doc['input']['loads_known']
    loads_random = doc['input']['loads_random']
    Vc_max = parseFloat(doc['input']['Vc_max']['_val'])
    Tmin = parseFloat(doc['input']['Tmin']['_val'])
    Tmax = parseFloat(doc['input']['Tmax']['_val'])
    Tnominal = parseFloat(doc['input']['Tnominal']['_val'])
    design_margin = parseFloat(doc['input']['design_margin']['_val'])
    aging_factor  = parseFloat(doc['input']['aging_factor']['_val'])
    cell_range = doc['input']['cell_range']['_val']
    Ncell_basis = doc['input']['Ncell_basis']['_val']

    Veod_max = 1.14
    Veod_min = 1.0
    Ncell_max = floor(Vmax/Vc_max)
    Ncell_min = ceil(Vmin/Veod_max)

    if (Ncell_basis=='manual'):
        Ncell = parseFloat(doc['input']['Ncell_manual']['_val'])
    else:
        Ncell = Ncell_max


    Vmax_attained = Vc_max*Ncell
    Veod = Vmin/Ncell
    if (Veod < Veod_min):
        Veod = Veod_min


    if (Ncell_min > Ncell_max):
        doc['errors'].append('The system minimum voltage is too high for making economic selection. Check if the same can be lowered. Also try lowering the maximum charging voltage if possible.')

    if (Ncell > Ncell_max):
        doc['errors'].append('No. of cells selected above max. Please choose withing range.')

    if (Ncell < Ncell_min):
        doc['errors'].append('No. of cells selected below min. Please choose withing range.')

    Vmin_attained = Veod*Ncell
    amp_data_known  = getAmpDataKnown(loads_known, Vmin)
    print(amp_data_known)
    amp_data_random = getAmpDataRandom(loads_random, Vmin)
    try:
        Fs_max, Fs_random, Fs_uncorrected, Fs_corrected, cell_selected, strings = getCellSize(amp_data_known, amp_data_random,  cell_range, Veod, Tmin, design_margin, aging_factor)
    except Exception as e:
        doc['errors'].append(str(e))
        Fs_max = nan
        Fs_random = nan
        Fs_uncorrected = nan
        Fs_corrected = nan
        cell_selected=""
        strings = nan

    doc['result'].update({'Ncell_max':{'_val' : str(int(Ncell_max))}})
    doc['result'].update({'Ncell_min':{'_val' : str(int(Ncell_min))}})
    doc['result'].update({'Ncell':{'_val' : str(int(Ncell))}})
    doc['result'].update({'Veod':{'_val' : str(roundit(Veod))}})
    doc['result'].update({'Vmax_attained':{'_val' : str(roundit(Vmax_attained))}})
    doc['result'].update({'Vmin_attained':{'_val' : str(roundit(Vmin_attained))}})

    doc['result'].update({'Fs_max':{'_val' : str(roundit(Fs_max))}})
    doc['result'].update({'Fs_random':{'_val' : str(roundit(Fs_random))}})
    doc['result'].update({'Fs_uncorrected':{'_val' : str(roundit(Fs_uncorrected))}})
    doc['result'].update({'Fs_corrected':{'_val' : str(roundit(Fs_corrected))}})
    doc['result'].update({'cell_selected':{'_val' : cell_selected }})
    doc['result'].update({'strings':{'_val' : str(strings) }})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
