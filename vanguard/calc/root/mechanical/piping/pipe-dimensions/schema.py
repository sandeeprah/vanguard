from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_option = fields.Nested(sXfld, required=True)
    Schedule = fields.Nested(sXfld, required=True)
    NPS = fields.Nested(sXfld)
    Di = fields.Nested(sXfld)
    Do = fields.Nested(sXfld)

    @validates('calculation_option')
    def check_calculation_option(self, value):
        vd.xString(value)
        calculation_options = ["NPS","Di","Do"]
        vd.xChoice(value, calculation_options)

    @validates('Schedule')
    def check_schedule(self, value):
        vd.xString(value)
        schedule_options= ['5', '10', '20', '30', '40', '60', '80', '100', '120', '140', '160', 'STD', 'XS', 'XXS', '5S', '10S', '40S', '80S']
        vd.xChoice(value, schedule_options)

    @validates('NPS')
    def check_nps(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        nps_options = ["0.125", "0.25", "0.375", "0.5", "0.75", "1", "1.25", "1.5", "2", "2.5", "3", "3.5", "4", "5", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "34", "36"]
        vd.xChoice(value, nps_options)

    @validates('Di')
    def check_Di(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('Do')
    def check_Do(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates_schema(pass_original=True)
    def check_missing(self,data, original_data):
        err_fields = []
        if 'calculation_option' in data:
            if (data['calculation_option']['_val']=='NPS'):
                if xisMissing(original_data, 'NPS'):
                    err_fields.append('NPS')
            if (data['calculation_option']['_val']=='Di'):
                if xisMissing(original_data, 'Di'):
                    err_fields.append('Di')
            if (data['calculation_option']['_val']=='Do'):
                if xisMissing(original_data, 'Do'):
                    err_fields.append('Do')

        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)


class docResult(Schema):
    NPS = fields.Nested(sXfld)
    Di = fields.Nested(sXfld)
    Do = fields.Nested(sXfld)
    t = fields.Nested(sXfld)

    @validates('NPS')
    def check_nps(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        nps_options = ["0.125", "0.25", "0.375", "0.5", "0.75", "1", "1.25", "1.5", "2", "2.5", "3", "3.5", "4", "5", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "34", "36"]
        vd.xChoice(value, nps_options)

    @validates('Di')
    def check_Di(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('Do')
    def check_Do(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('t')
    def check_t(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
