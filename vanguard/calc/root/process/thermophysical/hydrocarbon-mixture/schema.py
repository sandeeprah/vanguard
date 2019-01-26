from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class schema_fluidfraction(Schema):
    fluid_list = CP.FluidsList()
    fluid = fields.String(required=True, validate=validate.OneOf(choices=fluid_list))
    molefraction = fields.Float(required=True)
    class Meta:
        ordered = True

    @validates('molefraction')
    def check_molefraction(self, value):
        vd.fGrtThanEq(value,0)
        vd.fLessThanEq(value,1)



class docInput(Schema):
    P = fields.Nested(sXfld, required=True)
    T = fields.Nested(sXfld, required=True)
    mixture = fields.Nested(schema_fluidfraction, many=True, required=True)
    class Meta:
        ordered = True

    @validates('P')
    def check_P(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('T')
    def check_T(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates_schema()
    def check_mixture(self, data):
        mixture = data['mixture']
        sigma_y = 0
        for component in mixture:
            if ('molefraction' in component):
                sigma_y = sigma_y + component['molefraction']

        if (sigma_y <=0):
            raise ValidationError('Invalid Gas Composition Entered','schema_mixture')


class docResult(Schema):
    MW = fields.Nested(sXfld)
    Pcritical = fields.Nested(sXfld)
    Tcritical = fields.Nested(sXfld)
    Pr = fields.Nested(sXfld)
    Tr = fields.Nested(sXfld)
    acentric = fields.Nested(sXfld)
    Z_PR = fields.Nested(sXfld)
    Z_LKP = fields.Nested(sXfld)
    Z_NO = fields.Nested(sXfld)
    Cp0mass = fields.Nested(sXfld)
    Cv0mass = fields.Nested(sXfld)
    Cp0molar = fields.Nested(sXfld)
    Cv0molar = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
