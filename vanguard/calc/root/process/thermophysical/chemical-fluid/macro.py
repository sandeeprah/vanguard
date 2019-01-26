import math
import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    fluid = doc['input']['fluid']['_val']
    P = float(doc['input']['P']['_val'])
    T = float(doc['input']['T']['_val'])
    result = {}


    try:
        phase = CP.PhaseSI('T',T, 'P',P, fluid)
    except Exception as e:
        phase = ""
        doc['errors'].append("Failed to calculate 'phase' . Check Inputs")
    finally:
        doc['result'].update({'phase':{'_val' : phase}})

    try:
        MW = round(CP.PropsSI('M', fluid),5)
    except Exception as e:
        MW = math.nan
        doc['errors'].append("Failed to calculate 'MW' . Check Inputs")
    finally:
        doc['result'].update({'MW':{'_val' : str(MW), '_dim':'molecularMass'}})

    try:
        Pcritical = round(CP.PropsSI('Pcrit', 'T',T, 'P',P, fluid),1)
    except:
        Pcritical = math.nan
        doc['errors'].append("Failed to calculate 'Pcritical' . Check Inputs")
    finally:
        doc['result'].update({'Pcritical':{'_val' : str(Pcritical), '_dim':'pressure'}})

    try:
        Tcritical = round(CP.PropsSI('Tcrit', 'T',T, 'P',P, fluid),1)
    except:
        Tcritical = math.nan
        doc['errors'].append("Failed to calculate 'Tcritical' . Check Inputs")
    finally:
        doc['result'].update({'Tcritical':{'_val' : str(Tcritical), '_dim':'temperature'}})

    try:
        Ptriple = round(CP.PropsSI('P_TRIPLE', 'T',T, 'P',P, fluid),1)
    except:
        Ptriple = math.nan
        doc['errors'].append("Failed to calculate 'Ptriple' . Check Inputs")
    finally:
        doc['result'].update({'Ptriple':{'_val' : str(Ptriple), '_dim':'pressure'}})


    try:
        Ttriple = round(CP.PropsSI('T_TRIPLE', 'T',T, 'P',P, fluid),1)
    except:
        Ttriple = math.nan
        doc['errors'].append("Failed to calculate 'Ttriple' . Check Inputs")
    finally:
        doc['result'].update({'Ttriple':{'_val' : str(Ttriple), '_dim':'temperature'}})


    try:
        acentric = round(CP.PropsSI('acentric', 'T',T, 'P',P, fluid),4)
    except:
        acentric = math.nan
        doc['errors'].append("Failed to calculate 'acentric' . Check Inputs")
    finally:
        doc['result'].update({'acentric':{'_val' : str(acentric)}})

    try:
        Z = round(CP.PropsSI('Z', 'T',T, 'P',P, fluid),4)
    except:
        Z = math.nan
        doc['errors'].append("Failed to calculate 'Z' . Check Inputs")
    finally:
        doc['result'].update({'Z':{'_val' : str(Z)}})

    try:
        rho = round(CP.PropsSI('D', 'T',T, 'P',P, fluid),4)
        v = round(1/rho,4)
    except:
        rho = math.nan
        v = math.nan
        doc['errors'].append("Failed to calculate 'Density' and 'Specific Volume' . Check Inputs")

    finally:
        doc['result'].update({'rho':{'_val' : str(rho), '_dim':'density'}})
        doc['result'].update({'v':{'_val' : str(v), '_dim':'specificVolume'}})


    try:
        h =  round(CP.PropsSI('H', 'T',T, 'P',P, fluid),1)
    except:
        h = math.nan
        doc['errors'].append("Failed to calculate 'Enthalphy' . Check Inputs")

    finally:
        doc['result'].update({'h':{'_val' : str(h), '_dim':'specificEnergy'}})



    try:
        u = round(CP.PropsSI('U', 'T',T, 'P',P, fluid),1)
    except:
        u = math.nan
        doc['errors'].append("Failed to calculate 'Specific Internal Energy' . Check Inputs")
    finally:
        doc['result'].update({'u':{'_val' : str(u), '_dim':'specificEnergy'}})

    try:
        s = round(CP.PropsSI('S', 'T',T, 'P',P, fluid),1)
    except:
        s = math.nan
        doc['errors'].append("Failed to calculate 'Specific Entropy' . Check Inputs")
    finally:
        doc['result'].update({'s':{'_val' : str(s), '_dim':'specificHeat'}})


    try:
        gibbs = round(CP.PropsSI('G', 'T',T, 'P',P, fluid),1)
    except:
        gibbs = math.nan
        doc['errors'].append("Failed to calculate 'Gibbs Free Energy' . Check Inputs")

    finally:
        doc['result'].update({'gibbs':{'_val' : str(gibbs), '_dim':'specificEnergy'}})

    try:
        helmholtz = round(CP.PropsSI('Helmholtzmass', 'T',T, 'P',P, fluid),1)
    except:
        helmholtz = math.nan
        doc['errors'].append("Failed to calculate 'Helmholtz Energy' . Check Inputs")

    finally:
        doc['result'].update({'helmholtz':{'_val' : str(helmholtz), '_dim':'specificEnergy'}})


    try:
        Cp = round(CP.PropsSI('Cpmass', 'T',T, 'P',P, fluid),1)
    except:
        Cp = math.nan
        doc['errors'].append("Failed to calculate 'Cp' . Check Inputs")

    finally:
        doc['result'].update({'Cp':{'_val' : str(Cp), '_dim':'specificHeat'}})


    try:
        Cv = round(CP.PropsSI('Cvmass', 'T',T, 'P',P, fluid),1)
    except:
        Cv = math.nan
        doc['errors'].append("Failed to calculate 'Cv' . Check Inputs")

    finally:
        doc['result'].update({'Cv':{'_val' : str(Cv), '_dim':'specificHeat'}})

    try:
        Cp_molar = round(CP.PropsSI('Cpmolar', 'T',T, 'P',P, fluid),1)
    except:
        Cp_molar = math.nan
        doc['errors'].append("Failed to calculate 'Cp_molar' . Check Inputs")

    finally:
        doc['result'].update({'Cp_molar':{'_val' : str(Cp_molar), '_dim':'specificHeatMolar'}})


    try:
        Cv_molar = round(CP.PropsSI('Cvmolar', 'T',T, 'P',P, fluid),1)
    except:
        Cv_molar = math.nan
        doc['errors'].append("Failed to calculate 'Cv_molar' . Check Inputs")

    finally:
        doc['result'].update({'Cv_molar':{'_val' : str(Cv_molar), '_dim':'specificHeatMolar'}})


    try:
        Cp0 = round(CP.PropsSI('Cp0mass', 'T',T, 'P',P, fluid),1)
    except:
        Cp0 = math.nan
        doc['errors'].append("Failed to calculate 'Cp0' . Check Inputs")
    finally:
        doc['result'].update({'Cp0':{'_val' : str(Cp0), '_dim':'specificHeat'}})


    try:
        Prandtl = round(CP.PropsSI('Prandtl', 'T',T, 'P',P, fluid),4)
    except:
        Prandtl = math.nan
        doc['errors'].append("Failed to calculate 'Prandtl' . Check Inputs")

    finally:
        doc['result'].update({'Prandtl':{'_val' : str(Prandtl)}})


    try:
        dynViscosity = round(CP.PropsSI('viscosity', 'T',T, 'P',P, fluid),8)
    except:
        dynViscosity = math.nan
        doc['errors'].append("Failed to calculate 'Dynamic Viscosity' . Check Inputs")

    finally:
        doc['result'].update({'dynViscosity':{'_val' : str(dynViscosity), '_dim':'dynViscosity'}})


    try:
        conductivity  = round(CP.PropsSI('conductivity', 'T',T, 'P',P, fluid),8)
    except:
        conductivity = math.nan
        doc['errors'].append("Failed to calculate 'Thermal Conductivity' . Check Inputs")

    finally:
        doc['result'].update({'conductivity':{'_val' : str(conductivity), '_dim':'thermalConductivity'}})

    try:
        HH = CP.PropsSI('HH', 'T',T, 'P',P, fluid)
    except:
        HH=""
    finally:
        doc['result'].update({'HH':{'_val' : str(HH)}})


    try:
        PH = CP.PropsSI('PH', 'T',T, 'P',P, fluid)
    except:
        PH = ""
    finally:
        doc['result'].update({'PH':{'_val' : str(PH)}})


    try:
        GWP = CP.PropsSI('GWP100', 'T',T, 'P',P, fluid)
    except:
        GWP = ""
    finally:
        doc['result'].update({'GWP':{'_val' : str(GWP)}})

    try:
        ODP = CP.PropsSI('ODP', 'T',T, 'P',P, fluid)
    except:
        ODP = ""
    finally:
        doc['result'].update({'ODP':{'_val' : str(ODP)}})


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])

    doc_original['errors'] = doc['errors']

    return True
