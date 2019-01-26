from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd

class docInput(Schema):
    ups_load_kW = fields.Nested(sXfld)
    lagging_pf = fields.Nested(sXfld)
    ups_efficiency = fields.Nested(sXfld)
    design_margin = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_ups_load_kW(self, data):
        fName = 'ups_load_kW'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_lagging_pf(self, data):
        fName = 'lagging_pf'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_ups_efficiency(self, data):
        fName = 'ups_efficiency'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_design_margin(self, data):
        fName = 'design_margin'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)


class docResult(Schema):
    ups_rating_kVA = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
