from math import *

def moistAirDensity(P, T, RH):
    W = humidityRatio(P,T,W)
    MWda = 0.02897
    MWw = 0.018
    R = 8.314
    Rda = R/MWda
    Rw = R/MWw
    rho_da = P/(Rda*T)
    rho_ma = rho_da*(1+W)/(1+W*(Rw/Rda))
    return rho_ma

def humidityRatio(P, T, RH):
    Pws = Pw_sat(T)
    Pw = Pws*RH/100 # get partial pressure of water vapor in Pa
    W = 0.62198*Pw/(P-Pw) # get humidity ratio
    return W

def humidityRatio_molar(P, T, RH):
    Pws = Pw_sat(T)
    Pw = Pws*RH/100 # get partial pressure of water vapor in Pa
    Xw_by_Xa = Pw/(P-Pw) # get humidity ratio
    return Xw_by_Xa

def Pw_sat(T):
    '''
    Returns vapor pressure of water vapour for a given temperature
    '''

    if (T < 273.15):
        C1 = -5.6745359e3
        C2 = 6.3925247e0
        C3 = -9.6778430e-3
        C4 = 6.2215701e-7
        C5 = 2.0747825e-9
        C6 = -9.4840240e-13
        C7 = 4.1635019e0
        ln_Pws = (C1/T) + C2 + C3*T + C4*pow(T,2) + C5*pow(T,3) + C6*pow(T,4) + C7*log(T)
    else:
        C8 = -5.8002206e3
        C9 = 1.3914993e0
        C10 = -4.8640239e-2
        C11 = 4.1764768e-5
        C12 = -1.4452093e-8
        C13 = 6.5459673e0
        ln_Pws = (C8/T) + C9 + C10*T + C11*pow(T,2) + C12*pow(T,3) + C13*log(T)

    Pws = exp(ln_Pws)

    return Pws
