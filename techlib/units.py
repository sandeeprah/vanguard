from collections import OrderedDict
import json
import os
import math
from marshmallow import Schema, fields, pprint, pre_load, validate, validates, ValidationError
from collections import OrderedDict
from techlib.mathutils import parseFloat, roundit

unitLib = OrderedDict({
    "length": {
        "dimtitle": "Length",
        "units": {
            "um": {
                "label": "μm",
                "cf": 1e-6,
                "off": 0
            },
            "mm": {
                "label": "mm",
                "cf": 1e-3,
                "off": 0
            },
            "m": {
                "label": "m",
                "cf": 1,
                "off": 0
            },
            "ft": {
                "label": "ft",
                "cf": 0.3048,
                "off": 0
            },
            "yd": {
                "label": "yd",
                "cf": 0.9144,
                "off": 0
            }
        }
    },

    "length_micro": {
        "dimtitle": "Length Micro",
        "units": {
            "um": {
                "label": "μm",
                "cf": 1e-6,
                "off": 0
            },
            "mm": {
                "label": "mm",
                "cf": 1e-3,
                "off": 0
            },
            "m": {
                "label": "m",
                "cf": 1,
                "off": 0
            },
            "ft": {
                "label": "ft",
                "cf": 0.3048,
                "off": 0
            },
            "yd": {
                "label": "yd",
                "cf": 0.9144,
                "off": 0
            }
        }
    },

    "length_mili": {
        "dimtitle": "Length Mili",
        "units": {
            "um": {
                "label": "μm",
                "cf": 1e-6,
                "off": 0
            },
            "mm": {
                "label": "mm",
                "cf": 1e-3,
                "off": 0
            },
            "m": {
                "label": "m",
                "cf": 1,
                "off": 0
            },
            "ft": {
                "label": "ft",
                "cf": 0.3048,
                "off": 0
            },
            "yd": {
                "label": "yd",
                "cf": 0.9144,
                "off": 0
            }
        }
    },

    "length_kilo": {
        "dimtitle": "Length Kilo",
        "units": {
            "um": {
                "label": "μm",
                "cf": 1e-6,
                "off": 0
            },
            "mm": {
                "label": "mm",
                "cf": 1e-3,
                "off": 0
            },
            "m": {
                "label": "m",
                "cf": 1,
                "off": 0
            },
            "ft": {
                "label": "ft",
                "cf": 0.3048,
                "off": 0
            },
            "yd": {
                "label": "yd",
                "cf": 0.9144,
                "off": 0
            }
        }
    },

    "area": {
        "dimtitle": "Area",
        "units": {
            "m2": {
                "label": "m²",
                "cf": 1,
                "off": 0
            },
            "mm2": {
                "label": "mm²",
                "cf": 1e-6,
                "off": 0
            },
            "ft2": {
                "label": "ft²",
                "cf": 0.092903,
                "off": 0
            },
            "in2": {
                "label": "in²",
                "cf": 6.4516e-4,
                "off": 0
            }
        }
    },

    "volume": {
        "dimtitle": "Volume",
        "units": {
            "m3": {
                "label": "m³",
                "cf": 1,
                "off": 0
            },
            "ft3": {
                "label": "ft³",
                "cf": 0.0283168,
                "off": 0
            }
        }
    },

    "angle": {
        "dimtitle": "Angle",
        "units": {
            "degrees": {
                "label": "degrees",
                "cf": 1.74533e-2,
                "off": 0
            },
            "radians": {
                "label": "radians",
                "cf": 1,
                "off": 0
            }
        }
    },

    "mass": {
        "dimtitle": "Mass",
        "units": {
            "ug": {
                "label": "μg",
                "cf": 1e-9,
                "off": 0
            },
            "mg": {
                "label": "mg",
                "cf": 1e-6,
                "off": 0
            },
            "g": {
                "label": "g",
                "cf": 1e-3,
                "off": 0
            },
            "kg": {
                "label": "kg",
                "cf": 1,
                "off": 0
            },
            "ton": {
                "label": "ton",
                "cf": 1e3,
                "off": 0
            },
            "lb": {
                "label": "lb",
                "cf": 0.453592,
                "off": 0
            }
        }
    },
    "time": {
        "dimtitle": "Time",
        "units": {
            "us": {
                "label": "μs",
                "cf": 1e-6,
                "off": 0
            },
            "ms": {
                "label": "ms",
                "cf": 1e-3,
                "off": 0
            },
            "s": {
                "label": "μs",
                "cf": 1,
                "off": 0
            },
            "min": {
                "label": "min",
                "cf": 60,
                "off": 0
            },
            "hr": {
                "label": "hr",
                "cf": 3600,
                "off": 0
            },
            "day": {
                "label": "day",
                "cf": 86400,
                "off": 0
            }
        }
    },
    "speed": {
        "dimtitle": "Speed",
        "units": {
            "m/s": {
                "label": "m/s",
                "cf": 1,
                "off": 0
            },
            "km/hr": {
                "label": "km/hr",
                "cf": 0.277778,
                "off": 0
            },
            "ft/s": {
                "label": "ft/s",
                "cf": 0.3048,
                "off": 0
            }
        }
    },
    "acceleration": {
        "dimtitle": "Acceleration",
        "units": {
            "m/s2": {
                "label": "m/s²",
                "cf": 1,
                "off": 0
            },
            "ft/s2": {
                "label": "ft/s²",
                "cf": 0.3048,
                "off": 0
            }
        }
    },

    "force": {
        "dimtitle": "Force",
        "units": {
            "N": {
                "label": "N",
                "cf": 1,
                "off": 0
            },
            "kN": {
                "label": "kN",
                "cf": 1e3,
                "off": 0
            },
            "lbf": {
                "label": "lbf",
                "cf": 4.44822,
                "off": 0
            }
        }
    },

    "energy": {
        "dimtitle": "Energy",
        "units": {
            "J": {
                "label": "J",
                "cf": 1,
                "off": 0
            },
            "kJ": {
                "label": "kJ",
                "cf": 1e3,
                "off": 0
            },
            "Btu": {
                "label": "Btu",
                "cf": 1055.06,
                "off": 0
            }
        }
    },

    "power": {
        "dimtitle": "Power",
        "units": {
            "W": {
                "label": "W",
                "cf": 1,
                "off": 0
            },
            "kW": {
                "label": "kW",
                "cf": 1e3,
                "off": 0
            },
            "hp": {
                "label": "hp",
                "cf": 746,
                "off": 0
            }
        }
    },

    "pressure": {
        "dimtitle": "Pressure",
        "units": {
            "Pa": {
                "label": "Pa",
                "cf": 1,
                "off": 0
            },
            "kPa": {
                "label": "kPa",
                "cf": 1e3,
                "off": 0
            },
            "MPa": {
                "label": "MPa",
                "cf": 1e6,
                "off": 0
            },
            "bar": {
                "label": "bar",
                "cf": 1e5,
                "off": 0
            },
            "atm": {
                "label": "atm",
                "cf": 101325,
                "off": 0
            },
            "kg/cm2": {
                "label": "kg/cm²",
                "cf": 98066.5,
                "off": 0
            }
        }
    },

    "temperature": {
        "dimtitle": "Temperature",
        "units": {
            "K": {
                "label": "K",
                "cf": 1,
                "off": 0
            },
            "C": {
                "label": "°C",
                "cf": 1,
                "off": 273.15
            },
            "F": {
                "label": "°F",
                "cf": 5 / 9,
                "off": -32 * 5 / 9 + 273.15,
            },
            "R": {
                "label": "°R",
                "cf": 5 / 9,
                "off": 0
            }
        }
    },

    "flow": {
        "dimtitle": "Flow",
        "units": {
            "m3/s": {
                "label": "m³/s",
                "cf": 1,
                "off": 0
            },
            "m3/min": {
                "label": "m³/min",
                "cf": 1 / 60,
                "off": 0
            },
            "m3/hr": {
                "label": "m³/hr",
                "cf": 1 / 3600,
                "off": 0
            },
            "lpm": {
                "label": "lpm",
                "cf": 1.666667e-5,
                "off": 0
            },
            "lph": {
                "label": "lph",
                "cf": 1e-3/3.6e3,
                "off": 0
            },
            "usgpm": {
                "label": "usgpm",
                "cf": 6.309e-5,
                "off": 0
            },
            "bbl/day": {
                "label": "bbl/day",
                "cf": 1.840e-6,
                "off": 0
            },
        }
    },

    "massflow": {
        "dimtitle": "Mass Flow",
        "units": {
            "kg/s": {
                "label": "kg/s",
                "cf": 1,
                "off": 0
            },
            "kg/min": {
                "label": "kg/min",
                "cf": 1 / 60,
                "off": 0
            },
            "kg/hr": {
                "label": "kg/hr",
                "cf": 1 / 3600,
                "off": 0
            },
            "lb/hr": {
                "label": "lb/hr",
                "cf": 1.25998e-4,
                "off": 0
            },
        }
    },


    "density": {
        "dimtitle": "Density",
        "units": {
            "kg/m3": {
                "label": "kg/m³",
                "cf": 1,
                "off": 0
            },
            "g/cm3": {
                "label": "g/cm³",
                "cf": 1e3,
                "off": 0
            },
            "lb/ft3": {
                "label": "lb/ft³",
                "cf": 16.018,
                "off": 0
            }
        }
    },
    "molecularMass":{
        "dimtitle":"Molecular Mass",
        "units":{
            "kg/mol" : {
                "label" : "kg/mol",
                "cf" : 1,
                "off" : 0
            },
            "g/mol" : {
                "label" : "g/mol",
                "cf" : 0.001,
                "off" : 0
            },
            "kg/kmol" : {
                "label" : "g/mol",
                "cf" : 0.001,
                "off" : 0
            }
        }
    },

    "specificVolume":{
        "dimtitle":"Specific Volume",
        "units":{
            "m3/kg" : {
                "label" : "m³/kg",
                "cf" : 1,
                "off" : 0
            }
        }
    },
    "specificEnergy":{
        "dimtitle":"Specific Energy",
        "units":{
            "J/kg" : {
                "label" : "J/kg",
                "cf" : 1,
                "off" : 0
            },
            "kJ/kg" : {
                "label" : "kJ/kg",
                "cf" : 1000,
                "off" : 0
            }
        }
    },
    "specificEnergyMolar":{
        "dimtitle":"Specific Energy Molar",
        "units":{
            "J/mol" : {
                "label" : "J/mol",
                "cf" : 1,
                "off" : 0
            },
            "kJ/kmol" : {
                "label" : "J/mol",
                "cf" : 1,
                "off" : 0
            }
        }
    },
    "specificHeat":{
        "dimtitle":"Specific Heat",
        "units":{
            "J/kg.K" : {
                "label" : "J/kg.K",
                "cf" : 1,
                "off" : 0
            },
            "kJ/kg.K" : {
                "label" : "kJ/kg.K",
                "cf" : 1000,
                "off" : 0
            }
        }
    },

    "specificHeatMolar":{
        "dimtitle":"Molar Specific Heat",
        "units":{
            "J/mol.K" : {
                "label" : "J/mol.K",
                "cf" : 1,
                "off" : 0
            },
            "kJ/kmol.K" : {
                "label" : "J/mol.K",
                "cf" : 1,
                "off" : 0
            }
        }
    },


    "thermalConductivity":{
        "dimtitle":"Thermal Conductivity",
        "units":{
            "W/m.K" : {
                "label" : "W/m.K",
                "cf" : 1,
                "off" : 0
            }
        }
    },

    "dynViscosity": {
        "dimtitle": "Dynamic Viscosity",
        "units": {
            "Pa.s": {
                "label": "Pa.s",
                "cf": 1,
                "off": 0
            },
            "mPa.s": {
                "label": "mPa.s",
                "cf": 1e-3,
                "off": 0
            },
            "cP": {
                "label": "cP",
                "cf": 1e-3,
                "off": 0
            }
        }
    },

    "kinViscosity": {
        "dimtitle": "Kinematic Viscosity",
        "units": {
            "m2/s": {
                "label": "m²/s",
                "cf": 1,
                "off": 0
            },
            "St": {
                "label": "St",
                "cf": 1e-4,
                "off": 0
            },
            "cSt": {
                "label": "cSt",
                "cf": 1e-6,
                "off": 0
            }
        }
    },

    "specificFuelConsumption" : {
        "dimtitle": "Specific Fuel Consumption",
        "units": {
            "m3/W.s": {
                "label": "m³/W.s",
                "cf": 1,
                "off": 0
            },
            "litre/kW.h": {
                "label": "litre/kW.h",
                "cf": 1e-6/3600,
                "off": 0
            }
        }
    },
    "intensity" : {
        "dimtitle": "Energy Intensity",
        "units": {
            "W/m2": {
                "label": "W/m²",
                "cf": 1,
                "off": 0
            },
            "kW/m2": {
                "label": "kW/m²",
                "cf": 1000,
                "off": 0
            }
        }
    }
})

SI_UNITS = {
    "length": "m",
    "length_micro": "m",
    "length_mili": "m",
    "length_kilo": "m",
    "area": "m2",
    "volume": "m3",
    "angle": "radians",
    "mass": "kg",
    "time": "s",
    "speed": "m/s",
    "acceleration": "m/s2",
    "force": "N",
    "energy": "J",
    "power": "W",
    "pressure": "Pa",
    "temperature": "K",
    "massflow": "kg/s",
    "flow": "m3/s",
    "density": "kg/m3",
    "molecularMass": "kg/mol",
    "specificVolume": "m3/kg",
    "specificEnergy": "J/kg",
    "specificEnergyMolar": "J/mol",
    "specificHeat": "J/kg.K",
    "specificHeatMolar": "J/mol.K",
    "thermalConductivity": "W/m.K",
    "dynViscosity": "Pa.s",
    "kinViscosity": "m2/s",
    "specificFuelConsumption" : "m3/W.s",
    "intensity" : "W/m2"

}

def getDimensions():
    dim_list = []
    for key in unitLib:
        dim_list.append(key)
    return dim_list

def getDimensionTitle(dimension):
    return unitLib[dimension]['dimtitle']

def getUnits(dimension):
    units_list = []
    if dimension in unitLib:
        units = unitLib[dimension]['units']
        for key in units:
            units_list.append(key)

    return units_list

def getUnitLabel(dimension, unit):
    return unitLib[dimension]["units"][unit]['label']


def getUnitConvFact(dimension,unit):
    ucf = unitLib[dimension]["units"][unit]["cf"]
    return ucf

def getUnitOffset(dimension, unit):
    off = unitLib[dimension]["units"][unit]["off"]
    return off

def getSI_unit(dimension):
    return SI_UNITS[dimension]

def unitConvert(value, dimension, fromUnit, toUnit, autoRoundOff=False):
    if (math.isnan(parseFloat(value))):
        return_value = value
    else:
        if ((fromUnit=='none') or (toUnit=='none')):
            return_value = value
        else:
            if (fromUnit==toUnit):
                return_value = value
            else:
                parsed_value = parseFloat(value)
                cf_from_unit = getUnitConvFact(dimension, fromUnit)
                offset_from_unit = getUnitOffset(dimension, fromUnit)
                cf_to_unit = getUnitConvFact(dimension, toUnit);
                offset_to_unit = getUnitOffset(dimension, toUnit);
                base_value = parsed_value * cf_from_unit + offset_from_unit;
                return_value = (base_value - offset_to_unit) / cf_to_unit;
                if (autoRoundOff):
                    return_value = roundit(return_value,7,0.001)

    if (isinstance(value, str)):
        return str(return_value)
    else:
        return return_value


def treeUnitConvert(tree, fromUnits, toUnits, autoRoundOff=False):
    if (isinstance(tree, dict)):
        if ('_val' in tree) and ('_dim' in tree):
            value = tree['_val']
            dimension = tree['_dim']
            fromUnit = fromUnits[dimension]
            toUnit = toUnits[dimension]
            con_value = unitConvert(value, dimension, fromUnit, toUnit, autoRoundOff)
            tree['_val'] = con_value
        if ('_val' in tree) and ('_dim' not in tree):
            pass
        if ('_coldim' in tree) and ('_list' in tree):
            for row in tree['_list']:
                for column in row:
                    if column in tree['_coldim']:
                        dimension = tree['_coldim'][column]
                        value = row[column]
                        fromUnit = fromUnits[dimension]
                        toUnit = toUnits[dimension]
                        con_value = unitConvert(value, dimension, fromUnit, toUnit, autoRoundOff)
                        row[column] = con_value
        else:
            for k,v in tree.items():
                treeUnitConvert(v, fromUnits, toUnits, autoRoundOff)

    elif (isinstance(tree, list)):
        for item in tree:
            treeUnitConvert(item, fromUnits, toUnits, autoRoundOff)



def printUnitLib():
    print(json.dumps(unitLib, indent=4))
