from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_option = fields.Nested(sXfld, required=True)
    PWL = fields.Nested(sXfld)
    SPL = fields.Nested(sXfld)
    distance = fields.Nested(sXfld)
    Q = fields.Nested(sXfld, required=True)

    @validates('calculation_option')
    def check_calculation_option(self, value):
        vd.xString(value)
        calculation_options = [
                            "calcSPL",
                            "calcPWL",
                            "calcDistance"
                            ]
        vd.xChoice(value, calculation_options)

    @validates('PWL')
    def check_PWL(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('SPL')
    def check_SPL(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('distance')
    def check_distance(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'length')

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        Q_options = ["1","2","4","8"]
        vd.xChoice(value, Q_options)


    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'calculation_option' in data:
            if (data['calculation_option']['_val']=='calcSPL'):
                if xisMissing(original_data, 'PWL'):
                    err_fields.append('PWL')
                if xisMissing(original_data, 'distance'):
                    err_fields.append('distance')

            if (data['calculation_option']['_val']=='calcPWL'):
                if xisMissing(original_data, 'SPL'):
                    err_fields.append('SPL')
                if xisMissing(original_data, 'distance'):
                    err_fields.append('distance')

            if (data['calculation_option']['_val']=='calcDistance'):
                if xisMissing(original_data, 'PWL'):
                    err_fields.append('PWL')
                if xisMissing(original_data, 'SPL'):
                    err_fields.append('SPL')


        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    PWL = fields.Nested(sXfld)
    SPL = fields.Nested(sXfld)
    distance = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
