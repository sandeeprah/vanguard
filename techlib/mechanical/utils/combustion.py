import os
from math import *
import pandas as pd
from techlib.mathutils import linarray_interp, linear_interp
from techlib.mechanical.utils.psychrometrics import humidityRatio_molar

def gasCombustion(gasfuel, fuel_as='mole_percent', flue_as='mole_per_fuelmole', excessAir=0, Pair=101325, Tair=298.15, RH=50):
    mass_total = 0
    moles_total = 0

    air_reqd_total = 0
    theoritical_air_reqd_total = 0
    CO2_formed_total = 0
    H2O_formed_total  = 0
    SO2_formed_total = 0
    N2_formed_total = 0


    #normalising the composition all percentages should add to 100
    percent_total = 0
    for component in gasfuel:
        percent_total = percent_total + component['percent']
    for component in gasfuel:
        component['percent'] = component['percent']*100/percent_total

    # all combustion analysis is done based on mole fraction
    for component in gasfuel:
        percent = component['percent']
        fraction = percent/100
        fluid = component['fluid']
        MW, O2_moles, air_moles, CO2_moles, H2O_moles, SO2_moles, N2_moles = combustionData(fluid)
        if fuel_as =='mole_percent':
            moles = fraction
            mass = MW*fraction
        else:
            mass = fraction
            moles = mass/MW

        mass_total = mass_total + mass
        moles_total = moles_total + moles
        theoritical_air_reqd_total = theoritical_air_reqd_total + moles*air_moles
        CO2_formed_total = CO2_formed_total + moles*CO2_moles
        H2O_formed_total = H2O_formed_total + moles*H2O_moles
        SO2_formed_total = SO2_formed_total + moles*SO2_moles
        N2_formed_total = N2_formed_total + moles*N2_moles + moles*air_moles*(1+excessAir/100)*0.791


    MW_fuel = mass_total/moles_total
    air_reqd_total = (1+excessAir/100)*theoritical_air_reqd_total
    O2_excess = theoritical_air_reqd_total*(excessAir/100)*0.209
    X = humidityRatio_molar(Pair,Tair,RH)
    moisture_moles = X*air_reqd_total
    H2O_formed_total = (H2O_formed_total+moisture_moles)

    # if mass composition is to be used then convert the products to mass equivalents and divide by the total mass of fuel gas
    if (flue_as=='mass_per_fuelmass'):
        MW_air = 28.96/1000
        MW_H2O = 18.0/1000
        MW_CO2 = 44/1000
        MW_SO2 = 64.1/1000
        MW_N2 = 28/1000
        MW_O2 = 32/1000
        air_reqd_total = air_reqd_total*MW_air/mass_total
        CO2_formed_total = CO2_formed_total*MW_CO2/mass_total
        H2O_formed_total = H2O_formed_total*MW_H2O/mass_total
        SO2_formed_total = SO2_formed_total*MW_SO2/mass_total
        N2_formed_total = N2_formed_total*MW_N2/mass_total
        O2_excess = O2_excess*MW_O2/mass_total


    if (flue_as=='mole_per_fuelmole'):
        air_reqd_total = air_reqd_total/moles_total
        CO2_formed_total = CO2_formed_total/moles_total
        H2O_formed_total = H2O_formed_total/moles_total
        SO2_formed_total = SO2_formed_total/moles_total
        N2_formed_total = N2_formed_total/moles_total
        O2_excess = O2_excess/moles_total


    return MW_fuel, air_reqd_total, CO2_formed_total, H2O_formed_total, SO2_formed_total, N2_formed_total, O2_excess


def combustionData(componentName):
    data_file = "gasdata.csv"
    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        properties_df = pd.read_csv(data_file_path)
        properties_df = properties_df.set_index('Component')

        MW = properties_df.loc[componentName, "MW"]/1000
        O2_moles = properties_df.loc[componentName, "O2_moles"]
        air_moles = O2_moles/0.209
        CO2_moles = properties_df.loc[componentName, "CO2_moles"]
        H2O_moles = properties_df.loc[componentName, "H2O_moles"]
        SO2_moles = properties_df.loc[componentName, "SO2_moles"]
        N2_moles = properties_df.loc[componentName, "N2_moles"]

    except Exception as e:
        raise Exception("Unknown component. Properties could not be found. for " + componentName)

    return MW, O2_moles, air_moles, CO2_moles, H2O_moles, SO2_moles, N2_moles


def getSOxEmission_ppmv(CO2_moles, H2O_moles, SO2_moles, N2_moles, O2_moles, O2_reference=3):
    total_moles = CO2_moles + H2O_moles + SO2_moles + N2_moles
    SO2_ppmv_wet = (SO2_moles*pow(10,6)/total_moles)
    Fm = 100/(100-H2H2O_formed_total)
    SO2_ppmv_dry = SO2_ppmv_wet
    Fo = (20.9 - O2_reference)/(20.9 - O2_measured_dry)

    return C

def emissionConversion(concentration_measured, from_units, to_units, MW=None, Ps=101325, Ts=298.15):
    Vmolar  = 22.41 #volume occupied by one mole of gas at NTP conditions

    if (from_units != to_units):
        if (from_units=='ppmv'):
            if MW is not None:
                Ku = MW*1000/Vmolar
            else:
                raise Exception('MW is required for emission conversion')
            concentration_base = concentration_measured*Ku
        if (from_units=='mg/Nm3'):
            concentration_base = concentration_measured
        if (from_units=='mg/Sm3'):
            Tn = 273.15
            Pn = 101325
            if (Ts is not None):
                Ft = Ts/Tn
            else:
                raise Exception('Ts is required for emission conversion')

            if (Ps is not None):
                Fp = Pn/Ps
            else:
                raise Exception('Ps is required for emission conversion')

            concentration_base = concentration_measured*Ft*Fp

        if (to_units=='ppmv'):
            if MW is not None:
                Ku = MW*1000/Vmolar
            else:
                raise Exception('MW is required for emission conversion')
            concentration = concentration_base/Ku
        if (to_units=='mg/Nm3'):
            concentration = concentration_base
        if (to_units=='mg/Sm3'):
            Tn = 273.15
            Pn = 101325
            if (Ts is not None):
                Ft = Tn/Ts
            else:
                raise Exception('Ts is required for emission conversion')

            if (Ps is not None):
                Fp = Ps/Pn
            else:
                raise Exception('Ps is required for emission conversion')

            concentration = concentration_base*Ft*Fp
    else:
        concentration = concentration_measured

    return concentration



def emissionCorrectionFactors(H2O_measured=None, O2_measured=None, O2_reference=3):
    if H2O_measured is not None:
        Fm = 100/(100-H2O_measured)
    else:
        Fm = 1 #moisture correction

    if (O2_measured is not None):
        O2_measured_dry = O2_measured*Fm
        Fo = (20.9 - O2_reference)/(20.9 - O2_measured_dry)
    else:
        Fo = 1 # oxygen_correction

    return Fm, Fo

def emissionCorrection(concentration, Fm, Fo):
    return concentration*Fm*Fo


def FlueGasSOx_concentration(CO2, H2O, SO2, N2, O2, flue_as='mole_per_fuelmole', units='ppmv', O2_reference=3, Ps=101325, Ts=298.15):
    if (flue_as=='mole_per_fuelmole'):
        CO2_moles = CO2
        H2O_moles = H2O
        SO2_moles = SO2
        N2_moles = N2
        O2_moles = O2
        moles_total = CO2_moles + H2O_moles + SO2_moles + N2_moles + O2_moles
    else:
        MW_CO2 = 44/1000
        MW_H2O = 18.0/1000
        MW_SO2 = 64.1/1000
        MW_N2 = 28/1000
        MW_O2 = 32/1000
        CO2_moles = CO2/MW_CO2
        H2O_moles = H2O/MW_H2O
        SO2_moles = SO2/MW_SO2
        N2_moles = N2/MW_N2
        O2_moles = O2/MW_O2
        moles_total = CO2_moles + H2O_moles + SO2_moles + N2_moles + O2_moles


    O2_measured = O2_moles*100/moles_total
    H2O_measured = H2O_moles*100/moles_total
    SO2_measured = SO2_moles*100/moles_total

    SO2_ppmv_wet = SO2_measured*pow(10,4)
    print("SO2_ppmv_wet is {}".format(SO2_ppmv_wet))
    SO2_concentration =  emissionConversion(SO2_ppmv_wet, 'ppmv', units, MW=0.0641, Ps=Ps, Ts=Ts)
    Fm, Fo = emissionCorrectionFactors(H2O_measured, O2_measured, O2_reference)
    SO2_concentration_dry_corrected = emissionCorrection(SO2_concentration, Fm, Fo)

    return SO2_concentration_dry_corrected
