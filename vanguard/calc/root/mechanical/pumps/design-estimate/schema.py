from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Q = fields.Nested(sXfld, required=True)
    H = fields.Nested(sXfld, required=True)
    rho = fields.Nested(sXfld, required=True)
    mu = fields.Nested(sXfld, required=True)
    design_type = fields.Nested(sXfld, required=True)
    poles = fields.Nested(sXfld, required=True)
    frequency = fields.Nested(sXfld, required=True)

    @validates('design_type')
    def check_design_type(self, value):
        vd.xString(value)
        item_options = ["OH", "DS1", "SS2","DS2"]
        vd.xChoice(value, item_options)

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'flow')

    @validates('H')
    def check_H(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'length')

    @validates('rho')
    def check_rho(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'density')

    @validates('mu')
    def check_mu(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'dynViscosity')


    @validates('poles')
    def check_poles(self, value):
        vd.xInteger(value)
        value['_val'] = int(value['_val'])
        item_options = [2, 4, 6]
        vd.xChoice(value, item_options)

    @validates('frequency')
    def check_frequency(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)



class docResult(Schema):
    Nq = fields.Nested(sXfld)
    eta = fields.Nested(sXfld)
    psi = fields.Nested(sXfld)
    u2 = fields.Nested(sXfld)
    d2 = fields.Nested(sXfld)
    NPSHR = fields.Nested(sXfld)
    Phydraulic = fields.Nested(sXfld)
    P = fields.Nested(sXfld)
    Pmotor = fields.Nested(sXfld)
    tentative_availability = fields.Nested(sXfld)
    NPS_suction = fields.Nested(sXfld)
    NPS_discharge = fields.Nested(sXfld)
    L = fields.Nested(sXfld)
    W = fields.Nested(sXfld)
    H = fields.Nested(sXfld)
    Wpump = fields.Nested(sXfld)
    Wbase = fields.Nested(sXfld)
    Wtotal = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
