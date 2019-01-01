from math import *

def PFC_compensation(power_P,pf_actual,pf_desired):
    phi_actual = acos(pf_actual)
    phi_desired = acos(pf_desired)
    tan_actual = tan(phi_actual)
    tan_desired = tan(phi_desired)
    C = power_P*(tan_actual - tan_desired)
    return C


def phase_parameters(VLL, pf, I=None, kW=None, kVA=None, kVAr=None):
    phi = acos(pf)
    if (I is not None):
        kW = sqrt(3)*VLL*I*pf/1000
        kVA = kW/pf
        kVAr = sin(phi)*kVA
    elif(kW is not None):
        kVA = kW/pf
        I = (kW*1000)/(sqrt(3)*VLL*pf)
        kVAr = sin(phi)*kVA
    elif(kVA is not None):
        kW = kVA*pf
        kVAr = sin(phi)*kVA
        I = (kW*1000)/(sqrt(3)*VLL*pf)
    elif(kVAr is not None):
        kVA = kVAr/sin(phi)
        kW = kVA*pf
        I = (kW*1000)/(sqrt(3)*VLL*pf)
    else:
        raise Exception("Sufficient Inputs not provided for Calculation. Specify VLL, pf and one of I, kW or kVAr")


    return I, kW, kVA, kVAr
