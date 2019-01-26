from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd


class schema_fluidfraction(Schema):
    fluid_list = ["Carbon",
                "Hydrogen",
                "Oxygen",
                "Nitrogen",
                "CarbonMonoxide",
                "CarbonDioxide",
                "Methane",
                "Ethane",
                "Ethylene",
                "Acetylene",
                "Propane",
                "Propylene",
                "Butane",
                "Butylene",
                "Pentane",
                "Hexane",
                "Benzene",
                "Methanol",
                "Ammonia",
                "Sulphur",
                "HydrogenSulphide",
                "Water"]
    fluid = fields.String(required=True, validate=validate.OneOf(choices=fluid_list))
    percent = fields.Float(required=True)
    class Meta:
        ordered = True

    @validates('percent')
    def check_percent(self, value):
        vd.fGrtThanEq(value,0)
        vd.fLessThanEq(value,100)



class docInput(Schema):
    fuel_as = fields.Nested(sXfld)
    flue_as = fields.Nested(sXfld)
    gasfuel = fields.Nested(schema_fluidfraction, many=True, required=True)
    emission_units = fields.Nested(sXfld)
    Tair = fields.Nested(sXfld)
    Pair = fields.Nested(sXfld)
    RH = fields.Nested(sXfld)
    excess_air = fields.Nested(sXfld)
    Ts = fields.Nested(sXfld)
    Ps = fields.Nested(sXfld)
    O2_reference = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_fuel_as(self, data):
        fName = 'fuel_as'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        fuel_as_options = ["mole_percent","mass_percent"]
        vd.xChoice(value, fuel_as_options, fName)

    @validates_schema()
    def check_flue_as(self, data):
        fName = 'flue_as'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        fuel_as_options = ["mole_per_fuelmole","mass_per_fuelmass"]
        vd.xChoice(value, fuel_as_options, fName)

    @validates_schema()
    def check_Tair(self, data):
        fName = 'Tair'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_Pair(self, data):
        fName = 'Pair'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['pressure'], fName)
        vd.xGrtThanEq(value, 0, fName)


    @validates_schema()
    def check_RH(self, data):
        fName = 'RH'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThanEq(value, 100, fName)

    @validates_schema()
    def check_excess_air(self, data):
        fName = 'excess_air'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_emission_units(self, data):
        fName = 'emission_units'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        unit_options = ["ppmv","mg/Nm3","mg/Sm3"]
        vd.xChoice(value, unit_options, fName)

    @validates_schema()
    def check_Ts(self, data):
        fName = 'Ts'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_Ps(self, data):
        fName = 'Ps'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['pressure'], fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_O2_reference(self, data):
        fName = 'O2_reference'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)


    @validates_schema()
    def check_gasfuel(self, data):
        if ('gasfuel' in data):
            gasfuel = data['gasfuel']
            sigma_y = 0
            for component in gasfuel:
                if ('percent' in component):
                    sigma_y = sigma_y + component['percent']

            if (sigma_y <=0):
                raise ValidationError('No gas composition entered. Total > 0 reqd','schema_gasfuel')



class docResult(Schema):
    concentration = fields.Nested(sXfld)
    units = fields.Nested(sXfld)
    O2_reference = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
