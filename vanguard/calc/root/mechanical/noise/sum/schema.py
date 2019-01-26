from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    noiseLevelList = fields.List(fields.Float, required=True)

class docResult(Schema):
    noiseTotal = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
