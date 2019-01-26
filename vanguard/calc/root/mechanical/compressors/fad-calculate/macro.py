import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from techlib.mechanical.compressor.comp_api617 import Hpolytropic, absPower, Tdischarge, Qactual, polyeff, nexp, centframe, theta, HpmaxWheel
from techlib.thermochem.thermochem_utils import mixture_props
from math import *
from techlib.mechanical.compressor.air import moistAirDensity, humidityRatio

from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

#    Get essential data
    Pambient = float(doc['input']['Pambient']['_val'])
    Tambient = float(doc['input']['Tambient']['_val'])
    RHambient = float(doc['input']['RHambient']['_val'])
    Flow = float(doc['input']['Flow']['_val'])

    X = humidityRatio(Pambient, Tambient, RHambient)
    FAD = Flow*(1+X)*(298.0/273.15)

    Pnormal = 101325
    Tnormal = 273.15
    rho_normal = moistAirDensity(Pnormal, Tnormal, RH=0)
    mass_dryair = Flow*rho_normal
    mass_moistair = mass_dryair*(1+X)
    rho_moistair = moistAirDensity(Pambient, Tambient, RHambient)
    FAD = mass_moistair/rho_moistair
    rho = roundit(rho_moistair)
    doc['result'].update({'FAD':{'_val' : str(FAD), '_dim':'flow'}})
    doc['result'].update({'rho':{'_val' : str(rho_moistair), '_dim':'density'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
