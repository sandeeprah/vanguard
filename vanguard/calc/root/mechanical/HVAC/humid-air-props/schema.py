from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_option = fields.Nested(sXfld, required=True)
    Tdb = fields.Nested(sXfld, required=True)
    P = fields.Nested(sXfld, required=True)
    Twb = fields.Nested(sXfld)
    Tdp = fields.Nested(sXfld)
    RH = fields.Nested(sXfld)
    W = fields.Nested(sXfld)
    h = fields.Nested(sXfld)

    @validates('calculation_option')
    def check_calculation_option(self, value):
        vd.xString(value)
        calculation_options = [
                            "Tdb_RH_P",
                            "Tdb_Twb_P",
                            "Tdb_Tdp_P",
                            "Tdb_W_P",
                            "Tdb_h_P"]

        vd.xChoice(value, calculation_options)

    @validates('Tdb')
    def check_Tdb(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('P')
    def check_P(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('Twb')
    def check_Twb(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('Tdp')
    def check_Tdp(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('RH')
    def check_RH(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 1)

    @validates('W')
    def check_W(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('h')
    def check_h(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value, ['specificEnergy'])

    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'calculation_option' in data:
            if (data['calculation_option']['_val']=='Tdb_RH_P'):
                if xisMissing(original_data, 'RH'):
                    err_fields.append('RH')

            if (data['calculation_option']['_val']=='Tdb_Twb_P'):
                if xisMissing(original_data, 'Twb'):
                    err_fields.append('Twb')

            if (data['calculation_option']['_val']=='Tdb_Tdp_P'):
                if xisMissing(original_data, 'Tdp'):
                    err_fields.append('Tdp')

            if (data['calculation_option']['_val']=='Tdb_W_P'):
                if xisMissing(original_data, 'W'):
                    err_fields.append('W')

            if (data['calculation_option']['_val']=='Tdb_h_P'):
                if xisMissing(original_data, 'h'):
                    err_fields.append('h')

        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)


class docResult(Schema):
    RH = fields.Nested(sXfld)
    Twb = fields.Nested(sXfld)
    Tdp = fields.Nested(sXfld)
    W = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)
    v = fields.Nested(sXfld)
    h = fields.Nested(sXfld)
    u = fields.Nested(sXfld)
    s = fields.Nested(sXfld)
    Cp = fields.Nested(sXfld)
    Cp_ha = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
