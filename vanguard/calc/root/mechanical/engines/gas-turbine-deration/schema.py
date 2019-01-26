from marshmallow import Schema, fields, validate, validates,  validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Piso = fields.Nested(sXfld, required=True)
    Tsite = fields.Nested(sXfld, required=True)
    Hsite = fields.Nested(sXfld, required=True)
    RHsite = fields.Nested(sXfld, required=True)
    delPinlet = fields.Nested(sXfld, required=True)
    delPoutlet = fields.Nested(sXfld, required=True)
    fueltype = fields.Nested(sXfld, required=True)

    class Meta:
        ordered = True

    @validates('Piso')
    def check_Piso(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['power'])

    @validates('Tsite')
    def check_Tsite(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('Hsite')
    def check_Hsite(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['length'])

    @validates('RHsite')
    def check_RHsite(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 100)

    @validates('delPinlet')
    def check_delPinlet(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['length_mili'])

    @validates('delPoutlet')
    def check_delPoutlet(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['length_mili'])

    @validates('fueltype')
    def check_fueltype(self, value):
        vd.xString(value)
        fueltype_options = ["naturalgas", "distillate"]
        vd.xChoice(value, fueltype_options)



class docResult(Schema):
    Ltemperature = fields.Nested(sXfld)
    Lhumidity = fields.Nested(sXfld)
    Laltitude = fields.Nested(sXfld)
    Linlet = fields.Nested(sXfld)
    Loutlet = fields.Nested(sXfld)
    Lfuel = fields.Nested(sXfld)
    Ltotal = fields.Nested(sXfld)
    Psite = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)


def checkVal(value):
    if ('_val' not in value):
        raise ValidationError('_val missing')
