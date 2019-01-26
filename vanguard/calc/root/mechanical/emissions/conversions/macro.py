from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from fluids.piping import nearest_pipe
from techlib.mechanical.heater.combustion  import gasfuelProperties,airMoistureContent,wetAirRequired, excessAir, excessAir_pc
from techlib.mechanical.heater.combustion  import flueMassicHeatContent, H2OformedEAcorrected, getEnthalphy, radiationLoss
from techlib.mechanical.heater.combustion  import enthalpySteam, netThermalEfficiency, fuelEfficiency, grossThermalEfficiency, getHHV

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    specie = doc['input']['specie']['_val']
    concentration_measured = parseFloat(doc['input']['concentration_measured']['_val'])
    from_units = doc['input']['from_units']['_val']
    sampling_basis = doc['input']['sampling_basis']['_val']
    oxygen_correction = doc['input']['oxygen_correction']['_val']
    to_units = doc['input']['to_units']['_val']


    # Let base units be mg/Nm3. Convert from from_units to base unit and then from base_unit to to_unit
    if (specie=='NOx'):
        MW = 46.0
    elif (specie=='SOx'):
        MW = 64.1
    elif (specie=='CO'):
        MW = 28.01
    elif (specie=='Other'):
        MW = parseFloat(doc['input']['MW']['_val'])*1000
    else:
        raise Exception('Unknown specie of pollutant. Molecular weight not found')

    Vmolar  = 22.41 #volume occupied by one mole of gas at NTP conditions
    Ku = MW/Vmolar

    if (from_units != to_units):
        if (from_units=='ppmv'):
            concentration_base = concentration_measured*Ku
        if (from_units=='mg/Nm3'):
            concentration_base = concentration_measured
        if (from_units=='mg/Sm3'):
            Ts = parseFloat(doc['input']['Ts']['_val'])
            Ps = parseFloat(doc['input']['Ps']['_val'])
            Tn = 273.15
            Pn = 101325
            Ft = Ts/Tn
            Fp = Pn/Ps
            concentration_base = concentration_measured*Ft*Fp

        if (to_units=='ppmv'):
            concentration_wet = concentration_base/Ku
        if (to_units=='mg/Nm3'):
            concentration_wet = concentration_base
        if (to_units=='mg/Sm3'):
            Ts = parseFloat(doc['input']['Ts']['_val'])
            Ps = parseFloat(doc['input']['Ps']['_val'])
            Tn = 273.15
            Pn = 101325
            Ft = Tn/Ts
            Fp = Ps/Pn
            concentration_wet = concentration_base*Ft*Fp
    else:
        concentration_wet = concentration_measured


    # check if moisture correction is to be applied
    if (sampling_basis=='wet'):
        H2O_measured = parseFloat(doc['input']['H2O_measured']['_val'])
        Fm = 100/(100-H2O_measured)
    else:
        Fm = 1


    concentration_dry = concentration_wet*Fm


    # check if oxygen correction is to be applied
    try:
        if (oxygen_correction=='yes'):
            O2_measured = parseFloat(doc['input']['O2_measured']['_val'])
            O2_reference = parseFloat(doc['input']['O2_reference']['_val'])
            O2_measured_dry = O2_measured*Fm
            Fo = (20.9 - O2_reference)/(20.9 - O2_measured_dry)
        else:
            O2_measured_dry = nan
            Fo = 1
    except Exception as e:
        Fo = nan
        O2_measured_dry = nan


    concentration_dry_corrected = concentration_dry*Fo

    doc['result'].update({'concentration_wet':{'_val' : str(roundit(concentration_wet))}})
    doc['result'].update({'units':{'_val' : to_units}})
    doc['result'].update({'Fm':{'_val' : str(roundit(Fm))}})
    doc['result'].update({'concentration_dry':{'_val' : str(roundit(concentration_dry))}})
    doc['result'].update({'O2_measured_dry':{'_val' : str(roundit(O2_measured_dry))}})
    doc['result'].update({'Fo':{'_val' : str(roundit(Fo))}})
    doc['result'].update({'concentration_dry_corrected':{'_val' : str(roundit(concentration_dry_corrected))}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
