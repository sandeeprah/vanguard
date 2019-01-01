import pandas as pd
from marshmallow import pprint
import CoolProp.CoolProp as CP
import math
import cmath
from techlib.mathutils import cubic_solve, linear_interp, linarray_interp, getindex
from techlib.thermochem.nelsonobert import nelobdatalow, nelobdatahigh
from collections import OrderedDict
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
R = 8.314

def mixture_props(mixture, P=None, T=None):
    MW_mix = 0
    Pc_mix = 0
    Tc_mix = 0
    ω_mix = 0
    Pr_mix = 0
    Tr_mix = 0
    Cp0mass_mix = 0
    Cp0molar_mix = 0
    normalise(mixture)
    properties = OrderedDict()

    for component in mixture:
        fluid = component["fluid"]
        y_component = component["molefraction"]
        # Molecular Weight averaging
        MW_specie = CP.PropsSI('M', fluid)
        MW_mix += MW_specie*y_component
        #Critical Pressure averaging
        Pc_specie = CP.PropsSI('Pcrit', fluid)
        Pc_mix += Pc_specie*y_component
        #Critical Temperature averaging
        Tc_specie = CP.PropsSI('Tcrit', fluid)
        Tc_mix += Tc_specie*y_component

        ω_specie= CP.PropsSI("acentric", fluid)
        ω_mix += ω_specie*y_component

        if (P is not None) and (T is not None):
            Cp0mass = CP.PropsSI("Cp0mass", "P", P, "T", T, fluid)
            Cp0mass_mix += Cp0mass*y_component
            Cp0molar = CP.PropsSI("Cp0molar", "P", P, "T", T, fluid)
            Cp0molar_mix += Cp0molar*y_component

    MW_mix = round(MW_mix, 6)
    Pc_mix = round(Pc_mix, 1)
    Tc_mix = round(Tc_mix, 1)
    ω_mix = round(ω_mix, 4)

    if (Pc_mix ==0):
        Pc_mix = math.nan

    if (Tc_mix ==0):
        Tc_mix = math.nan

    if (MW_mix ==0):
        MW_mix = math.nan

    if (Cp0mass_mix ==0):
        Cp0mass_mix = math.nan

    if (Cp0molar_mix ==0):
        Cp0molar_mix = math.nan

    properties.update({"MW":MW_mix})
    properties.update({"Pcritical":Pc_mix})
    properties.update({"Tcritical":Tc_mix})
    properties.update({"acentric":ω_mix})

    if (P is not None) and (T is not None):

        try:
            Pr_mix = P/Pc_mix
            Tr_mix = T/Tc_mix
            Cv0mass_mix  = Cp0mass_mix - (R/ MW_mix)
            Cv0molar_mix = Cp0molar_mix - R
            k_mix = Cp0molar_mix/Cv0molar_mix

        except Exception as e:
            Pr_mix = math.nan
            Tr_mix = math.nan
            Cv0mass_mix  = math.nan
            Cv0molar_mix = math.nan
            k_mix = math.nan


        try:
            Z_mix_PR = Z_PengRobinson_mixture(mixture=mixture, P=P, T=T)
        except Exception:
            Z_mix_PR = math.nan

        try:
            Z_mix_LKP = Z_LeeKesler_mixture(mixture=mixture, P=P, T=T)
        except Exception:
            Z_mix_LKP = math.nan

        try:
            Z_mix_NO = Z_NelsonObert_mixture(mixture=mixture, P=P, T=T)
        except Exception:
            Z_mix_NO = math.nan



        Pr_mix = round(Pr_mix, 4)
        Tr_mix = round(Tr_mix, 4)
        Z_mix_PR = round(Z_mix_PR, 4)
        Z_mix_LKP = round(Z_mix_LKP, 4)
        Z_mix_NO = round(Z_mix_NO, 4)

        Cp0mass_mix = round(Cp0mass_mix, 1)
        Cv0mass_mix = round(Cv0mass_mix, 1)
        Cp0molar_mix = round(Cp0molar_mix, 1)
        Cv0molar_mix = round(Cv0molar_mix, 1)
        k = Cp0molar_mix/(Cp0molar_mix - 8.314)
        k = round(k,2)


        properties.update({"Pr":Pr_mix})
        properties.update({"Tr":Tr_mix})
        properties.update({"Cp0mass":Cp0mass_mix})
        properties.update({"Cp0molar":Cp0molar_mix})
        properties.update({"Cv0mass":Cv0mass_mix})
        properties.update({"Cv0molar":Cv0molar_mix})
        properties.update({"k":k})
        properties.update({"Z_PR":Z_mix_PR})
        properties.update({"Z_LKP":Z_mix_LKP})
        properties.update({"Z_NO":Z_mix_NO})

    return properties





def normalise(mixture):
        sigma_molfrac = 0
        for component in mixture:
            molfrac = component["molefraction"]
            sigma_molfrac += molfrac

        if (sigma_molfrac !=0):
            for component in mixture:
                component["molefraction"] = component["molefraction"]/sigma_molfrac


def Z_PengRobinson_mixture(mixture, P, T):
    try:
        mixData = mixingData(mixture)
        amix, bmix = pengRobinsonMixing(mixData,T)
        Z = solvePengRobinson(amix, bmix, P, T)
        if (amix==0 and bmix==0):
            Z = math.nan
    except Exception:
        Z = math.nan

    return Z


def pengRobinsonMixing(mixData, T):
    y = []
    a = []
    b = []
    for component in mixData:
        molefrac = component["y"]
        y.append(molefrac)
        Pc = component["Pc"]
        Tc = component["Tc"]
        omega = component["omega"]

        ω = omega
        Tr = T/Tc
        κ = 0.37464 + 1.54226*ω - 0.26992*pow(ω,2)
        α = pow(1 + κ*(1 - math.sqrt(Tr)), 2)
        _a = 0.45724*(pow(R*Tc,2)/Pc)*α
        a.append(_a)
        _b = 0.07780*R*Tc/Pc
        b.append(_b)

    n = len(y)
    amix = 0
    for i in range(0,n):
        for j in range(0,n):
            amix += y[i]*y[j]*math.sqrt(a[i]*a[j])

    bmix = 0
    for i in range(0,n):
        bmix += y[i]*b[i]

    return amix, bmix


def Z_PengRobinson(Pc, Tc, omega, P, T):
    '''
    This function returns compressibility factors based on Peng-Robinson Equation of State
    Arguments and Units
    -------------------
    Pc : Critical Pressure in Pa
    Tc : Critical Temperature in K
    omega = Acentric Factor
    P : Pressure in Pa
    T : Temperature in K
    '''

    ω = omega
    Tr = T/Tc
    κ = 0.37464 + 1.54226*ω - 0.26992*pow(ω,2)
    α = pow(1 + κ*(1 - math.sqrt(Tr)), 2)
    a = 0.45724*(pow(R*Tc,2)/Pc)*α
    b = 0.07780*R*Tc/Pc
    Z = solvePengRobinson(a, b, P, T)

    return Z

def solvePengRobinson(a,b,P,T):
    A = a*P/pow(R*T,2)
    B = b*P/(R*T)
    C3 = 1
    C2 = -(1-B)
    C1 = A - 3*pow(B,2) -2*B
    C0 = -(A*B -pow(B,2) -pow(B,3))

    root1, root2, root3 = cubic_solve(C3, C2, C1, C0)
    real_root=[]

    if (root1.imag==0):
        real_root.append(root1.real)
    if (root2.imag==0):
        real_root.append(root2.real)
    if (root3.imag==0):
        real_root.append(root3.real)
    Z = max(real_root)
    return Z


def Z_LeeKesler_mixture(mixture, P, T):
    mixData = mixingData(mixture)
    Pc_mix, Tc_mix, omega_mix  = kaysMixing(mixData)
    Z = Z_LeeKesler(Pc_mix, Tc_mix, omega_mix, P, T)
    return Z


def Z_LeeKesler(Pc, Tc, omega, P, T):
    '''
    This function returns compressibility factors based on Lee Kesler Equation of State

    Arguments and Units
    -------------------
    Pc : Critical Pressure in Pa
    Tc : Critical Temperature in K
    omega = Acentric Factor
    P : Pressure in Pa
    T : Temperature in K
    '''

    Pr = P/Pc
    Tr = T/Tc
    Z = Z_LeeKesler_reduced(Pr, Tr, omega)
    return Z


def Z_LeeKesler_reduced(Pr, Tr, omega):
    '''
    This function returns compressibility factors based on Lee Kesler Equation of State

    Arguments and Units
    -------------------
    Pr : Reduced Pressure (= P/Pcritical)
    Tr : Reduced Temperature (= T/Tcritical)
    omega = Acentric Factor
    '''

#    print('Pc :' + str(Pc))
#    print('Tc :' + str(Tc))


    my_file = os.path.join(THIS_FOLDER, 'LeeKesler_Z0.csv')
    Z0df = pd.read_csv(my_file)
    Z0df = Z0df.set_index('T')

    pr_list = Z0df.columns.tolist()
    tr_list = Z0df.index.tolist()

    prindex_lower, prindex_higher =  getindex(pr_list, Pr)
    trindex_lower, trindex_higher =  getindex(tr_list, Tr)

    pr_lower = float(pr_list[prindex_lower])
    pr_higher = float(pr_list[prindex_higher])
    tr_lower = float(tr_list[trindex_lower])
    tr_higher = float(tr_list[trindex_higher])

    Z0_trl_prl = Z0df.iat[trindex_lower, prindex_lower]
    Z0_trl_prh = Z0df.iat[trindex_lower, prindex_higher]
    Z0_trh_prl = Z0df.iat[trindex_higher, prindex_lower]
    Z0_trh_prh = Z0df.iat[trindex_higher, prindex_higher]

    Z0_trl = linear_interp(Pr, pr_lower, Z0_trl_prl, pr_higher, Z0_trl_prh)
    Z0_trh = linear_interp(Pr, pr_lower, Z0_trh_prl, pr_higher, Z0_trh_prh)
    Z0 = linear_interp(Tr, tr_lower, Z0_trl, tr_higher, Z0_trh)

    my_file = os.path.join(THIS_FOLDER, 'LeeKesler_Z1.csv')
    Z1df = pd.read_csv(my_file)
    Z1df = Z1df.set_index('T')

    pr_list = Z1df.columns.tolist()
    tr_list = Z1df.index.tolist()

    prindex_lower, prindex_higher =  getindex(pr_list, Pr)
    trindex_lower, trindex_higher =  getindex(tr_list, Tr)

    pr_lower = float(pr_list[prindex_lower])
    pr_higher = float(pr_list[prindex_higher])
    tr_lower = float(tr_list[trindex_lower])
    tr_higher = float(tr_list[trindex_higher])

    Z1_trl_prl = Z1df.iat[trindex_lower, prindex_lower]
    Z1_trl_prh = Z1df.iat[trindex_lower, prindex_higher]
    Z1_trh_prl = Z1df.iat[trindex_higher, prindex_lower]
    Z1_trh_prh = Z1df.iat[trindex_higher, prindex_higher]

    Z1_trl = linear_interp(Pr, pr_lower, Z1_trl_prl, pr_higher, Z1_trl_prh)
    Z1_trh = linear_interp(Pr, pr_lower, Z1_trh_prl, pr_higher, Z1_trh_prh)
    Z1 = linear_interp(Tr, tr_lower, Z1_trl, tr_higher, Z1_trh)

    Z = Z0 + omega*Z1

    #print('Z :' + str(Z))
    #print('Z0 :' + str(Z0))
    #print('Z1 :' + str(Z1))

    return Z


def Z_NelsonObert_mixture(mixture, P, T):
    mixData = mixingData(mixture)
    Pc_mix, Tc_mix, omega_mix  = kaysMixing(mixData)
    Z = Z_NelsonObert(Pc_mix, Tc_mix,P, T)
    return Z


def Z_NelsonObert(Pc, Tc, P, T):
    '''
    This function returns compressibility factors based on Nelson Obert Generalised compressibility Charts

    Arguments and Units
    -------------------
    Pc : Critical Pressure in Pa
    Tc : Critical Temperature in K
    P : Pressure in Pa
    T : Temperature in K
    '''

    Pr = P/Pc
    Tr = T/Tc
    Z = Z_NelsonObert_reduced(Pr, Tr)
    return Z


def Z_NelsonObert_reduced(Pr,Tr):
    '''
    This function returns compressibility factors using Nelson Obert Generalised Compressibility Charts

    Arguments and Units
    -------------------
    Pr : Reduced Pressure (= P/Pcritical)
    Tr : Reduced Temperature (= T/Tcritical)
    '''


    if ((Pr <= 0.09) and (Tr <=2)):
            nelobdata = nelobdatalow
    else:
            nelobdata = nelobdatahigh

    ncurves = len(nelobdata)

    #try:

    lindex=0
    for i in range(0, ncurves):
            if (nelobdata[i][0] > Tr):
                    lindex = i-1
                    break

    tr_lower = nelobdata[lindex][0]
    tr_lower_curve = nelobdata[lindex][1]
    tr_higher = nelobdata[lindex+1][0]
    tr_higher_curve = nelobdata[lindex+1][1]

    x, y = zip(*tr_lower_curve)
    Z_lower = linarray_interp(x,y,Pr)

    x, y = zip(*tr_higher_curve)
    Z_higher = linarray_interp(x,y,Pr)

    x = [tr_lower, tr_higher]
    y = [Z_lower, Z_higher]
    Z = linarray_interp(x,y, Tr)


    #except:
    #    Z = None
    return Z



def kaysMixing(mixData):
    sigma_y = 0
    Pc_mix = 0
    Tc_mix = 0
    omega_mix = 0

    for component in mixData:
        y = component["y"]
        Pc = component["Pc"]
        Tc = component["Tc"]
        omega = component["omega"]

        sigma_y += y
        Pc_mix += Pc*y
        Tc_mix += Tc*y
        omega_mix += omega*y

    Pc_mix = Pc_mix/sigma_y
    Tc_mix = Tc_mix/sigma_y
    omega_mix = omega_mix/sigma_y

    return Pc_mix, Tc_mix, omega_mix


def mixingData(mixture):
    mixingData = []
    for component in mixture:
        fluid = component["fluid"]
        y = component["molefraction"]
        Pc = CP.PropsSI("Pcrit", fluid)
        Tc = CP.PropsSI("Tcrit", fluid)
        omega = CP.PropsSI("acentric", fluid)
        component_data = {"fluid": fluid, "y": y, "Pc":Pc, "Tc":Tc, "omega":omega}
        mixingData.append(component_data)
    return mixingData
