import json
import os
from math import *
import pandas as pd
from techlib.mathutils import linarray_interp


from collections import OrderedDict

def getS(materialSpec, T):
    data_file = "ASME_B31_3_table_A_1.csv"
    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        stress_df = pd.read_csv(data_file_path)
        stress_df = stress_df.set_index('MatlSpec')
        matl_stress = stress_df.loc[materialSpec]
        matl_stress = matl_stress.drop(['Tmin','Su','Sy'])
        temperature_values = matl_stress.index.tolist()
        stress_values = matl_stress.values

        for index, val  in enumerate(temperature_values):
            temperature_values[index] = float(val)

        # convert K to F
        T_C = T - 273
        T_F = T_C*9/5 + 32
        S_ksi = linarray_interp(temperature_values,stress_values,T_F)
        S = S_ksi*6894757.2932
        #S = 137896000

    except Exception as e:
#        raise e
        raise Exception('S could not be determined')


    return S

def getY(materialSpec, T):
    Material = "Other_ductile_metals"
    Ferritic_steels = []
    Austenitic_steels = ["A312-TP316L","A358-Gr316L","A312-TP304","A358-Gr304"]
    Other_ductile_metals = ["A106-B","A333-6","A671-CC65","A335-P5","A691-5CR"]
    Cast_irons = []

    if materialSpec in Ferritic_steels:
        Material = "Ferritic_steel"
    elif materialSpec in Austenitic_steels:
        Material = "Austenitic_steel"
    elif materialSpec in Other_ductile_metals:
        Material = "Other_ductile_metals"
    elif materialSpec in Cast_irons:
        Material = "Cast_iron"
    else:
        raise Exception("Y lookup from ASME B31.3 table 304.1.1 failed. Check material specification input")

    data_file = "ASME_B31_3_table_304_1_1.csv"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(THIS_FOLDER, data_file)
    Ycoeff_df = pd.read_csv(data_file_path)
    Ycoeff_df = Ycoeff_df.set_index("Material")
    Y_series = Ycoeff_df.loc[Material]
    temperature_values = Y_series.index.tolist()
    for index, val  in enumerate(temperature_values):
        temperature_values[index] = float(val)

    Y_values = Y_series.values

    T_C = T - 273.15
    if (T_C < 482):
        T_C = 482

    if (T_C > 621):
        T_C = 621

    Y = linarray_interp(temperature_values,Y_values,T_C)
    return Y


def getE(weldType):
    data_file = "ASME_B31_3_table_302_3_4.csv"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(THIS_FOLDER, data_file)
    Efactor_df = pd.read_csv(data_file_path)
    Efactor_df = Efactor_df.set_index("Weld_type")
    E = Efactor_df.loc[weldType,"E"]
    return E

def t_pressure(P,D,S,E,W,Y):
    t = P*D/(2*(S*E*W + P*Y))
    return t
