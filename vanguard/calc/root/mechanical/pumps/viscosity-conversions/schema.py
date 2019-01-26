from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    convert = fields.Nested(sXfld, required=True)
    nu = fields.Nested(sXfld)
    mu = fields.Nested(sXfld)
    ssu = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)

    @validates('convert')
    def check_convert(self, value):
        vd.xString(value)
        convert_options = ["nu2mu", "mu2nu", "nu2ssu", "ssu2nu", "mu2ssu", "ssu2mu"]
        vd.xChoice(value, convert_options)


    @validates('nu')
    def check_nu(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['kinViscosity'])

    @validates('mu')
    def check_mu(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['dynViscosity'])

    @validates('ssu')
    def check_ssu(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('rho')
    def check_rho(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['density'])

    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'convert' in data:
            if (data['convert']['_val']=='nu2mu'):
                if xisMissing(original_data, 'nu'):
                    err_fields.append('nu')
                if xisMissing(original_data, 'rho'):
                    err_fields.append('rho')
            if (data['convert']['_val']=='mu2nu'):
                if xisMissing(original_data, 'mu'):
                    err_fields.append('mu')
                if xisMissing(original_data, 'rho'):
                    err_fields.append('rho')
            if (data['convert']['_val']=='nu2ssu'):
                if xisMissing(original_data, 'nu'):
                    err_fields.append('nu')
            if (data['convert']['_val']=='ssu2nu'):
                if xisMissing(original_data, 'ssu'):
                    err_fields.append('ssu')
            if (data['convert']['_val']=='mu2ssu'):
                if xisMissing(original_data, 'mu'):
                    err_fields.append('mu')
                if xisMissing(original_data, 'rho'):
                    err_fields.append('rho')
            if (data['convert']['_val']=='ssu2mu'):
                if xisMissing(original_data, 'ssu'):
                    err_fields.append('ssu')
                if xisMissing(original_data, 'rho'):
                    err_fields.append('rho')

        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)


class docResult(Schema):
    nu = fields.Nested(sXfld)
    mu = fields.Nested(sXfld)
    ssu = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
