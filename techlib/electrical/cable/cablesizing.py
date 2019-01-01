import json
import os
from math import *
import pandas as pd

from collections import OrderedDict

def get_available_insulations():
    available_options = ["PVC", "XLPE", "MIN_LT_500", "MIN_LT_750", "MIN_HT_500", "MIN_HT_750"]
    return available_options

def get_available_conductors(insulation_type):
    insulation_options = get_available_insulations()
    if insulation_type in insulation_options:
        if (insulation_type=="PVC" or insulation_type=="XLPE"):
            return ["Cu", "Al"]
        else:
            return ["Cu"]
    else:
        raise Exception("Invalid Insulation Type")

def get_available_cables():
    return ["single_core", "multi_core"]


def get_available_installationMethods(insulation_type, cable_type):
    insulation_options = get_available_insulations()
    cable_options = get_available_cables()

    if insulation_type not in insulation_options:
        raise Exception("Invalid Insulation Type")

    if cable_type not in cable_options:
        raise Exception("Invalid Cable Type")

    if (insulation_type=="PVC" or insulation_type=="XLPE"):
        if (cable_type=="single_core"):
            available_options = ["A1", "B1", "C", "D1", "D2", "F", "G"]
        if (cable_type=="multi_core"):
            available_options = ["A2", "B2", "C", "D1", "D2", "E"]
    else:
        if (cable_type=="single_core"):
            available_options = ["C", "F", "G"]
        if (cable_type=="multi_core"):
            available_options = ["C", "E"]

    return available_options



def get_available_installationTypes(installation_method, cable_type):
    available_options = []
    if (installation_method in ["A1", "A2", "B1", "B2"]):
        available_options = []
    if (installation_method =="C"):
        available_options = ["on_wall", "under_ceiling"]
    if (installation_method in ["D1", "D2"]):
        available_options = []
    if (installation_method == "E"):
        available_options = ["bunched",
                            "horzperftray_touching",
                            "vertperftray_touching",
                            "ladder_touching",
                            "unpftray_touching",
                            "horzperftray_spaced",
                            "vertperftray_spaced",
                            "ladder_spaced"
                            ]
    if (installation_method == "F"):
        available_options = ["bunched",
                        "horzperftray_flat",
                        "vertperftray_flat",
                        "ladder_flat",
                        "horzperftray_trefoil",
                        "vertperftray_trefoil",
                        "ladder_trefoil"
                        ]
    if (installation_method == "G"):
        available_options = ["spaced_horizontal",
                            "spaced_vertical"]

    return available_options


def derive_arrangement(installation_method, installation_type):
    arrangement = "trefoil"
    if (installation_method == "F"):
        if (installation_type=="bunched"):
            arrangement = "trefoil"
        elif (installation_type=="horzperftray_flat"):
            arrangement = "flat"
        elif (installation_type=="vertperftray_flat"):
            arrangement = "flat"
        elif (installation_type=="ladder_flat"):
            arrangement = "flat"
        elif (installation_type=="horzperftray_trefoil"):
            arrangement = "trefoil"
        elif (installation_type=="vertperftray_trefoil"):
            arrangement = "trefoil"
        elif (installation_type=="ladder_trefoil"):
            arrangement = "trefoil"
        else:
            raise Exception("Invalid Installation Type")

    if(installation_method=="G"):
        if (installation_type=="spaced_horizontal"):
            arrangement = "spaced_horizontal"
        elif(installation_type=="spaced_vertical"):
            arrangement = "spaced_vertical"
        else:
            raise Exception("Invalid Installation Type")

    if(installation_method=="C"):
        if (installation_type=="on_wall"):
            arrangement = "flat"
        elif(installation_type=="on_ceiling"):
            arrangement = "flat"
        else:
            raise Exception("Invalid Installation Type")

    return arrangement


def get_available_layers(installation_type):
    available_options = []

    if (installation_type in ['bunched', 'on_wall', 'under_ceiling']):
        available_options = [1]

    # based on Table B52.20
    elif(installation_type in ["horzperftray_touching","unpftray_touching","ladder_touching"]):
        available_options = [1,2,3,6]
    elif(installation_type in ["horzperftray_spaced","ladder_spaced"]):
        available_options = [1,2,3]
    elif(installation_type in ["vertperftray_touching","vertperftray_spaced"]):
        available_options = [1,2]

    # based on Table B52.21
    elif(installation_type in ["horzperftray_flat","ladder_flat","horzperftray_trefoil",]):
        available_options = [1,2,3]
    elif(installation_type in ["vertperftray_flat","vertperftray_trefoil","ladder_trefoil"]):
        available_options = [1,2]


    return available_options


def get_available_no_grpcables(installation_method):
    available_options = []
    if (installation_method in ['A1', 'A2', 'B1', 'B2', 'C']):
        available_options = [1,2,3,4,5,6,7,8,9,12,16,20]

    elif(installation_method == "D2"):
        available_options = [1,2,3,4,5,6,7,8,9,12,16,20]

    elif(installation_method in  ["D1", "G"]):
        available_options = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

    elif(installation_method == "E"):
        available_options = [1,2,3,4,6,9]

    elif(installation_method =="F"):
        available_options = [1,2,3]

    else:
        raise Exception("Invalid Installation Method")


    return available_options


def get_available_underground_spacing(installation_method):
    available_options =[]
    if (installation_method=="D1"):
        available_options = ["CT", "C250", "C500", "C1000"]
    elif(installation_method=="D2"):
        available_options = ["CT", "CD", "C125", "C250", "C500"]
    else:
        raise Exception("Invalid Installation Method")

    return available_options


def get_cable_lookup(insulation_type="PVC", conductor_type="Cu", cable_type="multicore", loaded_conductors=3,  installation_method="E", arrangement=None):
    table=""
    column = ""
    if (insulation_type=="PVC" and loaded_conductors=="LC2" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Cu"):
        table = "table_B52_2_CU"
    elif (insulation_type=="PVC" and loaded_conductors=="LC2" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Al"):
        table = "table_B52_2_AL"
    elif (insulation_type=="XLPE" and loaded_conductors=="LC2" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Cu"):
        table = "table_B52_3_CU"
    elif (insulation_type=="XLPE" and loaded_conductors=="LC2" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Al"):
        table = "table_B52_3_AL"
    elif (insulation_type=="PVC" and loaded_conductors=="LC3" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Cu"):
        table = "table_B52_4_CU"
    elif (insulation_type=="" and loaded_conductors=="LC3" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Al"):
        table = "table_B52_4_AL"
    elif (insulation_type=="XLPE" and loaded_conductors=="LC3" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Cu"):
        table = "table_B52_5_CU"
    elif (insulation_type=="XLPE" and loaded_conductors=="LC3" and installation_method in ["A1", "A2", "B1", "B2", "C","D1", "D2"] and conductor_type=="Al"):
        table = "table_B52_5_AL"
    elif(insulation_type=="MIN_LT_500" and installation_method =="C"):
        table = "table_B52_6_500V"
    elif(insulation_type=="MIN_LT_750" and installation_method =="C"):
        table = "table_B52_6_750V"
    elif(insulation_type=="MIN_HT_500" and installation_method =="C"):
        table = "table_B52_7_500V"
    elif(insulation_type=="MIN_HT_750" and installation_method =="C"):
        table = "table_B52_7_750V"
    elif(insulation_type=="MIN_LT_500" and installation_method in ["E", "F", "G"]):
        table = "table_B52_8_500V"
    elif(insulation_type=="MIN_LT_750" and installation_method in ["E", "F", "G"]):
        table = "table_B52_8_750V"
    elif(insulation_type=="MIN_HT_500" and installation_method in ["E", "F", "G"]):
        table = "table_B52_9_500V"
    elif(insulation_type=="MIN_HT_750" and installation_method in ["E", "F", "G"]):
        table = "table_B52_9_750V"
    elif(insulation_type=="PVC" and conductor_type=="Cu" and installation_method in ["E", "F", "G"]):
        table = "table_B52_10"
    elif(insulation_type=="PVC" and conductor_type=="Al" and installation_method in ["E", "F", "G"]):
        table = "table_B52_11"
    elif(insulation_type=="XLPE" and conductor_type=="Cu" and installation_method in ["E", "F", "G"]):
        table = "table_B52_12"
    elif(insulation_type=="XLPE" and conductor_type=="Al" and installation_method in ["E", "F", "G"]):
        table = "table_B52_13"
    else:
        raise Exception("No Current Capacity available for parameters specifed")


    if (table in ["table_B52_2_CU","table_B52_2_AL","table_B52_3_CU","table_B52_3_AL","table_B52_4_CU","table_B52_4_AL","table_B52_5_CU", "table_B52_5_AL"]):
        if (installation_method=="A1"):
            column = "C2"
        elif(installation_method=="A2"):
            column = "C3"
        elif(installation_method=="B1"):
            column = "C4"
        elif(installation_method=="B2"):
            column = "C5"
        elif(installation_method=="C"):
            column = "C6"
        elif(installation_method=="D1"):
            column = "C7"
        elif(installation_method=="D2"):
            column = "C8"
        else:
            raise Exception("Invalid Installation Method")

    elif (table in ["table_B52_6_500V","table_B52_6_750V","table_B52_7_500V","table_B52_7_750V"]):
        if (cable_type=="multi_core"):
            if (loaded_conductors=="LC2"):
                column = "C2"
            elif(loaded_conductors=="LC3"):
                column = "C3"
            else:
                raise Exception("Invalid Loaded Conductors")
        elif(cable_type=="single_core"):
            if (loaded_conductors=="LC2"):
                column = "C2"
            elif(loaded_conductors=="LC3"):
                if (arrangement == "trefoil"):
                    column="C3"
                elif(arrangement=="flat"):
                    column="C4"
                else:
                    raise Exception("Invalid Arrangement")
            else:
                raise Exception("Invalid Loaded Conductors")

        else:
            raise Exception("Invalid Cable Type")



    elif (table in ["table_B52_8_500V","table_B52_8_750V","table_B52_9_500V","table_B52_9_750V"]):
        if (cable_type=="multi_core"):
            if (loaded_conductors=="LC2"):
                column = "C2"
            elif(loaded_conductors=="LC3"):
                column = "C3"
            else:
                raise Exception("Invalid Loaded Conductors")
        elif(cable_type=="single_core"):
            if (loaded_conductors=="LC2"):
                column = "C2"
            elif(loaded_conductors=="LC3"):
                if(installation_method=="F"):
                    if (arrangement == "trefoil"):
                        column="C3"
                    elif(arrangement=="flat"):
                        column="C4"
                    else:
                        raise Exception("Invalid Arrangement")
                elif(installation_method=="G"):
                    if(arrangement=="spaced_horizontal"):
                        column="C5"
                    elif(arrangement=="spaced_vertical"):
                        column="C6"
                    else:
                        raise Exception("Invalid Arrangement")
                else:
                    raise Exception("Invalid Installation Method")
            else:
                raise Exception("Invalid Loaded Conductors")
        else:
            raise Exception("Invalid Cable Type")



    elif (table in ["table_B52_10","table_B52_11","table_B52_12","table_B52_13"]):
        if (cable_type=="multi_core"):
            if (loaded_conductors=="LC2"):
                column = "C2"
            elif(loaded_conductors=="LC3"):
                column = "C3"
            else:
                raise Exception("Invalid Loaded Conductors")
        elif(cable_type=="single_core"):
            if (loaded_conductors=="LC2"):
                column = "C4"
            elif(loaded_conductors=="LC3"):
                if (installation_method=="F"):
                    if (arrangement == "trefoil"):
                        column="C5"
                    elif(arrangement=="flat"):
                        column="C6"
                    else:
                        raise Exception("Invalid Arrangement")
                elif (installation_method=="G"):
                    if (arrangement == "spaced_horizontal"):
                        column="C7"
                    elif(arrangement=="spaced_vertical"):
                        column="C8"
                    else:
                        raise Exception("Invalid Arrangement")
                else:
                    raise Exception("Invalid Installation Method")
            else:
                raise Exception("Invalid Loaded Conductors")

        else:
            raise Exception("Invalid Cable Type")

    return table, column


def get_current_capacity(cable_section, table, column):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    cable_file = os.path.join(THIS_FOLDER, table+".csv")
    cable_df = pd.read_csv(cable_file)
    cable_df = cable_df.set_index('C1')
    ampacity = cable_df.loc[cable_section, column]
    return ampacity

def select_cable_section(table, column, FLC, total_deration):
    reqd_amps = FLC/total_deration
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    cable_file = os.path.join(THIS_FOLDER, table+".csv")
    cable_df = pd.read_csv(cable_file)
    cable_df = cable_df.set_index('C1')
    condition = cable_df[column] > reqd_amps
    result_row = cable_df[condition]
    cable_section = float(result_row.head(1).iloc[0].name)
    Ibase = float(result_row.head(1).iloc[0][column])
    return cable_section, Ibase


def full_load_current(phases, voltage, power_factor, rated_load, load_efficiency):
    flc = 0
    if (phases=="single"):
        flc = rated_load/(voltage*power_factor*load_efficiency)
    elif(phases=="three"):
        flc = rated_load/(1.732*voltage*power_factor*load_efficiency)
    else:
        raise Exception("Invalid 'phases'")

    return flc


def get_k1(T, insulation_type="PVC", location="ground"):
    k1 = 1
    k1_ref = ""
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    if (location=="air"):
        k1_file = os.path.join(THIS_FOLDER, "table_B52_14.csv")
        k1_ref = "table_B52_14"
    elif(location=="ground"):
        k1_file = os.path.join(THIS_FOLDER, "table_B52_15.csv")
        k1_ref = "table_B52_15"
    else:
        raise Exception("Invalid 'location' input for cable installation")

    k1_df = pd.read_csv(k1_file)
    k1_df = k1_df.set_index('T')
    insul_type = insulation_type
    if (insulation_type=='MIN_LT_500' or insulation_type=='MIN_LT_750'):
        insul_type = "MIN_LT"
    elif (insulation_type=='MIN_HT_500' or insulation_type=='MIN_HT_750'):
        insul_type = "MIN_HT"

    k1 = k1_df.loc[T, insul_type]

    try:
        k1 = float(k1)
    except:
        k1 = nan

    return k1, k1_ref


def get_k2(installation_method="E", installation_type="bunched", no_layers=1, cable_type="multi_core", no_grpcables=1, underground_spacing="" ):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    k2 = 1
    table=""
    row=""
    column = ""

    if (installation_method in ["A1", "A2", "B1","B2"]):
        table = "table_B52_17"
        col= str(no_grpcables)
        row = "bunched"
        k2_file = os.path.join(THIS_FOLDER, table+".csv")
        k2_df = pd.read_csv(k2_file)
        k2_df = k2_df.set_index('Item')
        k2 = float(k2_df.loc[row, col])
        k2_ref = "table_B52_17"

    elif(installation_method=="C"):
        table = "table_B52_17"
        col= str(no_grpcables)
        if(installation_type=="on_wall"):
            row = "on_wall"
        elif(installation_type=="under_ceiling"):
            row = "under_ceiling"
        else:
            raise Exception("Invalid Installation Type")
        k2_file = os.path.join(THIS_FOLDER, table+".csv")
        k2_df = pd.read_csv(k2_file)
        k2_df = k2_df.set_index('Item')
        k2 = float(k2_df.loc[row, col])

    elif(installation_method=="D1"):
        if (cable_type=="multi_core"):
            table = "table_B52_19_A"
        elif(cable_type=="single_core"):
            table = "table_B52_19_B"
        else:
            raise Exception("Invalid Cable Type")

        if (underground_spacing in ["CT", "C250", "C500", "C1000"]):
            col = underground_spacing
        else:
            raise Exception("Invalid Underground Spacing")

        row = no_grpcables
        k2_file = os.path.join(THIS_FOLDER, table+".csv")
        k2_df = pd.read_csv(k2_file)
        k2_df = k2_df.set_index('N')
        k2 = float(k2_df.loc[row, col])

    elif(installation_method=="D2"):
        table = "table_B52_18"

        row = no_grpcables
        if (underground_spacing in ["CT", "CD", "C125", "C250", "C500"]):
            col = underground_spacing
        else:
            raise Exception("Invalid Underground Spacing")
        k2_file = os.path.join(THIS_FOLDER, table+".csv")
        k2_df = pd.read_csv(k2_file)
        k2_df = k2_df.set_index('N')
        k2 = float(k2_df.loc[row, col])

    elif(installation_method=="E"):
        item_options = get_available_installationTypes(installation_method, cable_type)
        if(installation_type in item_options):
            if (installation_type=="bunched"):
                table = "table_B52_17"
                row = "bunched"
                col = str(no_grpcables)
                k2_file = os.path.join(THIS_FOLDER, table+".csv")
                k2_df = pd.read_csv(k2_file)
                k2_df = k2_df.set_index('Item')
                k2 = float(k2_df.loc[row, col])
            else:
                table = "table_B52_20"
                k2_file = os.path.join(THIS_FOLDER, table+".csv")
                k2_df = pd.read_csv(k2_file)
                condition = (k2_df['Type'] == installation_type) & (k2_df['Layer']==no_layers)
                result = k2_df[condition]
                col = str(no_grpcables)
                k2 = float(result.head(1).iloc[0][col])
        else:
            raise Exception("Invalid Installation Type")

    elif(installation_method=="F"):
        item_options = get_available_installationTypes(installation_method, cable_type)
        if(installation_type in item_options):
            if (installation_type=="bunched"):
                table = "table_B52_17"
                row = "bunched"
                col = str(no_grpcables)
                k2_file = os.path.join(THIS_FOLDER, table+".csv")
                k2_df = pd.read_csv(k2_file)
                k2_df = k2_df.set_index('Item')
                k2 = float(k2_df.loc[row, col])
            else:
                table = "table_B52_21"
                k2_file = os.path.join(THIS_FOLDER, table+".csv")
                k2_df = pd.read_csv(k2_file)
                condition = (k2_df['Type'] == installation_type) & (k2_df['Layer']==no_layers)
                result = k2_df[condition]
                col = str(no_grpcables)
                k2 = float(result.head(1).iloc[0][col])

        else:
            raise Exception("Invalid Installation Type")


    elif(installation_method=="G"):
        table = ""
        k2 = 1

    else:
        raise Exception("Invalid Installation Method. K2 could not be looked up")

    k2_ref = table
    return k2, k2_ref


def get_k3(soil_thermal_resistivity):
    k3 = 1
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    k3_file = os.path.join(THIS_FOLDER, "table_B52_16.csv")
    k3_ref = "table_B52_16"
    k3_df = pd.read_csv(k3_file)
    k3_df = k3_df.set_index('R')
    k3 = k3_df.loc[soil_thermal_resistivity]

    try:
        k3 = float(k3)
    except:
        k3 = nan

    return k3, k3_ref


def getVoltageDrop(phases, I, Rc, Xc, pf, L):
    '''
    Calculates Voltage Drop in a cable in 3phase circuit

    Arguments:
    ----------
    phases: no. of phases - 1 for single phase, 3 for three phase
    I   : nominal full load or starting current (A)
    Rc  : ac resistance of the cable (ohm/km)
    Xc  : ac reactance of the cable (ohm/km)
    pf  : load power factor
    L   : length of the cable (m)

    Returns:
    --------
    Voltage Drop (V)
    '''

    if (pf > 1 or pf < 0):
        raise Exception("Invalid Power Factor")

    cos_phi = pf
    sin_phi = sqrt(1-cos_phi**2)

    if (phases=='single'):
        K = 2
    elif(phases=='three'):
        K = sqrt(3)
    else:
        raise Exception("Invalid no. of 'phases'")

    vdrop = K*I*(Rc*cos_phi + Xc*sin_phi)*L/1000

    return vdrop



def getXc(cable_section, insulation_type="PVC", cable_type="multi_core", arrangement="flat"):
    Xc = 0
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    if (arrangement=="spaced_horizontal" or arrangement=='spaced_vertical'):
        arrangement = "flat"

    if (insulation_type not in ["PVC", "EPR", "XLPE"]):
        raise Exception("Invalid Insulation Type")

    if (cable_type not in ["single_core", "multi_core"]):
        raise Exception("Invalid Cable Type")
    else:
        if (cable_type=='single_core' and arrangement not in ["flat", "trefoil"]):
            raise Exception("Invalid Arrangement")


    if (cable_type == "multi_core"):
        table_file = "multicore_ac_reactance.csv"
        column = insulation_type
    elif(cable_type == "single_core"):
        table_file = "singlecore_ac_reactance.csv"
        column = insulation_type + "_" + arrangement

    Xc_file = os.path.join(THIS_FOLDER, table_file)
    Xc_df = pd.read_csv(Xc_file)
    Xc_df = Xc_df.set_index('SIZE')
    Xc = Xc_df.loc[cable_section, column]
    Xc = float(Xc)

    return Xc


def getRc(cable_section, insulation_type="PVC", conductor_type="Cu", cable_type="multi_core"):
    Rc = 0
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    if (insulation_type not in ["PVC", "EPR", "XLPE"]):
        raise Exception("Invalid insulation_type")

    if (conductor_type not in ["Cu", "Al"]):
        raise Exception("Invalid conductor_type")

    if (cable_type not in ["single_core", "multi_core"]):
        raise Exception("Invalid cable_type")

    if  (insulation_type in ["XLPE", "EPR"]):
        T = "90_degC"
    else:
        T = "75_degC"


    if (cable_type == "multi_core"):
        if (conductor_type=="Al"):
            table_file = "multicore_ac_resistance_AL.csv"
        else:
            table_file = "multicore_ac_resistance_CU.csv"
    else:
        if (conductor_type=="Al"):
            table_file = "singlecore_ac_resistance_AL.csv"
        else:
            table_file = "singlecore_ac_resistance_CU.csv"

    column = T

    Rc_file = os.path.join(THIS_FOLDER, table_file)
    Rc_df = pd.read_csv(Rc_file)
    Rc_df = Rc_df.set_index('SIZE')
    Rc = Rc_df.loc[cable_section, column]
    Rc = float(Rc)

    return Rc

def select_cable_section_from_voltageDrop(phases, I, V, pf, L, Vdrop_permitted, insulation_type="PVC", conductor_type="Cu", cable_type="multi_core", arrangement="flat"):
    cable_section_selected = nan
    Vdrop_selected = nan
    available_sections = [1, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630]
    deltaV_permitted = V*Vdrop_permitted/100
    for cbl_sect in available_sections:
        Xc = getXc(cbl_sect, insulation_type, cable_type, arrangement)
        Rc = getRc(cbl_sect, insulation_type, conductor_type, cable_type)
        deltaV = getVoltageDrop(phases, I, Rc, Xc, pf, L)
        Vdrop = deltaV*100/V
        if (Vdrop <= Vdrop_permitted):
            cable_section_selected = cbl_sect
            Vdrop_selected = Vdrop
            break


    return cable_section_selected, Vdrop_selected

def select_cable_section_from_shortCircuit(I_sc, t_fault, conductor_type="Cu", insulation_type="PVC", Tc_init=None, Tc_final=None):
    cable_section = nan
    available_sections = [1, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630]

    Tc = {
        "PVC" :{
            "Tc_init" : 75,
            "Tc_final" : 160
            },
        "EPR" :{
            "Tc_init" : 90,
            "Tc_final" : 250
            },
        "XLPE" :{
            "Tc_init" : 90,
            "Tc_final" : 250
            }
    }

    if (conductor_type=="Cu"):
        C1 = 226
        C2 = 234.5
    elif(conductor_type=="Al"):
        C1 = 148
        C2 = 228

    if (Tc_init==None):
        Tc_init = Tc[insulation_type]["Tc_init"]

    if (Tc_final==None):
        Tc_final = Tc[insulation_type]["Tc_final"]

    Numerator = Tc_final - Tc_init
    Denominator = C2 + Tc_init

    k = C1*sqrt(log(1 + (Numerator/Denominator)))
    A = sqrt(pow(I_sc,2)*t_fault)/k

    for cbl_sect in available_sections:
        if cbl_sect > A:
            cable_section = cbl_sect
            break

    return cable_section, k
