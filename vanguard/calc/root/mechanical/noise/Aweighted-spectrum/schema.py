from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld
from techlib.schemautils import validator as vd

class schema_Spectrum(Schema):
    f63 = fields.Float(required=True)
    f125 = fields.Float(required=True)
    f250 = fields.Float(required=True)
    f500 = fields.Float(required=True)
    f1000 = fields.Float(required=True)
    f2000 = fields.Float(required=True)
    f4000 = fields.Float(required=True)
    f8000 = fields.Float(required=True)

class docInput(Schema):
    unfilteredSpectrum = fields.Nested(schema_Spectrum,required=True)


class docResult(Schema):
    filteredSpectrum = fields.Nested(schema_Spectrum)
    totalAudibleNoise = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
