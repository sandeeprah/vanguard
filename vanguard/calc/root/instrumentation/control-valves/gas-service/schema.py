from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    T = fields.Nested(sXfld, required=True)
    MW = fields.Nested(sXfld, required=True)
    mu = fields.Nested(sXfld, required=True)
    gamma = fields.Nested(sXfld, required=True)
    Z = fields.Nested(sXfld, required=True)
    P1 = fields.Nested(sXfld, required=True)
    P2 = fields.Nested(sXfld, required=True)
    Q = fields.Nested(sXfld, required=True)
    D1 = fields.Nested(sXfld, required=True)
    D2 = fields.Nested(sXfld, required=True)
    d = fields.Nested(sXfld, required=True)
    FL = fields.Nested(sXfld, required=True)
    Fd = fields.Nested(sXfld, required=True)
    xT = fields.Nested(sXfld, required=True)

    class Meta:
        ordered = True

    @validates('T')
    def check_temp(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('MW')
    def check_MW(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['molecularMass'])

    @validates('mu')
    def check_mu(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['dynViscosity'])

    @validates('gamma')
    def check_gamma(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('Z')
    def check_Z(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('P1')
    def check_P1(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('P2')
    def check_P2(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['flow'])

    @validates('D1')
    def check_D1(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length_mili','length'])

    @validates('D2')
    def check_D2(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length_mili','length'])


    @validates('d')
    def check_d(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length_mili','length'])

    @validates('FL')
    def check_FL(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('Fd')
    def check_Fd(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('xT')
    def check_xT(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)


class docResult(Schema):
    Cmetric = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
