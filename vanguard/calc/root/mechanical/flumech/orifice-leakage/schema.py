from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd

class docInput(Schema):
    Pi = fields.Nested(sXfld)
    Pe = fields.Nested(sXfld)
    Ti = fields.Nested(sXfld)
    MW = fields.Nested(sXfld)
    k = fields.Nested(sXfld)
    A = fields.Nested(sXfld)
    Cd = fields.Nested(sXfld)

    class Meta:
        ordered = True

    '''
    @validates_schema()
    def check_sizing_basis(self, data):
        fName = 'sizing_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        sizing_basis_options = ["buffer_time", "switching_frequency"]
        vd.xChoice(value, sizing_basis_options, fName)
    '''

    @validates_schema()
    def check_Pi(self, data):
        fName = 'Pi'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['pressure'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Pe(self, data):
        fName = 'Pe'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['pressure'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Ti(self, data):
        fName = 'Ti'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_MW(self, data):
        fName = 'MW'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['molecularMass'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_k(self, data):
        fName = 'k'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)


    @validates_schema()
    def check_A(self, data):
        fName = 'A'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['area'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Cd(self, data):
        fName = 'Cd'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)


class docResult(Schema):
    v = fields.Nested(sXfld)
    Q = fields.Nested(sXfld)
    G = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
