from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    convert = fields.Nested(sXfld, required=True)
    candela = fields.Nested(sXfld)
    lux = fields.Nested(sXfld)
    distance = fields.Nested(sXfld, required=True)

    @validates('convert')
    def check_convert(self, value):
        vd.xString(value)
        convert_options = ["cd2lux", "lux2cd"]
        vd.xChoice(value, convert_options)

    @validates('candela')
    def check_candela(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('lux')
    def check_lux(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('distance')
    def check_distance(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value,'length')


    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'convert' in data:
            if (data['convert']['_val']=='cd2lux'):
                if xisMissing(original_data, 'candela'):
                    err_fields.append('candela')
            if (data['convert']['_val']=='lux2cd'):
                if xisMissing(original_data, 'lux'):
                    err_fields.append('lux')

        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)


class docResult(Schema):
    candela = fields.Nested(sXfld)
    lux = fields.Nested(sXfld)

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
