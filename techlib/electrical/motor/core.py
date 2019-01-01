from math import *
import pandas as pd
import os
from techlib.mathutils import roundit


def motor_params(kW_rating, poles=2, voltage=415, frequency=50):
    if (voltage != 415):
        raise Exception('Database for given voltage not available')

    if (frequency != 50):
        raise Exception('Database for given frequency not available')

    if (poles==2):
        data_file = "LV_TEFC_415V_50Hz_2Pole.csv"
    elif (poles==4):
        data_file = "LV_TEFC_415V_50Hz_4Pole.csv"
    elif (poles==6):
        data_file = "LV_TEFC_415V_50Hz_6Pole.csv"
    else:
        raise Exception("Invalid number of poles")

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        motor_df = pd.read_csv(data_file_path)
        motor_df = motor_df.set_index('kW')
        param_dict = {}
        param_dict['Frame_Size'] = roundit(motor_df.loc[kW_rating, "Frame_Size"])
        param_dict['Speed'] = roundit(motor_df.loc[kW_rating, "Speed"])
        param_dict['eta_full'] = roundit(motor_df.loc[kW_rating, "eta_full"])
        param_dict['eta_three_fourth'] = roundit(motor_df.loc[kW_rating, "eta_three_fourth"])
        param_dict['eta_half'] = roundit(motor_df.loc[kW_rating, "eta_half"])
        param_dict['pf'] = roundit(motor_df.loc[kW_rating, "pf"])
        param_dict['In'] = roundit(motor_df.loc[kW_rating, "In"])
        param_dict['Is_by_In'] = roundit(motor_df.loc[kW_rating, "Is_by_In"])
        param_dict['Tn'] = roundit(motor_df.loc[kW_rating, "Tn"])
        param_dict['Ti_by_Tn'] = roundit(motor_df.loc[kW_rating, "Ti_by_Tn"])
        param_dict['Tb_by_Tn'] = roundit(motor_df.loc[kW_rating, "Tb_by_Tn"])
        param_dict['J'] = roundit(motor_df.loc[kW_rating, "J"])
        param_dict['weight'] = roundit(motor_df.loc[kW_rating, "weight"])
    except Exception as e:
        param_dict = {}
        param_dict['Frame_Size'] = nan
        param_dict['Speed'] = nan
        param_dict['eta_full'] = nan
        param_dict['eta_three_fourth'] = nan
        param_dict['eta_half'] = nan
        param_dict['pf'] = nan
        param_dict['In'] = nan
        param_dict['Is_by_In'] = nan
        param_dict['Tn'] = nan
        param_dict['Ti_by_Tn'] = nan
        param_dict['Tb_by_Tn'] = nan
        param_dict['J'] = nan
        param_dict['weight'] = nan
        raise Exception('Motor rating not in LV motor range. Motor Dimensions not available')

    return param_dict

def standard_iec_motor(motor_power):
#    iec_sizes_kW = [0.37, 0.75, 1.1, 1.5, 2.2, 3, 3.7, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30,
#               37, 45, 55, 75, 90, 110, 132, 150, 185, 225, 260, 300, 335, 375]


    iec_sizes_kW = [0.37, 0.75, 1.1, 1.5, 2.2, 3, 3.7, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30,
               37, 45, 55, 75, 90, 110, 132, 150, 200, 250, 315, 355]


    motor_power_kW = motor_power/1000
    std_motor_rating= nan
    for size in iec_sizes_kW:
        if size >= motor_power_kW:
            std_motor_rating = size
            break
    if std_motor_rating is nan:
        std_motor_rating = motor_power_kW

    return std_motor_rating*1000


def motor_starting_time(Nr,Jm,Jl,Cs,Cmax,Cl,load_type):
    if load_type =="lift":
        Kl = 1
    elif load_type =="fan":
        Kl = 0.33
    elif load_type =="piston_pump":
        Kl = 0.5
    elif load_type == "flywheel":
        Kl = 0
    else :
        raise Exception("Invalid Load Type")


    Cacc = 0.45*(Cs+Cmax)-Kl*Cl
    print(Cacc)
    Ta = 2*pi*Nr*(Jm+Jl)/(60*Cacc)

    return Ta
