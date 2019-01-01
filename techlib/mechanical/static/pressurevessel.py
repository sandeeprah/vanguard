import json
import os
from math import *
import pandas as pd
from techlib.mathutils import linarray_interp
from collections import OrderedDict

def getAllowableStress(materialSpec, T):
    data_file = "ASME_VIII_table_1A.csv"

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        stress_df = pd.read_csv(data_file_path)
        stress_df = stress_df.set_index('MatlSpec')
        matl_stress = stress_df.loc[materialSpec]
        matl_stress = matl_stress.drop(['Density','St', 'Sy', 'Tmax', 'Chart'])
        temperature_values = matl_stress.index.tolist()
        stress_values = matl_stress.values

        for index, val  in enumerate(temperature_values):
            temperature_values[index] = float(val)

        # convert K to F
        T_C = T - 273.15
        S_MPa = linarray_interp(temperature_values,stress_values,T_C)
        S = S_MPa*1e6

    except Exception as e:
#        raise e
        raise Exception('S could not be determined')


    return S


def pressureHydroUG99(MAWP, S, St):
    Phydro = 1.3*MAWP*(St/S)
    return Phydro

# Equations for Cylinder
# ======================
# ======================


def thicknessCylinderCircumStress(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin cylinder equations are to be used or thick cylinders as per supplementary equations of ASME
    if (P <= 0.385*S*E):
        condn_P = True
        if (R is not None):
            t = (P*R)/(S*E-0.6*P)
            eqn_ref = "UG-27(1)"
        else:
            tc = (P*Ro)/(S*E+0.4*P)
            eqn_ref = "Appendix 1-1(1)"
    else:
        condn_P = False
        if (R is not None):
            t = R*(exp(P/(S*E))-1)
            eqn_ref = "Appendix 1-2(1)"
        else:
            t = Ro*(1-exp(-P/(S*E)))
            eqn_ref = "Appendix 1-2(1)"

    return t, condn_P, eqn_ref


def pressureCylinderCircumStress(S, E, t, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # Get the inner radius
    if (R is not None):
        Ri = R
    else:
        Ri = Ro - t

    if (t <= (Ri/2)):
        condn_t = True
        if (R is not None):
            P = (S*E*t)/(R+0.6*t)
            eqn_ref = "UG-27(1)"
        else:
            P = (S*E*t)/(Ro-0.4*t)
            eqn_ref = "Appendix 1-1(1)"
    else:
        condn_t = False
        if (R is not None):
            P = S*E*log((R+t)/R)
            eqn_ref = "Appendix 1-2(2)"
        else:
            P = S*E*log(Ro/(Ro-t))
            eqn_ref = "Appendix 1-2(2)"

    return P, condn_t, eqn_ref


def thicknessCylinderLongStress(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin cylinder equations are to be used or thick cylinders as per supplementary equations of ASME
    if (P <= 1.25*S*E):
        condn_P = True
        if (R is not None):
            t = (P*R)/(2*S*E+0.4*P)
            eqn_ref = "UG-27(2)"
        else:
            t = (P*Ro)/(2*S*E+1.4*P)
            eqn_ref = "UG-27(2) [derived]"
    else:
        condn_P = False
        Z = (P/(S*E)) + 1
        if (R is not None):
            t = R*(sqrt(Z) - 1)
            eqn_ref = "Appendix 1-2(3)"
        else:
            t = Ro*(sqrt(Z)-1)/sqrt(Z)
            eqn_ref = "Appendix 1-2(3)"

    return t, condn_P, eqn_ref


def pressureCylinderLongStress(S, E, t, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # Get the inner radius
    if (R is not None):
        Ri = R
    else:
        Ri = Ro - t

    if (t <= (Ri/2)):
        condn_t = True
        if (R is not None):
            P = (2*S*E*t)/(R-0.4*t)
            eqn_ref = "UG-27(2)"
        else:
            P = (2*S*E*t)/(Ro-1.4*t)
            eqn_ref = "UG-27(2) [derived]"
    else:
        condn_t = False
        if (R is not None):
            Z = ((R+t)/R)**2
        else:
            Z = (Ro/(Ro-t))**2

        P = S*E*(Z-1)
        eqn_ref = "Appendix 1-2(4)"

    return P, condn_t, eqn_ref

# Equations for Sphere
# ====================
# ====================

def thicknessSphere(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin spherical equations are to be used or thick spherical  as per supplementary equations of ASME
    if (P <= 0.665*S*E):
        condn_Ps = True
        if (R is not None):
            ts = (P*R)/(2*S*E -0.2*P)
            eqn_ref = "UG-27(3)"
        else:
            ts = (P*Ro)/(2*S*E +0.8*P)
            eqn_ref = "Appendix 1-1(2)"
    else:
        condn_Ps = False
        if (R is not None):
            ts = R*(exp((0.5*P)/(S*E)) - 1)
            eqn_ref = "Appendix 1-3(1)"
        else:
            ts = Ro*(1 - exp((-0.5*P)/(S*E)))
            eqn_ref = "Appendix 1-3(1)"

    return ts, condn_Ps, eqn_ref

def pressureSphere(S, E, t, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (t <= 0.356*R):
        condn_ts = True
        if (R is not None):
            Ps = (2*S*E*t)/(R+0.2*t)
            eqn_ref = "UG-27(3)"
        else:
            Ps = (2*S*E*t)/(Ro-0.8*t)
            eqn_ref = "Appendix 1-1(2)"
    else:
        condn_ts = False

        if (R is not None):
            Ps = 2.0*S*E*log((R+t)/R)
            eqn_ref = "Appendix 1-3(2)"
        else:
            Ps = 2.0*S*E*log(Ro/(Ro-t))
            eqn_ref = "Appendix 1-3(2)"

    return Ps, condn_ts, eqn_ref


# Equations for Formed Head
# =========================
# =========================

def thicknessEllipsoidalHead(S, E, P, D=None, Do=None,  ar = 2):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # evaluate the K factor
    K = (1/6)*(2 + ar**2)

    if (D is not None):
        t = (P*D*K)/(2*S*E - 0.2*P)
        eqn_ref = "Appendix 1-4(1)"
    else:
        t = (P*Do*K)/(2*S*E + 2*P*(K-0.1))
        eqn_ref = "Appendix 1-4(2)"

    return t, K, eqn_ref


def pressureEllipsoidalHead(S, E, t, D=None, Do=None, ar = 2):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # evaluate the K factor
    K = (1/6)*(2 + ar**2)

    if (D is not None):
        P = (2*S*E*t)/(K*D + 0.2*t)
        eqn_ref = "Appendix 1-4(1)"
    else:
        P = (2*S*E*t)/(K*Do -2*t(K-0.1))
        eqn_ref = "Appendix 1-4(2)"

    return P, K, eqn_ref


def thicknessTorisphericalHead(S, E, P, Do, L, r):
    # check for validity of L and r
    if (L > Do):
        raise Exception("Inner crown radius (L) should not be greater than outer skirt diameter (Do)")
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than 0.06 times outer skirt diamter (Do)")

    # evaluate the M factor
    M = (1/4)*(3 + sqrt(L/r))
    t = (P*L*M)/(2*S*E - 0.2*P)
    eqn_ref = "Appendix 1-4(3)"

    return t, M, eqn_ref


def pressureTorisphericalHead(S, E, t, Do, L, r ):
    # check for validity of L and r
    if (L > Do):
        raise Exception("Inner crown radius (L) should not be greater than outer skirt diameter (Do)")
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than 0.06 times outer skirt diamter (Do)")

    # evaluate the M factor
    M = (1/4)*(3 + sqrt(L/r))
    P = (2*S*E*t)/(L*M + 0.2*t)
    eqn_ref = "Appendix 1-4(3)"

    return P, M, eqn_ref

def thicknessHemisphericalHead(S, E, P, D):
    R = D/2
    t, condn_P, eqn_ref = thicknessSphere(S, E, P, R)
    return t, condn_P, eqn_ref

def pressureHemisphericalHead(S, E, t, D):
    R = D/2
    MAWP, condn_t, eqn_ref = pressureSphere(S, E, t, R)
    return MAWP, condn_t, eqn_ref

def thicknessConicalHead(S, E, P, D=None, Do=None, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check the validity of alpha
    if (alpha > 0.524):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    if (D is not None):
        t = (P*D)/(2*cos(alpha)*(S*E - 0.6*P))
        eqn_ref = "Appendix 1-4(5)"
    else:
        t = (P*Do)/(2*cos(alpha)*(S*E + 0.4*P))
        eqn_ref = "Appendix 1-4(5)"

    return t, eqn_ref

def pressureConicalHead(S, E, t, D=None, Do=None, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'D' or 'Do' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'D' and 'Do' should not be provided")

    #check the validity of P
    if (alpha > 0.524):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    if (D is not None):
        P = (2*S*E*t*cos(alpha))/(D + 1.2*t*cos(alpha))
        eqn_ref = "Appendix 1-4(5)"
    else:
        P = (2*S*E*t*cos(alpha))/(Do - 0.8*t*cos(alpha))
        eqn_ref = "Appendix 1-4(5)"

    return P, eqn_ref


def thicknessToriConicalHead(S, E, P, Do, tn, Di, r, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    # check for validity of L and r
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than 0.06 times outer skirt diamter (Do)")

    if (r < 3*tn):
        raise Exception("Knuckle radius (r) should not be less than three times knuckle thickness")

    #check the validity of alpha
    if (alpha > 30):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    tcone, eqn_ref_cone = thicknessConicalHead(S, E, P, D=Di, alpha=alpha)
    L = Di/(2*cos(alpha))
    tknuckle,M, eqn_ref_knuckle = thicknessTorisphericalHead(S, E, P, Do, L, r)

    t = max([tcone,tknuckle])
    return t, tcone, eqn_ref_cone, tknuckle, L, M, eqn_ref_knuckle


def pressureToriConicalHead(S, E, t, Do, tn, Di, r, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    # check for validity of L and r
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than 0.06 times outer skirt diamter (Do)")

    if (r < 3*tn):
        raise Exception("Knuckle radius should not be less than three times knuckle thickness")

    #check the validity of alpha
    if (alpha > 30):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    Pcone, eqn_ref_cone = pressureConicalHead(S, E, t, D=Di, alpha=alpha)
    L = Di/(2*cos(alpha))
    Pknuckle, M, eqn_ref_knuckle = pressureTorisphericalHead(S, E, t, Do, L, r )
    P = min([Pcone,Pknuckle])

    return P, Pcone, eqn_ref_cone, Pknuckle, L, M, eqn_ref_knuckle


# volumes and weight formulas

#material weight for cylindrical shell
def cylindricalShellVolume(tn, L, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (D is None):
        D = Do -2*tn

    R = D/2
    Vinner = pi*(R**2)*L

    Ro = R + tn
    Vouter = pi*(Ro**2)*L

    matlVol = Vouter - Vinner

    return Vinner, matlVol


#material weight for spherical shell
def sphericalShellVolume(tn, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (D is None):
        D = Do - 2*tn

    R  = D/2
    Ro = R + tn
    Vinner = (4/3)*pi*(R**3)
    Vouter = (4/3)*pi*(Ro**3)

    matlVol = Vouter - Vinner
    return Vinner, matlVol

# internal and material volume for ellipsoidal head
def volumeEllipsoidalHead(tn, ar, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # get the inner diameter if not available
    if (D is None):
        D = Do - 2*tn

    # get the inner radius
    R = D/2
    # get inner height using aspect ratio provided
    h = R/ar
    # volume of an ellipsoid is V=(4/3)*pi*a*b*c where a,b,c are semi principal axis
    # for the inner semi-ellipsoid
    a = R
    b = R
    c = h
    Vinner = (2/3)*pi*a*b*c
    # for the outer semi-ellipsoid
    ao = R + tn
    bo = R + tn
    co = h + tn
    Vouter = (2/3)*pi*ao*bo*co
    # net volume is obtained by subtracting the inner volume from outer volume
    matlVol = Vouter - Vinner
    return Vinner, matlVol

# internal and material volume for hemispherical head
def volumeHemisphericalHead(tn, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (D is None):
        D = Do - 2*tn

    R  = D/2
    Ro = R + tn
    Vinner = (4/6)*pi*(R**3)
    Vouter = (4/6)*pi*(Ro**3)

    matlVol = Vouter - Vinner
    return Vinner, matlVol


# internal and material volume for torispherical head
def volumeTorisphericalHead(tn, L, r, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (D is None):
        D = Do -2*tn

    Vinner = volToriDome(L,r,D)
    Lo = L + tn
    ro = r + tn
    Do = D + 2*tn

    Vouter = volToriDome(Lo, ro, Do)
    matlVol = Vouter - Vinner
    return Vinner, matlVol


# internal and material volume for conical head
def volumeConicalHead(tn, alpha, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (D is None):
        D = Do -2*tn

    R = D/2
    # get cone height h
    h = R/tan(alpha)
    Vinner = (1/3)*pi*(R**2)*h

    Ro = R + tn
    ho = Ro/tan(alpha)
    Vouter = (1/3)*pi*(Ro**2)*ho

    matlVol = Vouter - Vinner
    return Vinner, matlVol


# internal and material volume for toriconical head
def volumeToriconicalHead(tn, r, alpha, D=None, Do=None):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (D is None):
        D = Do -2*tn

    R = D/2
    # get cone height h
    h = R/tan(alpha)
    Vinner = (1/3)*pi*(R**2)*h

    Ro = R + tn
    ho = Ro/tan(alpha)
    Vouter = (1/3)*pi*(Ro**2)*ho

    matlVol = Vouter - Vinner
    return Vinner, matlVol

def volToriDome(R,a,D):
    '''
    R : inner crown radius
    a : knuckle radius
    D : inner dome diameter at base
    '''

    # get c the distance between center of torus to center of torus tube
    c = (D/2) - a

    # get the inner height of the head
    h = R - sqrt((a+c-R)*(a-c-R))

    # get the volume
    u = 2*h*(R**2)
    v = 2*(a**2) + c**2 + 2*a*R
    w = R - h
    x = 3*(a**2)*c
    y = asin((R-h)/(R-a))
    Volume = (pi/3)*(u - v*w +x*y)
    return Volume
