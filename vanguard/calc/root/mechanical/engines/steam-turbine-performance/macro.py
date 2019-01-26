import CoolProp.CoolProp as CP
from fluids.control_valve import size_control_valve_g
from techlib.units import treeUnitConvert, SI_UNITS, unitConvert
from techlib.mathutils import roundit
from fluids.safety_valve import API520_B, API520_N, API520_SH, API520_round_size, API520_A_steam
from techlib.fluids.safety_valve  import API520_A_l_cert, API526_letter,  Reynolds
from techlib.conversions import dyn2kinVisc, kin2dynVisc, SSU2cSt
from techlib.thermochem.psychrometry import Pws, humidityratio

from copy import deepcopy
import math

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    solve_for = doc['input']['solve_for']['_val']
    inlet_definition = doc['input']['inlet_definition']['_val']
    P_inlet = float(doc['input']['P_inlet']['_val'])


    # Determine Inlet Properties
    if (inlet_definition=="P-T"):
        T_inlet = float(doc['input']['T_inlet']['_val'])
        try:
            h_inlet = round(CP.PropsSI('H','P', P_inlet, 'T', T_inlet, 'Water'),1)
            s_inlet = round(CP.PropsSI('S','P', P_inlet, 'T', T_inlet, 'Water'),1)
            phase_inlet = CP.PhaseSI('P',P_inlet,'T',T_inlet,'Water')
        except Exception as e:
            doc['errors'].append('Failed to calculate steam inlet conditions, check inputs')
            h_inlet = math.nan
            s_inlet = math.nan
            phase_inlet = ""

    elif (inlet_definition=='P-h'):
        h_inlet = float(doc['input']['h_inlet']['_val'])
        try:
            T_inlet = round(CP.PropsSI('T','P', P_inlet, 'H', h_inlet, 'Water'),1)
            s_inlet = round(CP.PropsSI('S','P', P_inlet, 'H', h_inlet, 'Water'),1)
            phase_inlet = CP.PhaseSI('P',P_inlet,'H',h_inlet,'Water')
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate steam inlet conditions, check inputs')
            T_inlet = math.nan
            s_inlet = math.nan
            phase_inlet = ""


    elif(inlet_definition=='P-s'):
        s_inlet = float(doc['input']['s_inlet']['_val'])
        try:
            T_inlet = round(CP.PropsSI('T','P', P_inlet, 'S', s_inlet, 'Water'),1)
            h_inlet = round(CP.PropsSI('H','P', P_inlet, 'S', s_inlet, 'Water'),1)
            phase_inlet = CP.PhaseSI('P',P_inlet,'S',s_inlet,'Water')
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate steam inlet conditions, check inputs')
            T_inlet = math.nan
            h_inlet = math.nan
            phase_inlet = ""

    elif(inlet_definition=='P-Q'):
        Q_inlet = float(doc['input']['Q_inlet']['_val'])
        try:
            T_inlet = round(CP.PropsSI('T','P', P_inlet, 'Q', Q_inlet, 'Water'),1)
            s_inlet = round(CP.PropsSI('S','P', P_inlet, 'Q', Q_inlet, 'Water'),1)
            h_inlet = round(CP.PropsSI('H','P', P_inlet, 'Q', Q_inlet, 'Water'),1)
            phase_inlet = CP.PhaseSI('P',P_inlet,'Q',Q_inlet,'Water')
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate steam inlet conditions, check inputs')
            T_inlet = math.nan
            s_inlet = math.nan
            phase_inlet = ""




    outlet_definition = doc['input']['outlet_definition']['_val']
    P_outlet = float(doc['input']['P_outlet']['_val'])
    s_outlet_ideal = s_inlet

    try:
        h_outlet_ideal = round(CP.PropsSI('H','P', P_outlet, 'S', s_outlet_ideal, 'Water'),1)
    except Exception as e:
#        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate steam ideal outlet conditions, check inputs')
        h_outlet_ideal = math.nan


    if (solve_for=='outlet_properties'):
        isentropic_efficiency = float(doc['input']['isentropic_efficiency']['_val'])
        try:
            h_outlet = h_inlet - (isentropic_efficiency/100)*(h_inlet - h_outlet_ideal)
            h_outlet = round(h_outlet,1)
            T_outlet = round(CP.PropsSI('T','P', P_outlet, 'H', h_outlet, 'Water'),1)
            s_outlet = round(CP.PropsSI('S','P', P_outlet, 'H', h_outlet, 'Water'),1)
            phase_outlet = CP.PhaseSI('P',P_outlet,'H',h_outlet,'Water')
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate steam outlet conditions, check inputs')
            h_outlet = math.nan
            T_outlet = math.nan
            s_outlet = math.nan
            phase_outlet = ""

    else:

        try:
            if (outlet_definition=="P-T"):
                T_outlet = float(doc['input']['T_outlet']['_val'])
                h_outlet = round(CP.PropsSI('H','P', P_outlet, 'T', T_outlet, 'Water'),1)
                s_outlet = round(CP.PropsSI('S','P', P_outlet, 'T', T_outlet, 'Water'),1)

            elif (outlet_definition=='P-h'):
                h_outlet = float(doc['input']['h_outlet']['_val'])
                T_outlet = round(CP.PropsSI('H','P', P_outlet, 'H', h_outlet, 'Water'),1)
                s_outlet = round(CP.PropsSI('S','P', P_outlet, 'H', h_outlet, 'Water'),1)

            elif(outlet_definition=='P-s'):
                s_outlet = float(doc['input']['s_outlet']['_val'])
                h_outlet = float(doc['input']['h_outlet']['_val'])
                T_outlet = round(CP.PropsSI('H','P', P_outlet, 'H', h_outlet, 'Water'),1)

            elif(outlet_definition=='P-Q'):
                Q_outlet = float(doc['input']['Q_outlet']['_val'])
                T_outlet = round(CP.PropsSI('T','P', P_outlet, 'Q', Q_outlet, 'Water'),1)
                h_outlet = round(CP.PropsSI('H','P', P_outlet, 'Q', Q_outlet, 'Water'),1)
                s_outlet = round(CP.PropsSI('S','P', P_outlet, 'Q', Q_outlet, 'Water'),1)

        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate steam outlet conditions, check inputs')
            h_outlet = math.nan
            T_outlet = math.nan
            s_outlet = math.nan

        try:
            isentropic_efficiency = (h_inlet - h_outlet)*100/(h_inlet - h_outlet_ideal)
            isentropic_efficiency = round(isentropic_efficiency, 1)
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to Isentropic Efficiency, check inputs')
            isentropic_efficiency = math.nan



    phase_outlet = CP.PhaseSI('P',P_outlet,'H',h_outlet,'Water')

    turbine_definition = doc['input']['turbine_definition']['_val']
    generator_efficiency = float(doc['input']['generator_efficiency']['_val'])
    if (turbine_definition=='mass_flow'):
        mass_flow = float(doc['input']['mass_flow']['_val'])
        try:
            energy_output = (h_inlet - h_outlet)*mass_flow
            energy_output = roundit(energy_output)
            power_output = energy_output*generator_efficiency/100
            power_output = roundit(power_output)
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate Turbine Parameters, check inputs')
            energy_output = math.nan
            power_output = math.nan
    else:
        try:
            power_output = float(doc['input']['power_output']['_val'])
            energy_output = power_output*100/generator_efficiency
            mass_flow = energy_output/(h_inlet - h_outlet)
            mass_flow = roundit(mass_flow)
        except Exception as e:
#            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate Turbine Parameters, check inputs')
            energy_output = math.nan
            mass_flow = math.nan

    doc['result'].update({'P_inlet':{'_val':str(P_inlet), '_dim':'pressure'}})
    doc['result'].update({'T_inlet':{'_val':str(T_inlet), '_dim':'temperature'}})
    doc['result'].update({'h_inlet':{'_val':str(h_inlet), '_dim':'specificEnergy'}})
    doc['result'].update({'s_inlet':{'_val':str(s_inlet), '_dim':'specificHeat'}})
    doc['result'].update({'phase_inlet':{'_val':str(phase_inlet)}})
    doc['result'].update({'h_outlet_ideal':{'_val':str(h_outlet_ideal), '_dim':'specificEnergy'}})

    doc['result'].update({'P_outlet':{'_val':str(P_outlet), '_dim':'pressure'}})
    doc['result'].update({'T_outlet':{'_val':str(T_outlet), '_dim':'temperature'}})
    doc['result'].update({'h_outlet':{'_val':str(h_outlet), '_dim':'specificEnergy'}})
    doc['result'].update({'s_outlet':{'_val':str(s_outlet), '_dim':'specificHeat'}})
    doc['result'].update({'phase_outlet':{'_val':str(phase_outlet)}})

    doc['result'].update({'isentropic_efficiency':{'_val':str(isentropic_efficiency)}})
    doc['result'].update({'generator_efficiency':{'_val':str(generator_efficiency)}})
    doc['result'].update({'mass_flow':{'_val':str(mass_flow), '_dim':'massflow'}})
    doc['result'].update({'energy_output':{'_val':str(energy_output), '_dim':'power'}})
    doc['result'].update({'power_output':{'_val':str(power_output), '_dim':'power'}})


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True



def humidity_correction(x):
    x1 = 0.0063256
    y1 = 1.00
    x2 = 0.03
    y2 = 0.997
    y = y1 + (y2-y1)*(x-x1)/(x2-x1)
    return y
