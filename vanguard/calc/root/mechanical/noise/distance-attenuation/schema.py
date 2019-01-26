from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    source_option = fields.Nested(sXfld, required=True)
    SPL1 = fields.Nested(sXfld, required=True)
    R1 = fields.Nested(sXfld,required=True)
    R2 = fields.Nested(sXfld,required=True)
    width = fields.Nested(sXfld)
    height = fields.Nested(sXfld)


    @validates('source_option')
    def check_source_option(self, value):
        vd.xString(value)
        source_options = ["point","line","wall"]
        vd.xChoice(value, source_options)

    @validates('SPL1')
    def check_SPL1(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('R1')
    def check_R1(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'length')

    @validates('R2')
    def check_R2(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'length')

    @validates('width')
    def check_width(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value,'length')

    @validates('height')
    def check_height(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value,'length')

    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'source_option' in data:
            if (data['source_option']['_val']=='wall'):
                if xisMissing(original_data, 'width'):
                    err_fields.append('width')
                if xisMissing(original_data, 'height'):
                    err_fields.append('height')


        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    SPL2 = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
