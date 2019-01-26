from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    state = fields.Nested(sXfld, required=True)
    P = fields.Nested(sXfld)
    T = fields.Nested(sXfld)
    Q = fields.Nested(sXfld)

    @validates('state')
    def check_state(self, value):
        vd.xString(value)
        state_options = ["Saturated_T", "Saturated_P", "Superheated_or_Compressed"]
        vd.xChoice(value, state_options)

    @validates('P')
    def check_P(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('T')
    def check_T(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('Q')
    def check_Q(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 1)

    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'state' in data:
            if (data['state']['_val']=='Saturated_T'):
                if xisMissing(original_data, 'T'):
                    err_fields.append('T')
                if xisMissing(original_data, 'Q'):
                    err_fields.append('Q')

            if (data['state']['_val']=='Saturated_P'):
                if xisMissing(original_data, 'P'):
                    err_fields.append('P')
                if xisMissing(original_data, 'Q'):
                    err_fields.append('Q')

            if (data['state']['_val']=='Superheated_or_Compressed'):
                if xisMissing(original_data, 'P'):
                    err_fields.append('P')
                if xisMissing(original_data, 'T'):
                    err_fields.append('T')

        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    phase = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)
    Psat = fields.Nested(sXfld)
    Tsat = fields.Nested(sXfld)
    v = fields.Nested(sXfld)
    h = fields.Nested(sXfld)
    u = fields.Nested(sXfld)
    s = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
