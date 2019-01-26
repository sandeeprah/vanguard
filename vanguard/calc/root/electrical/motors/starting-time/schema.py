from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Nr = fields.Nested(sXfld, required=True)
    Cs = fields.Nested(sXfld, required=True)
    Cm = fields.Nested(sXfld, required=True)
    Jm = fields.Nested(sXfld, required=True)
    load_type = fields.Nested(sXfld, required=True)
    Cl = fields.Nested(sXfld, required=True)
    Jl = fields.Nested(sXfld, required=True)

    @validates('Nr')
    def check_Nr(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('Cs')
    def check_Cs(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('Cm')
    def check_Cm(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('Jm')
    def check_Jm(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('load_type')
    def check_load_type(self, value):
        vd.xString(value)
        item_options = ["lift", "fan", "piston_pump","flywheel"]
        vd.xChoice(value, item_options)

    @validates('Cl')
    def check_Cl(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('Jl')
    def check_Jl(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)


class docResult(Schema):
    Tacc = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
