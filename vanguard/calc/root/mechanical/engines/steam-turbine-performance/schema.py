from marshmallow import Schema, fields, validate, validates,  validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    solve_for = fields.Nested(sXfld, required=True)
    inlet_definition = fields.Nested(sXfld, required=True)
    P_inlet = fields.Nested(sXfld, required=True)
    T_inlet = fields.Nested(sXfld, required=True)
    h_inlet = fields.Nested(sXfld, required=True)
    s_inlet = fields.Nested(sXfld, required=True)
    Q_inlet = fields.Nested(sXfld, required=True)

    turbine_definition = fields.Nested(sXfld, required=True)
    mass_flow = fields.Nested(sXfld, required=True)
    power_output = fields.Nested(sXfld, required=True)
    isentropic_efficiency = fields.Nested(sXfld, required=True)
    generator_efficiency = fields.Nested(sXfld, required=True)

    outlet_definition = fields.Nested(sXfld, required=True)
    P_outlet = fields.Nested(sXfld, required=True)
    T_outlet = fields.Nested(sXfld, required=True)
    h_outlet = fields.Nested(sXfld, required=True)
    s_outlet = fields.Nested(sXfld, required=True)
    Q_outlet = fields.Nested(sXfld, required=True)

    class Meta:
        ordered = True

    @validates('solve_for')
    def check_solve_for(self, value):
        vd.xString(value)
        solve_for_options = ["outlet_properties", "isentropic_efficiency"]
        vd.xChoice(value, solve_for_options)

    @validates('inlet_definition')
    def check_inlet_definition(self, value):
        vd.xString(value)
        inlet_definition_options = ["P-T", "P-h", "P-s", "P-Q"]
        vd.xChoice(value, inlet_definition_options)

    @validates('P_inlet')
    def check_P_inlet(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('T_inlet')
    def check_T_inlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('h_inlet')
    def check_h_inlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['specificEnergy'])

    @validates('s_inlet')
    def check_s_inlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['specificHeat'])

    @validates('Q_inlet')
    def check_Q_inlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('turbine_definition')
    def check_turbine_definition(self, value):
        vd.xString(value)
        turbine_definition_options = ["mass_flow", "power_output"]
        vd.xChoice(value, turbine_definition_options)

    @validates('mass_flow')
    def check_mass_flow(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['massflow'])

    @validates('power_output')
    def check_power_output(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['power'])

    @validates('isentropic_efficiency')
    def check_isentropic_efficiency(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 100)

    @validates('generator_efficiency')
    def check_generator_efficiency(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 100)

    @validates('outlet_definition')
    def check_outlet_definition(self, value):
        vd.xString(value)
        outlet_definition_options = ["P-T", "P-h", "P-s", "P-Q"]
        vd.xChoice(value, outlet_definition_options)


    @validates('P_outlet')
    def check_P_outlet(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('T_outlet')
    def check_T_outlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])

    @validates('h_outlet')
    def check_h_outlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['specificEnergy'])

    @validates('s_outlet')
    def check_s_outlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['specificHeat'])

    @validates('Q_outlet')
    def check_Q_outlet(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates_schema(pass_original=True)
    def check_missingvalid(self,data, original_data):
        err_fields = []
        if 'inlet_definition' in data:
            if (data['inlet_definition']['_val']=='P-T'):
                if xisMissing(original_data, 'T_inlet'):
                    err_fields.append('T_inlet')
            if (data['inlet_definition']['_val']=='P-h'):
                if xisMissing(original_data, 'h_inlet'):
                    err_fields.append('h_inlet')
            if (data['inlet_definition']['_val']=='P-s'):
                if xisMissing(original_data, 's_inlet'):
                    err_fields.append('s_inlet')
            if (data['inlet_definition']['_val']=='P-Q'):
                if xisMissing(original_data, 'Q_inlet'):
                    err_fields.append('Q_inlet')

        if 'turbine_definition' in data:
            if (data['turbine_definition']['_val']=='mass_flow'):
                if xisMissing(original_data, 'mass_flow'):
                    err_fields.append('mass_flow')
            if (data['turbine_definition']['_val']=='power_output'):
                if xisMissing(original_data, 'power_output'):
                    err_fields.append('power_output')


        if 'solve_for' in data:
            if (data['solve_for']['_val']=='outlet_properties'):
                if xisMissing(original_data, 'isentropic_efficiency'):
                    err_fields.append('isentropic_efficiency')

            if (data['solve_for']['_val']=='isentropic_efficiency'):
                if 'outlet_definition' in data:
                    if (data['outlet_definition']['_val']=='P-T'):
                        if xisMissing(original_data, 'T_outlet'):
                            err_fields.append('T_outlet')
                    if (data['outlet_definition']['_val']=='P-h'):
                        if xisMissing(original_data, 'h_outlet'):
                            err_fields.append('h_outlet')
                    if (data['outlet_definition']['_val']=='P-s'):
                        if xisMissing(original_data, 's_outlet'):
                            err_fields.append('s_outlet')
                    if (data['outlet_definition']['_val']=='P-Q'):
                        if xisMissing(original_data, 'Q_outlet'):
                            err_fields.append('Q_outlet')



        if (len(err_fields)>0):
            raise ValidationError("invalid number", err_fields)

class docResult(Schema):
    P_inlet = fields.Nested(sXfld)
    T_inlet = fields.Nested(sXfld)
    h_inlet = fields.Nested(sXfld)
    s_inlet = fields.Nested(sXfld)
    Q_inlet = fields.Nested(sXfld)
    mass_flow = fields.Nested(sXfld)
    energy_output = fields.Nested(sXfld)
    generator_efficiency = fields.Nested(sXfld)
    power_output = fields.Nested(sXfld)
    P_outlet = fields.Nested(sXfld)
    T_outlet = fields.Nested(sXfld)
    h_outlet = fields.Nested(sXfld)
    s_outlet = fields.Nested(sXfld)
    Q_outlet = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)


def checkVal(value):
    if ('_val' not in value):
        raise ValidationError('_val missing')
