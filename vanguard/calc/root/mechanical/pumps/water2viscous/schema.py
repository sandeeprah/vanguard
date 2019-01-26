from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Qbep = fields.Nested(sXfld, required=True)
    Hbep = fields.Nested(sXfld, required=True)
    speed = fields.Nested(sXfld, required=True)
    Q = fields.Nested(sXfld, required=True)
    H = fields.Nested(sXfld)
    eta = fields.Nested(sXfld)
    viscosity_basis = fields.Nested(sXfld, required=True)
    nu = fields.Nested(sXfld)
    mu = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)

    @validates('Qbep')
    def check_Qbep(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['flow'])

    @validates('Hbep')
    def check_Hbep(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length'])


    @validates('speed')
    def check_speed(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['flow'])

    @validates('H')
    def check_H(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['length'])

    @validates('eta')
    def check_eta(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('viscosity_basis')
    def check_viscosity_basis(self, value):
        vd.xString(value)
        viscosity_basis_options = ["kinematic", "dynamic"]
        vd.xChoice(value, viscosity_basis_options)

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
        if 'viscosity_basis' in data:
            if (data['viscosity_basis']['_val']=='kinematic'):
                if xisMissing(original_data, 'nu'):
                    err_fields.append('nu')
            if (data['viscosity_basis']['_val']=='dynamic'):
                if xisMissing(original_data, 'mu'):
                    err_fields.append('mu')
                if xisMissing(original_data, 'rho'):
                    err_fields.append('rho')

        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    phase = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)
    Psat = fields.Nested(sXfld)
    Tsat = fields.Nested(sXfld)
    v = fields.Nested(sXfld)
    h = fields.Nested(sXfld)
    u = fields.Nested(sXfld)
    s = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
