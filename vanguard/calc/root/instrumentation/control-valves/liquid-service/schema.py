from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    rho = fields.Nested(sXfld, required=True)
    Psat = fields.Nested(sXfld, required=True)
    Pc = fields.Nested(sXfld, required=True)
    mu = fields.Nested(sXfld, required=True)
    P1 = fields.Nested(sXfld, required=True)
    P2 = fields.Nested(sXfld, required=True)
    Q = fields.Nested(sXfld, required=True)
    D1 = fields.Nested(sXfld, required=True)
    D2 = fields.Nested(sXfld, required=True)
    d = fields.Nested(sXfld, required=True)
    FL = fields.Nested(sXfld, required=True)
    Fd = fields.Nested(sXfld, required=True)

    class Meta:
        ordered = True

    @validates('rho')
    def check_rho(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['density'])

    @validates('Psat')
    def check_Psat(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('Pc')
    def check_Pc(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('mu')
    def check_mu(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['dynViscosity'])

    @validates('P1')
    def check_P1(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('P2')
    def check_P2(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['flow'])

    @validates('D1')
    def check_D1(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length', 'length_mili'])

    @validates('D2')
    def check_D2(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('d')
    def check_d(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('FL')
    def check_FL(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('Fd')
    def check_Fd(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

class docResult(Schema):
    Cmetric = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
