from marshmallow import Schema, fields, validate, validates,  validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Prated = fields.Nested(sXfld, required=True)
    Fuel_rate_specific = fields.Nested(sXfld, required=True)

    class Meta:
        ordered = True


    @validates('Prated')
    def check_Prated(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['power'])

    @validates('Fuel_rate_specific')
    def check_Fuel_rate_specific(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['specificFuelConsumption'])



class docResult(Schema):
    Fuel_flow_rate = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates('Fuel_flow_rate')
    def check_fuel_flow_rate(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['flow'])



class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)


def checkVal(value):
    if ('_val' not in value):
        raise ValidationError('_val missing')
