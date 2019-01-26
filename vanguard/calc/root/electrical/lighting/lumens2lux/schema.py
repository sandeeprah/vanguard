from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    convert = fields.Nested(sXfld, required=True)
    lumens = fields.Nested(sXfld)
    lux = fields.Nested(sXfld)
    area_basis = fields.Nested(sXfld, required=True)
    radius = fields.Nested(sXfld)
    area = fields.Nested(sXfld)

    @validates('convert')
    def check_convert(self, value):
        vd.xString(value)
        convert_options = ["lumens2lux", "lux2lumens"]
        vd.xChoice(value, convert_options)

    @validates('lumens')
    def check_lumens(self, value):
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

    @validates('area_basis')
    def check_area_basis(self, value):
        vd.xString(value)
        area_basis_options = ["radius", "area"]
        vd.xChoice(value, area_basis_options)

    @validates('radius')
    def check_radius(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value,'length')

    @validates('area')
    def check_area(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value,'area')

    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'convert' in data:
            if (data['convert']['_val']=='lumens2lux'):
                if xisMissing(original_data, 'lumens'):
                    err_fields.append('lumens')
            if (data['convert']['_val']=='lux2lumens'):
                if xisMissing(original_data, 'lux'):
                    err_fields.append('lux')

        if 'area_basis' in data:
            if (data['area_basis']['_val']=='radius'):
                if xisMissing(original_data, 'radius'):
                    err_fields.append('radius')
            if (data['area_basis']['_val']=='area'):
                if xisMissing(original_data, 'area'):
                    err_fields.append('area')

        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)


class docResult(Schema):
    lumens = fields.Nested(sXfld)
    lux = fields.Nested(sXfld)

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
