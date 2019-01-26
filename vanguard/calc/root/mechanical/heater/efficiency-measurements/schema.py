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
    Ta = fields.Nested(sXfld)
    RH = fields.Nested(sXfld)
    flue_O2 = fields.Nested(sXfld)
    sampling_basis = fields.Nested(sXfld)
    loss_radiation = fields.Nested(sXfld)
    Texit = fields.Nested(sXfld)
    composition_type = fields.Nested(sXfld)
    gasfuel = fields.Nested(schema_fluidfraction, many=True, required=True)
    Tf = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_Ta(self, data):
        fName = 'Ta'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_RH(self, data):
        fName = 'RH'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThanEq(value, 100, fName)

    @validates_schema()
    def check_flue_O2(self, data):
        fName = 'flue_O2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_sampling_basis(self, data):
        fName = 'sampling_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        sampling_basis_options = ["wet","dry"]
        vd.xChoice(value, sampling_basis_options, fName)

    @validates_schema()
    def check_loss_radiation(self, data):
        fName = 'loss_radiation'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThanEq(value, 100, fName)

    @validates_schema()
    def check_Texit(self, data):
        fName = 'Texit'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_composition_type(self, data):
        fName = 'composition_type'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        composition_type_options = ["mole_percent","mass_percent"]
        vd.xChoice(value, composition_type_options, fName)


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

    @validates_schema()
    def check_Tf(self, data):
        fName = 'Tf'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)



class docResult(Schema):
    MW = fields.Nested(sXfld)
    LHV = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
