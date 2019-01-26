from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd

class docInput(Schema):
    sizing_basis = fields.Nested(sXfld)
    Pstd = fields.Nested(sXfld)
    Tstd = fields.Nested(sXfld)
    t = fields.Nested(sXfld)
    fs = fields.Nested(sXfld)
    Pu = fields.Nested(sXfld)
    Pl = fields.Nested(sXfld)
    Qin = fields.Nested(sXfld)
    Qout = fields.Nested(sXfld)
    Tmax = fields.Nested(sXfld)
    margin = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_sizing_basis(self, data):
        fName = 'sizing_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        sizing_basis_options = ["buffer_time", "switching_frequency"]
        vd.xChoice(value, sizing_basis_options, fName)

    @validates_schema()
    def check_Pstd(self, data):
        fName = 'Pstd'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['pressure'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Tstd(self, data):
        fName = 'Tstd'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_t(self, data):
        if ('sizing_basis' not in data):
            return
        if (data['sizing_basis']['_val'] !='buffer_time'):
            return

        fName = 't'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['time'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_fs(self, data):
        if ('sizing_basis' not in data):
            return
        if (data['sizing_basis']['_val'] !='switching_frequency'):
            return
        fName = 'fs'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Pu(self, data):
        fName = 'Pu'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['pressure'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Pl(self, data):
        fName = 'Pl'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['pressure'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Qin(self, data):
        if ('sizing_basis' not in data):
            return
        if (data['sizing_basis']['_val'] !='switching_frequency'):
            return
        fName = 'Qin'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['flow'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Qout(self, data):
        fName = 'Qout'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['flow'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Tmax(self, data):
        fName = 'Tmax'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_margin(self, data):
        fName = 'margin'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

class docResult(Schema):
    V = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
