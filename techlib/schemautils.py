import numbers
from marshmallow import Schema, fields, pprint, pre_load, ValidationError, validate
from marshmallow.validate import Validator
from collections import OrderedDict
from techlib import units


def xisBlank(value):
    val = value['_val']
    if (val==""):
        return True
    else:
        return False

def xisMissing(data, key):
    if (key not in data):
        return True
    elif ('_val' not in data[key]):
        return True
    else:
        if (data[key]['_val']==''):
            return True
        else:
            return False

        return False


class validator:

    def xRequired(data, key, fName=None):
        if (key not in data):
            raise ValidationError('field is required', fName)

    def xNotEmpty(value, fName=None):
        val = value['_val']
        if (isinstance(val, str)):
            val = val.strip()
        if (val==""):
            raise ValidationError("field can't be empty", fName)


    def xChoice(value, choices, fName=None):
        if value['_val'] in choices:
            return True
        else:
            raise ValidationError("invalid choice", fName)

    def xNumber(value, fName=None):
        try:
            val = float(value['_val'])
            return True
        except Exception:
            raise ValidationError('invalid number', fName)


    def xInteger(value, fName=None):
        try:
            val = int(value['_val'])
            return True
        except Exception:
            raise ValidationError('invalid integer', fName)


    def xGrtThan(value, setVal, fName=None):
        val = float(value['_val'])
        if (val > setVal):
            return True
        else:
            raise ValidationError('> {} reqd'.format(setVal), fName)

    def xGrtThanEq(value, setVal, fName=None):
        val = float(value['_val'])
        if (val >= setVal):
            return True
        else:
            raise ValidationError('>= {} reqd'.format(setVal), fName)

    def xLessThan(value, setVal, fName=None):
        val = float(value['_val'])
        if (val < setVal):
            return True
        else:
            raise ValidationError('< {} reqd'.format(setVal), fName)

    def xLessThanEq(value, setVal, fName=None):
        val = float(value['_val'])
        if (val <= setVal):
            return True
        else:
            raise ValidationError('<= {} reqd'.format(setVal), fName)


    def fNumber(value, fName=None):
        try:
            val = float(value)
            return True
        except Exception:
            raise ValidationError('invalid number', fName)

    def fInteger(value, fName=None):
        try:
            val = int(value)
            return True
        except Exception:
            raise ValidationError('invalid integer', fName)


    def fGrtThan(value, setVal, fName=None):
        val = float(value)
        if (val > setVal):
            return True
        else:
            raise ValidationError('> {} reqd'.format(setVal), fName)

    def fGrtThanEq(value, setVal, fName=None):
        val = float(value)
        if (val >= setVal):
            return True
        else:
            raise ValidationError('>= {} reqd'.format(setVal), fName)

    def fLessThan(value, setVal, fName=None):
        val = float(value)
        if (val < setVal):
            return True
        else:
            raise ValidationError('< {} reqd'.format(setVal), fName)

    def fLessThanEq(value, setVal, fName=None):
        val = float(value)
        if (val <= setVal):
            return True
        else:
            raise ValidationError('<= {} reqd'.format(setVal), fName)

    def xString(value, fName=None):
        val = value['_val']
        if (isinstance(value['_val'], str)):
            return True
        else:
            raise ValidationError("Invalid String", fName)


    def xDim(value, dimensions, fName=None):
        if ('_dim' in value):
            dim = value['_dim']
            if (dim in dimensions):
                return True
            else:
                raise ValidationError("invalid dimension", fName)
        else:
            raise ValidationError("missing '_dim' Key", fName)


    def xPrm(value, permissions, fName=None):
        prm = value['_prm']
        if (prm in permissions):
            return True
        else:
            raise ValidationError("invalid permissions", fName)


class sXfld(Schema):
    _val = fields.Raw(required=True)
    _dim = fields.String()
    _lbl = fields.String()
    _prm = fields.String()
    class Meta:
        ordered = True

class sUnits(Schema):
    length_units = units.getUnits('length')
    length = fields.String(validate=validate.OneOf(length_units))
    length_micro_units = units.getUnits('length_micro')
    length_micro = fields.String(validate=validate.OneOf(length_units))
    length_mili_units = units.getUnits('length_mili')
    length_mili = fields.String(validate=validate.OneOf(length_units))
    length_kilo_units = units.getUnits('length_kilo')
    length_kilo = fields.String(validate=validate.OneOf(length_units))
    area_units = units.getUnits('area')
    area = fields.String(validate=validate.OneOf(area_units))
    volume_units = units.getUnits('volume')
    volume = fields.String(validate=validate.OneOf(volume_units))
    angle_units = units.getUnits('angle')
    angle = fields.String(validate=validate.OneOf(angle_units))
    mass_units = units.getUnits('mass')
    mass = fields.String(validate=validate.OneOf(mass_units))
    time_units = units.getUnits('time')
    time = fields.String(validate=validate.OneOf(time_units))
    speed_units = units.getUnits('speed')
    speed = fields.String(validate=validate.OneOf(speed_units))
    acceleration_units = units.getUnits('acceleration')
    acceleration = fields.String(validate=validate.OneOf(acceleration_units))
    force_units = units.getUnits('force')
    force = fields.String(validate=validate.OneOf(force_units))
    energy_units = units.getUnits('energy')
    energy = fields.String(validate=validate.OneOf(energy_units))
    power_units = units.getUnits('power')
    power = fields.String(validate=validate.OneOf(power_units))
    pressure_units = units.getUnits('pressure')
    pressure = fields.String(validate=validate.OneOf(pressure_units))
    temperature_units = units.getUnits('temperature')
    temperature = fields.String(validate=validate.OneOf(temperature_units))
    massflow_units = units.getUnits('massflow')
    massflow = fields.String(validate=validate.OneOf(massflow_units))
    flow_units = units.getUnits('flow')
    flow = fields.String(validate=validate.OneOf(flow_units))
    density_units = units.getUnits('density')
    density = fields.String(validate=validate.OneOf(density_units))
    molecularMass_units = units.getUnits('molecularMass')
    molecularMass = fields.String(validate=validate.OneOf(molecularMass_units))
    specificVolume_units = units.getUnits('specificVolume')
    specificVolume = fields.String(validate=validate.OneOf(specificVolume_units))
    specificEnergy_units = units.getUnits('specificEnergy')
    specificEnergy = fields.String(validate=validate.OneOf(specificEnergy_units))
    specificEnergyMolar_units = units.getUnits('specificEnergyMolar')
    specificEnergyMolar = fields.String(validate=validate.OneOf(specificEnergyMolar_units))
    specificHeat_units = units.getUnits('specificHeat')
    specificHeat = fields.String(validate=validate.OneOf(specificHeat_units))
    specificHeatMolar_units = units.getUnits('specificHeatMolar')
    specificHeatMolar = fields.String(validate=validate.OneOf(specificHeatMolar_units))
    thermalConductivity_units = units.getUnits('thermalConductivity')
    thermalConductivity = fields.String(validate=validate.OneOf(thermalConductivity_units))
    dynViscosity_units = units.getUnits('dynViscosity')
    dynViscosity = fields.String(validate=validate.OneOf(dynViscosity_units))
    kinViscosity_units = units.getUnits('kinViscosity')
    kinViscosity = fields.String(validate=validate.OneOf(kinViscosity_units))
    specificFuelConsumption_units = units.getUnits('specificFuelConsumption')
    specificFuelConsumption = fields.String(validate=validate.OneOf(specificFuelConsumption_units))
    intensity_units = units.getUnits('intensity')
    intensity = fields.String(validate=validate.OneOf(intensity_units))

    class Meta:
        ordered = True



class sMeta(Schema):
    project_no = fields.String(required=True)
    project_title = fields.String(required=True)
    docClass_code = fields.String(required=True)
    docClass_title = fields.String(required=True)
    docInstance_title = fields.String(required=True)
    doc_no = fields.String()
    rev = fields.String()
    date = fields.String()

    class Meta:
        ordered=True

'''
class sDoc(Schema):
    _id = fields.String(required=True)
    class Meta:
        ordered = True
'''
class sDocPrj(Schema):
#    _id = fields.String(required=True)
    sub_url = fields.String(required=True)
    meta = fields.Nested(sMeta, required=True)
    units = fields.Nested(sUnits)
    input = fields.Dict(required = True)
    result = fields.Dict()
    errors = fields.List(fields.String)

    class Meta:
        ordered = True
