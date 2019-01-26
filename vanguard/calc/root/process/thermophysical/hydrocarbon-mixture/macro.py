import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from techlib.thermochem.thermochem_utils import mixture_props
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    mixture = doc['input']['mixture']
    P = float(doc['input']['P']['_val'])
    T = float(doc['input']['T']['_val'])

    mixprops = mixture_props(mixture,P=P,T=T)

    MW = mixprops['MW']
    Pcritical = mixprops['Pcritical']
    Tcritical = mixprops['Tcritical']
    Pr = mixprops['Pr']
    Tr = mixprops['Tr']
    acentric = mixprops['acentric']
    Z_PR = mixprops['Z_PR']
    Z_LKP = mixprops['Z_LKP']
    Z_NO = mixprops['Z_NO']
    Cp0mass = mixprops['Cp0mass']
    Cv0mass = mixprops['Cv0mass']
    Cp0molar = mixprops['Cp0molar']
    Cv0molar = mixprops['Cv0molar']

    doc['result'].update({'MW':{'_val' : str(MW), '_dim':'molecularMass'}})
    doc['result'].update({'Pcritical':{'_val' : str(Pcritical), '_dim':'pressure'}})
    doc['result'].update({'Tcritical':{'_val' : str(Tcritical), '_dim':'temperature'}})
    doc['result'].update({'Pr':{'_val' : str(Pr)}})
    doc['result'].update({'Tr':{'_val' : str(Tr)}})
    doc['result'].update({'acentric':{'_val' : str(acentric)}})
    doc['result'].update({'Z_PR':{'_val' : str(Z_PR)}})
    doc['result'].update({'Z_LKP':{'_val' : str(Z_LKP)}})
    doc['result'].update({'Z_NO':{'_val' : str(Z_NO)}})
    doc['result'].update({'Cp0mass':{'_val' : str(Cp0mass), '_dim':'specificHeat'}})
    doc['result'].update({'Cv0mass':{'_val' : str(Cv0mass), '_dim':'specificHeat'}})
    doc['result'].update({'Cp0molar':{'_val' : str(Cp0molar), '_dim':'specificHeatMolar'}})
    doc['result'].update({'Cv0molar':{'_val' : str(Cv0molar), '_dim':'specificHeatMolar'}})


    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    return True
