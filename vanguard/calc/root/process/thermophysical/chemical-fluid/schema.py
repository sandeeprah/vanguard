from marshmallow import Schema, fields, validate, validates
from techlib.schemautils import sDocPrj, sXfld
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    fluid = fields.Nested(sXfld, required=True)
    P = fields.Nested(sXfld, required=True)
    T = fields.Nested(sXfld, required=True)

    class Meta:
        ordered = True

    @validates('fluid')
    def check_fluid(self, value):
        vd.xString(value)
        fluid_options = CP.FluidsList()
        vd.xChoice(value, fluid_options)

    @validates('P')
    def check_P(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('T')
    def check_T(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

class docResult(Schema):
    phase = fields.Nested(sXfld)
    MW = fields.Nested(sXfld)
    Pcritical = fields.Nested(sXfld)
    Tcritical = fields.Nested(sXfld)
    Ptriple = fields.Nested(sXfld)
    Ttriple = fields.Nested(sXfld)
    acentric = fields.Nested(sXfld)
    Z = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)
    v = fields.Nested(sXfld)
    h = fields.Nested(sXfld)
    u = fields.Nested(sXfld)
    s = fields.Nested(sXfld)
    gibbs = fields.Nested(sXfld)
    helmholtz = fields.Nested(sXfld)
    Cp = fields.Nested(sXfld)
    Cv = fields.Nested(sXfld)
    Cp_molar = fields.Nested(sXfld)
    Cv_molar = fields.Nested(sXfld)
    Cp0 = fields.Nested(sXfld)
    Prandtl = fields.Nested(sXfld)
    dynViscosity = fields.Nested(sXfld)
    conductivity = fields.Nested(sXfld)
    HH = fields.Nested(sXfld)
    PH = fields.Nested(sXfld)
    GWP = fields.Nested(sXfld)
    ODP = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
