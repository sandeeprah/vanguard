from math import *
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from techlib.electrical.cable.cablesizing import full_load_current, get_cable_lookup, select_cable_section, get_k1, get_k2, get_k3, derive_arrangement, getXc, getRc, getVoltageDrop, select_cable_section_from_voltageDrop, select_cable_section_from_shortCircuit

from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]



    try:
        phases = doc['input']['phases']['_val']
        voltage = float(doc['input']['voltage']['_val'])
        power_factor = float(doc['input']['power_factor']['_val'])
        rated_load = float(doc['input']['rated_load']['_val'])
        load_efficiency = float(doc['input']['load_efficiency']['_val'])
        FLC = full_load_current(phases=phases, voltage=voltage, power_factor=power_factor, rated_load=rated_load, load_efficiency=load_efficiency)
        FLC = roundit(FLC)
        doc['result'].update({'FLC':{'_val' : str(FLC)}})
    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate, Full Load Current')


    try:
        insulation_type = doc['input']['insulation_type']['_val']
        conductor_type = doc['input']['conductor_type']['_val']
        cable_type = doc['input']['cable_type']['_val']
        installation_method = doc['input']['installation_method']['_val']
        if (phases=='single'):
            loaded_conductors="LC2"
        else:
            loaded_conductors="LC3"

        installation_type = doc['input']['installation_type']['_val']
        arrangement = derive_arrangement(installation_method, installation_type)
        table, column = get_cable_lookup(conductor_type=conductor_type, insulation_type=insulation_type, \
                                cable_type=cable_type, loaded_conductors=loaded_conductors,\
                                installation_method=installation_method, arrangement=arrangement)

        Ibase_ref = table + "," + column
        doc['result'].update({'Ibase_ref':{'_val' : Ibase_ref }})

    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to Retrieve valid IEC Table for lookup, check inputs')




    try:
        if (installation_method in ["D1", "D2"]):
            location = "ground"
            T = float(doc['input']['Tground']['_val'])
        else:
            location = "air"
            T = float(doc['input']['Tamb']['_val'])

        k1, k1_ref = get_k1(T=T, insulation_type=insulation_type, location=location)
        k1 = roundit(k1)
        doc['result'].update({'k1':{'_val' : str(k1) }})
        doc['result'].update({'k1_ref':{'_val' : k1_ref }})
    except Exception as e:
        k1 = nan
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate, k1')


    try:
        installation_type = doc['input']['installation_type']['_val']
        no_grpcables = int(doc['input']['no_grpcables']['_val'])
        no_layers = int(doc['input']['no_layers']['_val'])
        underground_spacing = doc['input']['underground_spacing']['_val']
        k2, k2_ref = get_k2(installation_method=installation_method, installation_type=installation_type, cable_type=cable_type, no_layers=no_layers, no_grpcables=no_grpcables, underground_spacing=underground_spacing )
        k2 = roundit(k2)
        doc['result'].update({'k2':{'_val' : str(k2) }})
        doc['result'].update({'k2_ref':{'_val' : k2_ref }})
    except Exception as e:
        k2 = nan
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate, k2')


    try:
        if (installation_method=='D1') or (installation_method=='D2'):
            soil_thermal_resistivity = float(doc['input']['soil_thermal_resistivity']['_val'])
            k3, k3_ref = get_k3(soil_thermal_resistivity)
            doc['result'].update({'k3':{'_val' : str(k3) }})
            doc['result'].update({'k3_ref':{'_val' : k3_ref }})
        else:
            k3 = 1
    except Exception as e:
        k3 = nan
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate, k3')

    try:
        total_deration = roundit(k1*k2*k3)
        doc['result'].update({'total_deration':{'_val' : str(total_deration) }})
        cable_section, Ibase =  select_cable_section(table, column, FLC, total_deration)
        Iderated = roundit(Ibase*total_deration)
        doc['result'].update({'cable_section':{'_val' : str(cable_section) }})
        doc['result'].update({'Ibase':{'_val' : str(Ibase)}})
        doc['result'].update({'Iderated':{'_val' : str(Iderated)}})
    except Exception as e:
        cable_section = nan
        Ibase = nan
        doc['errors'].append(str(e))
        doc['errors'].append('Failed to calculate cable section based on ampacity considerations')

    try:
        voltage_drop_calculation = doc['input']['voltage_drop_calculation']['_val']
    except:
        voltage_drop_calculation = "no"

    if (voltage_drop_calculation=="yes"):
        try:
            cable_run = float(doc['input']['cable_run']['_val'])
            allowable_drop = float(doc['input']['allowable_drop']['_val'])
            cable_section_voltage, Vdrop_voltage = select_cable_section_from_voltageDrop(phases=phases, I=FLC, V=voltage, pf=power_factor, L=cable_run, Vdrop_permitted=allowable_drop, insulation_type=insulation_type, conductor_type=conductor_type, cable_type=cable_type, arrangement=arrangement)
            Vdrop_voltage = roundit(Vdrop_voltage)
            doc['result'].update({'cable_section_voltage':{'_val' : str(cable_section_voltage) }})
            doc['result'].update({'Vdrop_voltage':{'_val' : str(Vdrop_voltage) }})
        except Exception as e:
            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate cable section based on Voltage Drop considerations')

        try:
            cable_section_manual = float(doc['input']['cable_section_manual']['_val'])
            Xc = getXc(cable_section_manual, insulation_type, cable_type, arrangement)
            Rc = getRc(cable_section_manual, insulation_type, conductor_type, cable_type)
            deltaV = getVoltageDrop(phases=phases, I=FLC, Rc=Rc, Xc=Xc, pf=power_factor, L=cable_run)
            actual_drop_manual = deltaV*100/voltage
            Xc = roundit(Xc)
            Rc = roundit(Rc)
            actual_drop_manual = roundit(actual_drop_manual)
            doc['result'].update({'Xc':{'_val' : str(Xc) }})
            doc['result'].update({'Rc':{'_val' : str(Rc) }})
            doc['result'].update({'actual_drop_manual':{'_val' : str(actual_drop_manual) }})
        except Exception as e:
            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate voltage drop for manually selected cable section')


    try:
        short_circuit_calculation = doc['input']['short_circuit_calculation']['_val']
    except:
        short_circuit_calculation = "no"

    if (short_circuit_calculation=="yes"):
        try:
            I_sc = float(doc['input']['I_sc']['_val'])
            t_fault = float(doc['input']['t_fault']['_val'])
            Tc_basis = doc['input']['Tc_basis']['_val']
            if (Tc_basis=="custom"):
                Tc_init = float(doc['input']['Tc_init']['_val'])
                Tc_final = float(doc['input']['Tc_final']['_val'])
                cable_section_sc, k_sc = select_cable_section_from_shortCircuit(I_sc, t_fault, conductor_type="Cu", Tc_init=Tc_init, Tc_final=Tc_final)
            else:
                cable_section_sc, k_sc = select_cable_section_from_shortCircuit(I_sc, t_fault, conductor_type="Cu", insulation_type=insulation_type)

            k_sc = roundit(k_sc)
            doc['result'].update({'cable_section_sc':{'_val' : str(cable_section_sc) }})
            doc['result'].update({'k_sc':{'_val' : str(k_sc) }})
        except Exception as e:
            doc['errors'].append(str(e))
            doc['errors'].append('Failed to calculate cable section based on Short Circuit considerations')


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
