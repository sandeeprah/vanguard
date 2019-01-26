from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Pset = fields.Nested(sXfld, required=True)
    Pover = fields.Nested(sXfld, required=True)
    Psuper = fields.Nested(sXfld,required=True)
    Psuper_is_const = fields.Nested(sXfld,required=True)
    Pbuiltup = fields.Nested(sXfld, required=True)

    Q = fields.Nested(sXfld,required=True)
    rho = fields.Nested(sXfld,required=True)
    viscosity_basis = fields.Nested(sXfld,required=True)
    mu = fields.Nested(sXfld)
    nu = fields.Nested(sXfld)
    ssu = fields.Nested(sXfld)
    valve_design = fields.Nested(sXfld,required=True)
    rupture_disc = fields.Nested(sXfld,required=True)
    Kd_basis = fields.Nested(sXfld,required=True)
    Kd_manual = fields.Nested(sXfld)
    Kw_basis = fields.Nested(sXfld,required=True)
    Kw_manual = fields.Nested(sXfld)
    Kc_basis = fields.Nested(sXfld,required=True)
    Kc_manual = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates('Pset')
    def check_Pset(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('Pover')
    def check_Pover(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 100)

    @validates('Psuper')
    def check_Psuper(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['pressure'])


    @validates('Psuper_is_const')
    def check_Psuper_is_const(self, value):
        vd.xString(value)
        Psuper_is_const_options = ["Yes", "No"]
        vd.xChoice(value, Psuper_is_const_options)

    @validates('Pbuiltup')
    def check_Pbuiltup(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['flow'])

    @validates('rho')
    def check_rho(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['density'])

    @validates('viscosity_basis')
    def check_viscosity_basis(self, value):
        vd.xString(value)
        viscosity_basis_options = ["Dynamic", "Kinematic", "SSU"]
        vd.xChoice(value, viscosity_basis_options)

    @validates('mu')
    def check_mu(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['dynViscosity'])

    @validates('nu')
    def check_mu(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['kinViscosity'])

    @validates('ssu')
    def check_ssu(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('valve_design')
    def check_valve_design(self, value):
        vd.xString(value)
        valve_design_options = ["Conventional", "Balanced", "Pilot-Operated"]
        vd.xChoice(value, valve_design_options)

    @validates('rupture_disc')
    def check_rupture_disc(self, value):
        vd.xString(value)
        rupture_disc_options = ["Yes", "No"]
        vd.xChoice(value, rupture_disc_options)

    @validates('Kd_basis')
    def check_Kd_basis(self, value):
        vd.xString(value)
        K_basis_options = ["Default", "Manual"]
        vd.xChoice(value, K_basis_options)

    @validates('Kw_basis')
    def check_Kw_basis(self, value):
        vd.xString(value)
        K_basis_options = ["Default", "Manual"]
        vd.xChoice(value, K_basis_options)

    @validates('Kc_basis')
    def check_Kc_basis(self, value):
        vd.xString(value)
        K_basis_options = ["Default", "Manual"]
        vd.xChoice(value, K_basis_options)

    @validates('Kd_manual')
    def check_Kd_manual(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)

    @validates('Kw_manual')
    def check_Kw_manual(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)

    @validates('Kc_manual')
    def check_Kc_manual(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)

    @validates_schema(pass_original=True)
    def check_missing(self,data, original_data):
        err_fields = []
        if 'viscosity_basis' in data:
            if (data['viscosity_basis']['_val']=='Dynamic'):
                if xisMissing(original_data, 'mu'):
                    err_fields.append('mu')

            if (data['viscosity_basis']['_val']=='Kinematic'):
                if xisMissing(original_data, 'nu'):
                    err_fields.append('nu')

            if (data['viscosity_basis']['_val']=='SSU'):
                if xisMissing(original_data, 'ssu'):
                    err_fields.append('ssu')

        if 'Kd_basis' in data:
            if (data['Kd_basis']['_val']=='Manual'):
                if xisMissing(original_data, 'Kd_manual'):
                    err_fields.append('Kd_manual')

        if 'Kw_basis' in data:
            if (data['Kw_basis']['_val']=='Manual'):
                if xisMissing(original_data, 'Kw_manual'):
                    err_fields.append('Kw_manual')

        if 'Kc_basis' in data:
            if (data['Kc_basis']['_val']=='Manual'):
                if xisMissing(original_data, 'Kc_manual'):
                    err_fields.append('Kc_manual')


        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)



class docResult(Schema):
    Kd = fields.Nested(sXfld)
    Kw = fields.Nested(sXfld)
    Kc = fields.Nested(sXfld)
    Kv = fields.Nested(sXfld)
    A = fields.Nested(sXfld)
    A_letter = fields.Nested(sXfld)
    A_sel = fields.Nested(sXfld)
    Qrated = fields.Nested(sXfld)
    Ratio_Q = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
