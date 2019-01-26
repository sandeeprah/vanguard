from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd

class schema_load_known(Schema):
    load_desc = fields.String(required=True)
    load = fields.String(required=True)
    unit = fields.String(required=True)
    begin = fields.String(required=True)
    end = fields.String(required=True)

    class Meta:
        ordered = True

    @validates('load')
    def check_load(self, value):
        vd.fNumber(value)
        vd.fGrtThanEq(value,0)

    @validates('begin')
    def check_begin(self, value):
        vd.fNumber(value)
        vd.fGrtThanEq(value,0)

    @validates('end')
    def check_end(self, value):
        val = value.strip()
        if (val==''):
            return
        vd.fNumber(value)
        vd.fGrtThanEq(value,0)


class schema_load_random(Schema):
    load_desc = fields.String(required=True)
    load = fields.String(required=True)
    unit = fields.String(required=True)
    duration = fields.String(required=True)

    class Meta:
        ordered = True

    @validates('load')
    def check_load(self, value):
        vd.fNumber(value)
        vd.fGrtThanEq(value,0)

    @validates('duration')
    def check_duration(self, value):
        vd.fNumber(value)
        vd.fGrtThanEq(value,0)


class docInput(Schema):
    Vmin = fields.Nested(sXfld)
    Vmax = fields.Nested(sXfld)
    Vnominal = fields.Nested(sXfld)
    loads_known = fields.Nested(schema_load_known, many=True, required=True)
    loads_random = fields.Nested(schema_load_random, many=True, required=True)
    Vc_max = fields.Nested(sXfld)
    Tmax = fields.Nested(sXfld)
    Tmin = fields.Nested(sXfld)
    Tnominal = fields.Nested(sXfld)
    design_margin = fields.Nested(sXfld)
    aging_factor = fields.Nested(sXfld)
    cell_range = fields.Nested(sXfld)
    Ncell_basis = fields.Nested(sXfld)
    Ncell_manual = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_Vmin(self, data):
        fName = 'Vmin'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_Vmax(self, data):
        fName = 'Vmax'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_Vnominal(self, data):
        fName = 'Vnominal'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)


    @validates_schema()
    def check_Vc_max(self, data):
        fName = 'Vc_max'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)


    @validates_schema()
    def check_Tmax(self, data):
        fName = 'Tmax'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)

    @validates_schema()
    def check_Tmin(self, data):
        fName = 'Tmin'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)

    @validates_schema()
    def check_Tnominal(self, data):
        fName = 'Tnominal'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)

    @validates_schema()
    def check_design_margin(self, data):
        fName = 'design_margin'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_aging_factor(self, data):
        fName = 'aging_factor'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_cell_range(self, data):
        fName = 'cell_range'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        cell_range_options = ["L","M","H"]
        vd.xChoice(value, cell_range_options, fName)

    @validates_schema()
    def check_Ncell_basis(self, data):
        fName = 'Ncell_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        Ncell_basis_options = ["manual","max_possible"]
        vd.xChoice(value, Ncell_basis_options, fName)

    @validates_schema()
    def check_Ncell_manual(self, data):
        if ('Ncell_basis' not in data):
            return
        if (data['Ncell_basis']['_val'] !='manual'):
            return

        fName = 'Ncell_manual'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

class docResult(Schema):
    AH_uncorrected = fields.Nested(sXfld)
    AH_corrected = fields.Nested(sXfld)
    AH_selected = fields.Nested(sXfld)
    Cell_selected = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
