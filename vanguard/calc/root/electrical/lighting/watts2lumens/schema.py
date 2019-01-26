from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    convert = fields.Nested(sXfld, required=True)
    watts = fields.Nested(sXfld)
    lumens = fields.Nested(sXfld)
    luminous_efficacy = fields.Nested(sXfld, required=True)

    @validates('convert')
    def check_convert(self, value):
        vd.xString(value)
        convert_options = ["watts2lumens", "lumens2watts"]
        vd.xChoice(value, convert_options)

    @validates('watts')
    def check_watts(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('lumens')
    def check_lumens(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('luminous_efficacy')
    def check_luminous_efficacy(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)


    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'convert' in data:
            if (data['convert']['_val']=='watts2lumens'):
                if xisMissing(original_data, 'watts'):
                    err_fields.append('watts')
            if (data['convert']['_val']=='lumens2watts'):
                if xisMissing(original_data, 'lumens'):
                    err_fields.append('lumens')

        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)


class docResult(Schema):
    watts = fields.Nested(sXfld)
    lumens = fields.Nested(sXfld)

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
