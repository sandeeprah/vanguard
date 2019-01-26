from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Flow = fields.Nested(sXfld)
    Pambient = fields.Nested(sXfld)
    Tambient = fields.Nested(sXfld)
    RHambient = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_Flow(self, data):
        fName = 'Flow'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value, ['flow'], fName)

    @validates_schema()
    def check_Pambient(self, data):
        fName = 'Pambient'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['pressure'], fName)

    @validates_schema()
    def check_Tambient(self, data):
        fName = 'Tambient'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_RHambient(self, data):
        fName = 'RHambient'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThanEq(value, 100, fName)


class docResult(Schema):
    FAD = fields.Nested(sXfld)

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
