from math import *
import os
import pandas as pd
import fluids
from scipy.interpolate import interp1d

from vanguard.units import unitConvert
from techlib.electrical.motor.core import standard_iec_motor

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))




def viscCorr(Qbep, Hbep, nu, N, Qratio):
    '''
    Hydraulic Institute Viscosity Correction.
    '''

    _Qbep = Qbep*3600
    _Hbep = Hbep
    _nu = unitConvert(nu,'kinViscosity', 'm2/s','cSt')
    _N = N

    B = 16.5*(pow(_nu,0.5)*pow(_Hbep, 0.0625))/(pow(_Qbep, 0.375)*pow(_N,0.25))

    if (B <= 1):
        Cq = 1
        Ch = 1
        Ceta = 1
    elif(B> 1 and B < 40):
        f = log10(B)
        k = -0.165*pow(f, 3.15)
        Cq = pow(2.71, k)
        Cbep_h = Cq
        Ch = 1 - (1-Cbep_h)*pow(Qratio, 0.75)
        a = -0.0547*pow(B, 0.69)
        Ceta = pow(B,a)
    else:
        raise Exception('Outside Correction Range')

    return Cq, Ch, Ceta


def viscSel(Qvis, Hvis, nu):
    _Qvis = Qvis*3600
    _Hvis = Hvis
    _nu = unitConvert(nu,'kinViscosity', 'm2/s','cSt')

    B = 2.80*(pow(_nu,0.5)/(pow(_Qvis, 0.25)*pow(_Hvis, 0.125)))

    if (B <= 1):
        Cq = 1
        Ch = 1
        Ceta = 1
    elif(B> 1 and B < 40):
        f = log10(B)
        k = -0.165*pow(f, 3.15)
        Cq = pow(2.71, k)
        Ch = Cq

        a = -0.0547*pow(B, 0.69)
        Ceta = pow(B,a)
    else:
        raise Exception('Outside Correction Range')

    return Cq, Ch, Ceta


def specific_speed(Q, H, N):
    Nq = N * pow(Q,0.5) / pow(H,0.75)
    return Nq

def efficiency_overall(Q,Nq):
    '''
    Overall efficiency based on reference Centrifugal Pump by Gulich.

    '''
    Qref = 1
    if (Q > 1):
        a = 0.5
    else:
        a = 1
    m = 0.1 * a * pow(Qref / Q,0.15) * pow(45 / Nq, 0.06)
    eta_overall = 1 - 0.095 * pow(Qref / Q, m) - 0.3 * pow((0.35 - log10(Nq / 23)),2) * pow(Qref / Q,0.05)
    if (eta_overall <= 0):
        raise Exception('Failure in predicting efficiency for specified conditions. Check inputs')

    return eta_overall

def head_coefficient(Nq):
    Nq_ref = 100
    psi = 1.21 * exp(-0.77 * (Nq / Nq_ref))
    sigma_s = Nq/52.92
    return psi

def nozzle_size(Q, allowable_velocity):
    A = Q/allowable_velocity
    D_calculated = sqrt(A*4/pi)
    NPS, Di, Do, t = fluids.piping.nearest_pipe(Di=D_calculated)
    return NPS

def motor_syncspeed(frequency, poles):
    syncspeed = 120*frequency/poles
    return syncspeed

# chart data for Nss vs Ns in US units for overhung pumps
NSS_over = [(694.217,11006.5),
            (735.960,10848.3),
            (802.140,10642.7),
            (876.719,10425.2),
            (919.196,10282.8),
            (979.842,10128.6),
            (1030.09,10006.1),
            (1119.57,9816.33),
            (1190.02,9697.80),
            (1261.37,9591.14),
            (1378.39,9433.14),
            (1457.23,9278.90),
            (1506.51,9223.61),
            (1632.75,9057.64),
            (1774.28,8923.39),
            (1922.53,8828.76)]

NSS_thru = [(685.052,9963.80),
            (782.521,9742.67),
            (3307.92,8090.96),
            (822.476,9687.49),
            (916.280,9533.58),
            (1012.39,9375.65),
            (1109.27,9245.42),
            (1270.31,9095.66),
            (1391.73,8997.14),
            (1503.89,8898.54),
            (1693.88,8764.52),
            (2021.95,8575.38),
            (2283.93,8405.71),
            (2515.95,8323.08),
            (2937.28,8181.37),
            (3818.67,8020.53),
            (4013.20,8001.03)]


def Nss_limit(Nq, pump_design_type='OH'):
    Ns = Nq*51.64
    if pump_design_type=='OH':
        x,y = zip(*NSS_over)
        if (Ns < 695):
            Ns = 695
        if (Ns > 1922):
            Ns = 1922
    else:
        x, y = zip(*NSS_thru)
        if (Ns < 686):
            Ns = 686
        if (Ns > 4000):
            Ns = 4000

    func = interp1d(x, y)
    Nss_US_units = func(Ns)
    Nss = Nss_US_units/51.64
    return Nss


def getNPSHR(Nq, Q, N, design):
    Nss = Nss_limit(Nq, design)
    npshr = pow((N*sqrt(Q)/Nss), 4/3)
    return npshr


def model_select(d2, Q, poles, pump_design_type):
    selected_model = 'None'
    if pump_design_type=='OH':
        if poles == 2:
            data_file = "UCW_2Pole.csv"
        elif poles == 4:
            data_file = "UCW_4Pole.csv"
        else:
            raise Exception("Invalid number of poles for pump design type")

    elif pump_design_type =='DS1':
        if poles == 2:
            data_file = "KS_2Pole.csv"
        elif poles == 4:
            data_file = "KS_4Pole.csv"
        elif poles == 6:
            data_file = "KS_6Pole.csv"
        else:
            raise Exception("Invalid number of poles for pump design type")
    elif pump_design_type =='SS2':
        data_file = "R2_2Pole.csv"
    elif pump_design_type =='DS2':
        if poles ==2:
            data_file = "R2D_2Pole.csv"
        elif poles ==4 :
            data_file = "R2D_4Pole.csv"
        else :
            raise Exception("Invalid number of poles for pump design type")
    else:
        raise Exception("Invalid pump design type")

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        print(data_file)
        pmp_df = pd.read_csv(data_file_path)
        pmp_df = pmp_df.set_index('Model')
        for index, row in pmp_df.iterrows():
            if (row['Qbep']>= Q) and (row['Dia']>=d2*1000):
                if (d2*1000 > 0.75*row['Dia']) and(Q > 0.25*row['Qbep']):
                    selected_model = row.name
                    break
    except :
        raise Exception('Pump Model could not be selected')

    if (selected_model=='None'):
        raise Exception('Pump Model could not be selected')


    return selected_model


def API610_motor_size(Pabsorbed, Poverloading=None):
    motor_power = 0
    if (Pabsorbed < 22000):
        motor_power = 1.25*Pabsorbed
    elif (Pabsorbed >= 22000 and Pabsorbed <=55000):
        motor_power = 1.15*Pabsorbed
    else:
        motor_power = 1.1*Pabsorbed

    if (Poverloading is not None):
        if Poverloading > motor_power:
            motor_power = Poverloading

    std_motor_power = standard_iec_motor(motor_power)
    return std_motor_power


def pump_dimensions(pump_model, design_type):

    if (design_type=="OH"):
        data_file = "UCW_Dimensions.csv"
    elif (design_type=="DS1"):
        data_file = "KS_Dimensions.csv"
    elif (design_type=="SS2" or design_type=="DS2"):
        data_file = "R2R2D_Dimensions.csv"
    else:
        raise Exception("Invalid Design Type")

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        pmpdimensions_df = pd.read_csv(data_file_path)
        pmpdimensions_df = pmpdimensions_df.set_index('Model')
        L = pmpdimensions_df.loc[pump_model, "BL"]/1000
        W = pmpdimensions_df.loc[pump_model, "BW"]/1000
        H1 = pmpdimensions_df.loc[pump_model, "H1"]/1000
        H2 = pmpdimensions_df.loc[pump_model, "H2"]/1000
        H = H1 + H2
        Wpump = pmpdimensions_df.loc[pump_model, "Wpump"]
        Wbase = pmpdimensions_df.loc[pump_model, "Wbase"]
        Ds = pmpdimensions_df.loc[pump_model, "Suction"]
        Dd = pmpdimensions_df.loc[pump_model, "Discharge"]
    except Exception as e:
        print(str(e))
        raise Exception("Pump Dimensions could not be found for the model")

    return Ds, Dd, L, W, H, Wpump, Wbase

def DN2NPS(dn):
    data_file = "DN_to_NPS.csv"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(THIS_FOLDER, data_file)
    convchart_df = pd.read_csv(data_file_path)
    convchart_df = convchart_df.set_index('DN')
    nps = convchart_df.loc[dn, "NPS"]
    return nps

def pump_power(Q, H, eta, rho):
    g = 9.81

    #calculations
    Power_hydraulic = rho*Q*g*H
    Power = Power_hydraulic / eta

    if Power < 22000:
        motor_power = 1.25*Power
    elif (Power >=22000) and (Power <= 55000):
        motor_power = 1.15*Power
    else:
        motor_power = 1.1*Power

    Motor_rating = standard_iec_motor(motor_power)

    return Power_hydraulic, Power, Motor_rating
