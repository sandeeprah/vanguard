import os
from math import *
import pandas as pd
import CoolProp.CoolProp as CP
from techlib.mechanical.utils.psychrometrics import humidityRatio
from techlib.mathutils import linarray_interp, linear_interp


def gasfuelProperties(gasfuel, composition_type):
    mass_total = 0
    moles_total = 0
    h_L_total = 0
    Cp_total = 0
    air_total = 0
    CO2_total = 0
    H2O_total = 0
    N2_total = 0

    fraction_normalised = []
    fraction_total = 0
    for component in gasfuel:
        percent = component['percent']

        fraction = percent/100

        fluid = component['fluid']
        MW, h_L, Cp, specificAir, specificCO2, specificH2O, specificN2 = componentProperties(fluid)

        if composition_type =='mole_percent':
            mass = MW*fraction
            moles = fraction
        else:
            mass = fraction
            moles = mass/MW

        mass_total = mass_total + mass
        moles_total = moles_total + moles

        h_L_total = h_L_total + mass*h_L
        Cp_total = Cp_total + mass*Cp
        air_total = air_total + mass*specificAir
        CO2_total = CO2_total + mass*specificCO2
        H2O_total = H2O_total + mass*specificH2O
        N2_total = N2_total + mass*specificN2

    MW = mass_total/moles_total
    h_L = h_L_total/mass_total
    Cp = Cp_total/mass_total
    air_reqd = air_total/mass_total
    CO2_formed = CO2_total/mass_total
    H2O_formed = H2O_total/mass_total
    N2_formed = N2_total/mass_total
    return MW, h_L, Cp, air_reqd, CO2_formed, H2O_formed, N2_formed

def componentProperties(componentName):
    data_file = "properties.csv"
    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        properties_df = pd.read_csv(data_file_path)
        properties_df = properties_df.set_index('Component')
        MW = properties_df.loc[componentName, "MW"]/1000
        h_L = properties_df.loc[componentName, "LHV"]*1000
        Cp = properties_df.loc[componentName, "Cp"]*1000
        specificAir = properties_df.loc[componentName, "specificAir"]
        specificCO2 = properties_df.loc[componentName, "specificCO2"]
        specificH2O = properties_df.loc[componentName, "specificH2O"]
        specificN2 = properties_df.loc[componentName, "specificN2"]
    except Exception as e:
        raise e
        print(str(e))
#        raise Exception("Unknown component. Properties could not be found. for " + componentName)

    return MW, h_L, Cp, specificAir, specificCO2, specificH2O, specificN2


def airMoistureContent(T, RH):
    Patm = 101325
    X = humidityRatio(Patm,T,RH)
    X_wet = X/(1+X)
    return X_wet

def wetAirRequired(air_reqd, X_wet):
    wet_air_reqd = air_reqd/(1-X_wet)
    return wet_air_reqd

def excessAir(flue_O2, air_reqd, N2_formed, CO2_formed, H2O_formed_RHcorrected, moisture, sampling_basis):
    if (sampling_basis=='dry'):
        A = (N2_formed/28) + (CO2_formed/44)
        B = 1
        EA = 28.85*flue_O2*A/(20.95 - flue_O2*B)
    else:
        A = (N2_formed/28) + (CO2_formed/44) + (H2O_formed_RHcorrected/18)
        B = 1.6028*(moisture/air_reqd) + 1
        EA = 28.85*flue_O2*A/(20.95 - flue_O2*B)
    return EA

def excessAir_pc(excess_Air, air_reqd):
    EA_pc = excess_Air*100/air_reqd
    return EA_pc

def H2OformedEAcorrected(excess_Air_pc, moisture, H2O_formed_RHcorrected):
    water = (excess_Air_pc/100)*moisture + H2O_formed_RHcorrected
    return water

def flueMassicHeatContent(CO2_formed, H2O_formed, N2_formed, excess_Air, Texit_flue):
    Patm = 101325
    Tdatum = 273.15 + 15

    h_CO2 = getEnthalphy('CarbonDioxide', Texit_flue)
    h_H2O = getEnthalphy('Water',Texit_flue)
    h_N2 = getEnthalphy('Nitrogen',Texit_flue)
    h_EA = getEnthalphy('Air', Texit_flue)

    H_CO2 = h_CO2*CO2_formed
    H_H2O = h_H2O*H2O_formed
    H_N2 = h_N2*N2_formed
    H_EA = h_EA*excess_Air

    H_total = H_CO2 + H_H2O + H_N2 + H_EA

    return H_total

def getEnthalphy(component,T):

    try:
        P = 101325
        h =  CP.PropsSI('H', 'T',T, 'P',P, component) - CP.PropsSI('H', 'T', 288, 'P',P, component)

        if (component=='Water'):
            h =  CP.PropsSI('H', 'T',T, 'P',P, component) - 2464900 -65000

            '''
            data_file = "enthalpy_water_vapor.csv"
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            data_file_path = os.path.join(THIS_FOLDER, data_file)
            enthalpy_df = pd.read_csv(data_file_path)
            T_array = enthalpy_df['T'].tolist()
            h_array = enthalpy_df['h'].tolist()
            T_C = T -273.15
            print("T_C is {}".format(T_C))
            h = linarray_interp(T_array,h_array,T_C)*1000
            '''
    except:
        h = nan

    return h

def radiationLoss(loss_radiation, h_L):
    h_r = (loss_radiation/100)*h_L
    return h_r

def enthalpySteam(P,T):
    h_m = CP.PropsSI('H','T', T, 'P', P, 'Water')
    return h_m

def netThermalEfficiency(h_L, delh_a, delh_f, delh_m, h_r, h_s):
    heat_input = h_L + delh_a + delh_f + delh_m
    heat_lost = h_r + h_s
    heat_absorbed = heat_input - heat_lost
    net_efficiency = (heat_absorbed/heat_input)*100
    return net_efficiency

def grossThermalEfficiency(h_L, h_H, delh_a, delh_f, delh_m, h_r, h_s):
    Nr = (h_L + delh_a +  delh_f+ delh_m) - (h_r + h_s)
    Dr = h_H + delh_a + delh_f + delh_m
    gross_efficiency = (Nr/Dr)*100
    return gross_efficiency

def fuelEfficiency(h_L, delh_a, delh_f, delh_m, h_r, h_s):
    heat_input = h_L + delh_a + delh_f + delh_m
    heat_lost = h_r + h_s
    heat_absorbed = heat_input - heat_lost
    fuel_efficiency = (heat_absorbed/h_L)*100
    return fuel_efficiency

def getHHV(LHV, H2O_formed):
    C = 2464.9 #kJ/kg
    HHV = LHV + H2O_formed*C*1000
    return HHV
