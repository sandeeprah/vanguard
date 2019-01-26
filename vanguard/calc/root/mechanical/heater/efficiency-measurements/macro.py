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

    Td = 273.15 + 15.6

    Ta = parseFloat(doc['input']['Ta']['_val'])
    RH = parseFloat(doc['input']['RH']['_val'])
    flue_O2 = parseFloat(doc['input']['flue_O2']['_val'])
    sampling_basis = doc['input']['sampling_basis']['_val']
    loss_radiation = parseFloat(doc['input']['loss_radiation']['_val'])
    composition_type = doc['input']['composition_type']['_val']
    gasfuel = doc['input']['gasfuel']
    Tf = parseFloat(doc['input']['Tf']['_val'])

    MW,h_L,Cp_f, air_reqd, CO2_formed, H2O_formed, N2_formed = gasfuelProperties(gasfuel, composition_type)
    MW_str = format(MW,'0.6f')
    MW = float(MW_str)
    print("MW is {}".format(MW))
    X_wet = airMoistureContent(Ta, RH)
    air_reqd_RHcorrected = wetAirRequired(air_reqd, X_wet)
    moisture= air_reqd_RHcorrected - air_reqd
    H2O_formed_RHcorrected = H2O_formed + moisture

    excess_Air = excessAir(flue_O2, air_reqd, N2_formed, CO2_formed, H2O_formed_RHcorrected, moisture, sampling_basis)
    excess_Air_pc = excessAir_pc(excess_Air, air_reqd)
    total_air = air_reqd_RHcorrected + excess_Air
    H2O_formed_EAcorrected =  H2OformedEAcorrected(excess_Air_pc, moisture, H2O_formed_RHcorrected)
    Texit_flue = 273 + 148.9
    Patm = 101325

    h_CO2 = getEnthalphy('CarbonDioxide',Texit_flue)
    H_CO2 = h_CO2*CO2_formed

    h_H2O = getEnthalphy('Water',Texit_flue)
    H_H2O = h_H2O*H2O_formed_EAcorrected

    h_N2 = getEnthalphy('Nitrogen', Texit_flue)
    H_N2 = h_N2*N2_formed

    h_EA = getEnthalphy('Air',Texit_flue)
    H_EA = h_EA*excess_Air

    h_s = flueMassicHeatContent(CO2_formed, H2O_formed_EAcorrected, N2_formed, excess_Air, Texit_flue)
    h_r =  radiationLoss(loss_radiation, h_L)
    Cp_a = 1005

    delh_a = Cp_a*(Ta-Td)*total_air
    delh_f = Cp_f*(Tf-Td)
    delh_m = 0 # as steam atomisation not applicable

    e = netThermalEfficiency(h_L, delh_a, delh_f, delh_m, h_r, h_s)
    e_f = fuelEfficiency(h_L, delh_a, delh_f, delh_m, h_r, h_s)
    h_H = getHHV(h_L, H2O_formed)
    e_g = grossThermalEfficiency(h_L, h_H, delh_a, delh_f, delh_m, h_r, h_s)




    doc['result'].update({'MW':{'_val' : format(MW,'0.5f'), '_dim':'molecularMass'}})
    doc['result'].update({'h_L':{'_val' : str(roundit(h_L)), '_dim':'specificEnergy'}})
    doc['result'].update({'h_H':{'_val' : str(roundit(h_H)), '_dim':'specificEnergy'}})
    doc['result'].update({'Cp_f':{'_val' : str(roundit(Cp_f)), '_dim':'specificHeat'}})
    doc['result'].update({'air_reqd':{'_val' : str(roundit(air_reqd))}})
    doc['result'].update({'CO2_formed':{'_val' : str(roundit(CO2_formed))}})
    doc['result'].update({'H2O_formed':{'_val' : str(roundit(H2O_formed))}})
    doc['result'].update({'N2_formed':{'_val' : str(roundit(N2_formed))}})
    doc['result'].update({'X_wet':{'_val' : str(roundit(X_wet))}})
    doc['result'].update({'air_reqd_RHcorrected':{'_val' : str(roundit(air_reqd_RHcorrected))}})
    doc['result'].update({'moisture':{'_val' : str(roundit(moisture))}})
    doc['result'].update({'H2O_formed_RHcorrected':{'_val' : str(roundit(H2O_formed_RHcorrected))}})
    doc['result'].update({'excess_Air':{'_val' : str(roundit(excess_Air))}})
    doc['result'].update({'total_air':{'_val' : str(roundit(total_air))}})
    doc['result'].update({'excess_Air_pc':{'_val' : str(roundit(excess_Air_pc))}})
    doc['result'].update({'H2O_formed_EAcorrected':{'_val' : str(roundit(H2O_formed_EAcorrected))}})

    doc['result'].update({'h_CO2':{'_val' : str(roundit(h_CO2)),'_dim':'specificEnergy'}})
    doc['result'].update({'H_CO2':{'_val' : str(roundit(H_CO2)),'_dim':'energy'}})

    doc['result'].update({'h_H2O':{'_val' : str(roundit(h_H2O)),'_dim':'specificEnergy'}})
    doc['result'].update({'H_H2O':{'_val' : str(roundit(H_H2O)),'_dim':'energy'}})

    doc['result'].update({'h_N2':{'_val' : str(roundit(h_N2)),'_dim':'specificEnergy'}})
    doc['result'].update({'H_N2':{'_val' : str(roundit(H_N2)),'_dim':'energy'}})

    doc['result'].update({'h_EA':{'_val' : str(roundit(h_EA)),'_dim':'specificEnergy'}})
    doc['result'].update({'H_EA':{'_val' : str(roundit(H_EA)),'_dim':'energy'}})

    doc['result'].update({'h_s':{'_val' : str(roundit(h_s)),'_dim':'energy'}})

    doc['result'].update({'h_r':{'_val' : str(roundit(h_r)),'_dim':'specificEnergy'}})
    doc['result'].update({'delh_a':{'_val' : str(roundit(delh_a)),'_dim':'specificEnergy'}})
    doc['result'].update({'delh_f':{'_val' : str(roundit(delh_f)),'_dim':'specificEnergy'}})
    doc['result'].update({'e':{'_val' : str(roundit(e))}})
    doc['result'].update({'e_g':{'_val' : str(roundit(e_g))}})
    doc['result'].update({'e_f':{'_val' : str(roundit(e_f))}})


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
