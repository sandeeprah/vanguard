import json
import os
from math import *
import pandas as pd
from techlib.mathutils import linarray_interp, linear_interp

# Calculation of flare diameter

def flareDia(qm, p2, Ma2, Z, T, MW):
    #convert MW to gm/mol
    MW_ = MW*1000
    # convert qm to kg/hr
    qm_ = qm*3600
    # convert p2 to kPa
    p2_ = p2/1000
    dsq = 0.0000323*(qm_/(p2_*Ma2))*((Z*T/MW_)**0.5)
    d = sqrt(dsq)
    return d

def heatRelease(qm, LHV):
    Q = qm*LHV
    return Q

def flameLength(Q):
    x = log10(Q)
    x1 = log10(90000000)
    y1 = log10(20)
    x2 = log10(1000000000)
    y2 = log10(60)

    y =  linear_interp(x, x1, y1, x2, y2)
    L = pow(10,y)
    return L

def vaporFlowrate(Q, MW, T):
    MW_ = MW*1000
    q_vap = Q*(22.4/MW_)*(T/273.15)
    return q_vap

def tipVelocity(q_vap, d):
    A = pi*pow(d,2)/4
    Uj = q_vap/A
    return Uj

def flameDistortion(Uinf_by_Uj):
    data_file = "flamedistortion.csv"
    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        distortion_df = pd.read_csv(data_file_path)
        distortion_df = distortion_df.set_index('Sno')
        x_array = distortion_df['X1'].tolist()
        print(x_array)
        y_array = distortion_df['delY_by_L'].tolist()
        print(y_array)
        Sdy_by_L = linarray_interp(x_array,y_array,Uinf_by_Uj)

        x_array = distortion_df['X2'].tolist()
        y_array = distortion_df['delX_by_L'].tolist()
        Sdx_by_L = linarray_interp(x_array,y_array,Uinf_by_Uj)

    except Exception as e:
        raise e
        raise Exception('S could not be determined')


    return Sdy_by_L, Sdx_by_L



def getH(D,R,Sdy, Sdx):


    return D
