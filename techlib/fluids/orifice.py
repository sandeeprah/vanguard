from math import *

def mflow_reservoir_orifice(Pi, Ti, Pe, MW, k, A, Cd):
    '''
    Pi : Pressure upstream of orifice
    Ti : Pressure upstream of orifice
    Pe : Pressure downstream of orifice
    k : specific heat ratio of gas
    rhoi : density of gas upstream of orifice
    A : area of restriction orifice
    Cd : Coefficient of Discharge
    '''

    rhoi = density(Pi,Ti,MW)

    f = k/(k - 1)
    r = Pe/Pi
    rc = (2/(k+1))**f
    if (r <= rc):
        isChoked = True
        r = rc
    else:
        isChoked = False
    v = sqrt(2*f*(Pi/rhoi)*(1-r**(1/f)))
    rhoe = rhoi*(r**(1/k))
    mflow = A*v*rhoe

    return v, mflow, isChoked


def density(P,T,MW):
    Ru = 8.314
    Rg = Ru/MW
    rho = P/(Rg*T)
    return rho
