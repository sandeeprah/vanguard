from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_option = fields.Nested(sXfld)
    NPS = fields.Nested(sXfld)
    d = fields.Nested(sXfld)
    D = fields.Nested(sXfld)
    Schedule = fields.Nested(sXfld)
    P = fields.Nested(sXfld)
    Tdesign = fields.Nested(sXfld)
    materialSpec = fields.Nested(sXfld)
    weldType = fields.Nested(sXfld)
    W = fields.Nested(sXfld)
    ca = fields.Nested(sXfld)
    h = fields.Nested(sXfld)
    ut = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_calculation_option(self, data):
        fName = 'calculation_option'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        calculation_options = ["NPS","d","D"]
        vd.xChoice(value, calculation_options, fName)


    @validates_schema()
    def check_NPS(self, data):
        if ('calculation_option' not in data):
            return
        if (data['calculation_option']['_val'] !='NPS'):
            return
        fName = 'NPS'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        nps_options = ["0.125", "0.25", "0.375", "0.5", "0.75", "1", "1.25", "1.5", "2", "2.5", "3", "3.5", "4", "5", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "34", "36"]
        vd.xChoice(value, nps_options, fName)

    @validates_schema()
    def check_d(self, data):
        if ('calculation_option' not in data):
            return
        if (data['calculation_option']['_val'] !='d'):
            return
        fName = 'd'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['length','length_mili'], fName)

    @validates_schema()
    def check_D(self, data):
        if ('calculation_option' not in data):
            return
        if (data['calculation_option']['_val'] !='D'):
            return
        fName = 'D'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['length','length_mili'], fName)

    @validates_schema()
    def check_schedule(self, data):
        fName = 'Schedule'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        schedule_options= ['5', '10', '20', '30', '40', '60', '80', '100', '120', '140', '160', 'STD', 'XS', 'XXS', '5S', '10S', '40S', '80S']
        vd.xChoice(value, schedule_options, fName)

    @validates_schema()
    def check_P(self, data):
        fName = 'P'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['pressure'], fName)

    @validates_schema()
    def check_Tdesign(self, data):
        fName = 'Tdesign'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_materialSpec(self, data):
        fName = 'materialSpec'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)

    @validates_schema()
    def check_weldType(self, data):
        fName = 'weldType'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)

    @validates_schema()
    def check_W(self, data):
        fName = 'W'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xLessThanEq(value, 1, fName)

    @validates_schema()
    def check_ca(self, data):
        fName = 'ca'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value, ['length','length_mili'], fName)

    @validates_schema()
    def check_h(self, data):
        fName = 'h'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value, ['length','length_mili'], fName)

    @validates_schema()
    def check_ut(self, data):
        fName = 'ut'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

class docResult(Schema):
    NPS = fields.Nested(sXfld)
    d = fields.Nested(sXfld)
    D = fields.Nested(sXfld)
    t = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
