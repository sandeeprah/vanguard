from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError, pre_load
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP

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
    correction_option = fields.Nested(sXfld, required=True)
    totalSpectrum = fields.Nested(schema_Spectrum)
    backgroundSpectrum = fields.Nested(schema_Spectrum)
    totalNoise = fields.Nested(sXfld)
    backgroundNoise = fields.Nested(sXfld)

    @validates('correction_option')
    def check_correction_option(self, value):
        vd.xString(value)
        correction_options = ["overall","spectrum"]
        vd.xChoice(value, correction_options)

    @validates('totalNoise')
    def check_totalNoise(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('backgroundNoise')
    def check_backgroundNoise(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @pre_load()
    def remove_spectrum_if_not_needed(self, data):
        if ('correction_option' in data):
            if('_val' in data['correction_option']):
                if(data['correction_option']['_val']=='overall'):
                    for f in data['totalSpectrum']:
                        data['totalSpectrum'][f]=0
                    for f in data['backgroundSpectrum']:
                        data['backgroundSpectrum'][f]=0

        return data

class docResult(Schema):
    sourceSpectrum = fields.Nested(schema_Spectrum)
    sourceNoise = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
