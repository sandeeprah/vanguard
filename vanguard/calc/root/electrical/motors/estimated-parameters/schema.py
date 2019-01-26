from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    motor_power = fields.Nested(sXfld, required=True)
    poles = fields.Nested(sXfld, required=True)

    @validates('motor_power')
    def check_motor_power(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value,'power')


    @validates('poles')
    def check_poles(self, value):
        vd.xInteger(value)
        value['_val'] = int(value['_val'])
        item_options = [2, 4, 6]
        vd.xChoice(value, item_options)



class docResult(Schema):
    motor_rating = fields.Nested(sXfld)
    Frame_Size = fields.Nested(sXfld)
    Speed = fields.Nested(sXfld)
    eta_full = fields.Nested(sXfld)
    eta_three_fourth = fields.Nested(sXfld)
    eta_half = fields.Nested(sXfld)
    pf = fields.Nested(sXfld)
    In = fields.Nested(sXfld)
    Is_by_In = fields.Nested(sXfld)
    Tn = fields.Nested(sXfld)
    Ti_by_Tn = fields.Nested(sXfld)
    Tb_by_Tn = fields.Nested(sXfld)
    J = fields.Nested(sXfld)
    weight = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
