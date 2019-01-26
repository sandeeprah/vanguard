from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from fluids.piping import nearest_pipe
from techlib.mechanical.utils.combustion  import gasCombustion, FlueGasSOx_concentration

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    fuel_as = doc['input']['fuel_as']['_val']
    flue_as = doc['input']['flue_as']['_val']
    gasfuel = doc['input']['gasfuel']
    emission_units = doc['input']['emission_units']['_val']
    Tair = parseFloat(doc['input']['Tair']['_val'])
    Pair = parseFloat(doc['input']['Pair']['_val'])
    RH = parseFloat(doc['input']['RH']['_val'])
    excess_air = parseFloat(doc['input']['excess_air']['_val'])

    Ts = parseFloat(doc['input']['Ts']['_val'])
    Ps = parseFloat(doc['input']['Ps']['_val'])
    O2_reference = parseFloat(doc['input']['O2_reference']['_val'])

    MW_fuel, air_reqd, CO2_formed, H2O_formed, SO2_formed, N2_formed, O2_formed = gasCombustion(gasfuel, fuel_as, flue_as, excess_air, Pair, Tair, RH)
    SOx_concentration = FlueGasSOx_concentration(CO2_formed, H2O_formed, SO2_formed, N2_formed, O2_formed, flue_as=flue_as,  units=emission_units, O2_reference=O2_reference, Ps=Ps, Ts=Ts)


    doc['result'].update({'MW_fuel':{'_val' : str(roundit(MW_fuel)), '_dim':'molecularMass'}})
    doc['result'].update({'flue_as':{'_val' : str(roundit(flue_as))}})
    doc['result'].update({'air_reqd':{'_val' : str(roundit(air_reqd))}})
    doc['result'].update({'CO2_formed':{'_val' : str(roundit(CO2_formed))}})
    doc['result'].update({'H2O_formed':{'_val' : str(roundit(H2O_formed))}})
    doc['result'].update({'SO2_formed':{'_val' : str(roundit(SO2_formed))}})
    doc['result'].update({'N2_formed':{'_val' : str(roundit(N2_formed))}})
    doc['result'].update({'O2_formed':{'_val' : str(roundit(O2_formed))}})
    doc['result'].update({'SOx_concentration':{'_val' : str(roundit(SOx_concentration))}})
    doc['result'].update({'emission_units':{'_val' : emission_units}})
    doc['result'].update({'O2_reference':{'_val' : str(roundit(O2_reference))}})


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
