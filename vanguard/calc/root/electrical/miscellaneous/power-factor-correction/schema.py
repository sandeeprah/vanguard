from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    P = fields.Nested(sXfld, required=True)
    pf_actual = fields.Nested(sXfld, required=True)
    pf_desired = fields.Nested(sXfld, required=True)

    @validates('P')
    def check_P(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('pf_actual')
    def check_pf_actual(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)

    @validates('pf_desired')
    def check_pf_actual(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)


class docResult(Schema):
    kVAr_comp = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
