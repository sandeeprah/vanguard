from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd

class docInput(Schema):
    specie = fields.Nested(sXfld)
    MW = fields.Nested(sXfld)
    concentration_measured = fields.Nested(sXfld)
    from_units = fields.Nested(sXfld)
    sampling_basis = fields.Nested(sXfld)
    H2O_measured = fields.Nested(sXfld)
    oxygen_correction = fields.Nested(sXfld)
    O2_measured = fields.Nested(sXfld)
    O2_reference = fields.Nested(sXfld)
    to_units = fields.Nested(sXfld)
    Ts = fields.Nested(sXfld)
    Ps = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_specie(self, data):
        fName = 'specie'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        specie_options = ["NOx","SOx","CO","Other"]
        vd.xChoice(value, specie_options, fName)

    @validates_schema()
    def check_MW(self, data):
        if ('specie' not in data):
            return
        if (data['specie']['_val'] !='Other'):
            return
        fName = 'MW'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_concentration_measured(self, data):
        fName = 'concentration_measured'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_from_units(self, data):
        fName = 'from_units'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        unit_options = ["ppmv","mg/Nm3","mg/Sm3"]
        vd.xChoice(value, unit_options, fName)

    @validates_schema()
    def check_sampling_basis(self, data):
        fName = 'sampling_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        sampling_options = ["wet","dry"]
        vd.xChoice(value, sampling_options, fName)

    @validates_schema()
    def check_H2O_measured(self, data):
        if ('sampling_basis' not in data):
            return
        if (data['sampling_basis']['_val'] !='wet'):
            return
        fName = 'H2O_measured'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThan(value, 100, fName)

    @validates_schema()
    def check_oxygen_correction(self, data):
        fName = 'oxygen_correction'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        sampling_options = ["yes","no"]
        vd.xChoice(value, sampling_options, fName)

    @validates_schema()
    def check_O2_measured(self, data):
        if ('oxygen_correction' not in data):
            return
        if (data['oxygen_correction']['_val'] !='yes'):
            return
        fName = 'O2_measured'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_O2_reference(self, data):
        if ('oxygen_correction' not in data):
            return
        if (data['oxygen_correction']['_val'] !='yes'):
            return
        fName = 'O2_reference'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)

    @validates_schema()
    def check_to_units(self, data):
        fName = 'to_units'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        unit_options = ["ppmv","mg/Nm3","mg/Sm3"]
        vd.xChoice(value, unit_options, fName)

    @validates_schema()
    def check_Ts(self, data):
        if ('from_units' not in data):
            return
        if ('to_units' not in data):
            return

        Ts_reqd = False
        if (data['from_units']['_val'] =='mg/Sm3'):
            Ts_reqd = True
        if (data['to_units']['_val'] =='mg/Sm3'):
            Ts_reqd = True
        if ((data['from_units']['_val'] =='mg/Sm3') and (data['to_units']['_val'] =='mg/Sm3')):
            Ts_reqd = False

        if (not Ts_reqd):
            return

        fName = 'Ts'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_Ps(self, data):
        if ('from_units' not in data):
            return
        if ('to_units' not in data):
            return

        Ps_reqd = False
        if (data['from_units']['_val'] =='mg/Sm3'):
            Ps_reqd = True
        if (data['to_units']['_val'] =='mg/Sm3'):
            Ps_reqd = True
        if ((data['from_units']['_val'] =='mg/Sm3') and (data['to_units']['_val'] =='mg/Sm3')):
            Ps_reqd = False

        if (not Ps_reqd):
            return

        fName = 'Ps'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['pressure'],fName)

class docResult(Schema):
    concentration = fields.Nested(sXfld)
    units = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
