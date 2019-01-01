import math

def Pws(T):
    '''
    Gives water vapor pressure as per IAPWS 1995 formula

    '''
    Tc = 647.096 #Kelvin
    Pc = 22.064e6 #Pa

    # Coefficients
    C1 = -7.85951783
    C2 = 1.84408259
    C3 = -11.7866497
    C4 = 22.6807411
    C5 = -15.9618719
    C6 = 1.80122502

    v = 1 - (T/Tc)

    k1 = (Tc/T)*(C1*v + C2*math.pow(v, 1.5) + C3*math.pow(v, 3) + C4*math.pow(v, 3.5) + C5*math.pow(v, 4) + C6*math.pow(v, 7.5))
    k2 = math.exp(k1)
    _Pws = Pc*k2
    return _Pws

def humidityratio(T, Pamb, RH):
    Pwsat = Pws(T)
    Pw = (RH/100.0)*Pwsat
    x = 0.62198*(Pw)/(Pamb - Pw)
    return x
