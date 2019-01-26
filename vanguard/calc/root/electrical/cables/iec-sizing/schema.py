from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
from techlib.mathutils import roundit
import CoolProp.CoolProp as CP
from techlib.electrical.cable.cablesizing import get_available_conductors, get_available_cables, get_available_installationMethods, \
                                            get_available_installationTypes, get_available_layers, get_available_no_grpcables, \
                                            get_available_underground_spacing


class docInput(Schema):
    phases = fields.Nested(sXfld, required=True)
    voltage = fields.Nested(sXfld, required=True)
    power_factor = fields.Nested(sXfld, required=True)
    rated_load = fields.Nested(sXfld, required=True)
    load_efficiency = fields.Nested(sXfld, required=True)
    insulation_type = fields.Nested(sXfld, required=True)
    conductor_type = fields.Nested(sXfld, required=True)
    cable_type = fields.Nested(sXfld, required=True)
    installation_method = fields.Nested(sXfld, required=True)
    Tamb = fields.Nested(sXfld, required=True)
    installation_type = fields.Nested(sXfld)
    no_grpcables = fields.Nested(sXfld, required=True)
    no_layers = fields.Nested(sXfld)
    Tground = fields.Nested(sXfld)
    soil_thermal_resistivity = fields.Nested(sXfld)
    underground_spacing = fields.Nested(sXfld)
    voltage_drop_calculation = fields.Nested(sXfld, required=True)
    cable_section_manual = fields.Nested(sXfld)
    cable_run = fields.Nested(sXfld)
    allowable_drop = fields.Nested(sXfld)
    short_circuit_calculation = fields.Nested(sXfld, required=True)
    I_sc = fields.Nested(sXfld)
    t_fault = fields.Nested(sXfld)
    Tc_basis = fields.Nested(sXfld)
    Tc_init = fields.Nested(sXfld)
    Tc_final = fields.Nested(sXfld)

    class Meta:
        ordered=True

    @validates('phases')
    def check_phases(self, value):
        vd.xString(value)
        phases_options = ["single", "three"]
        vd.xChoice(value, phases_options)

    @validates('voltage')
    def check_voltage(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('power_factor')
    def check_power_factor(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xLessThanEq(value, 1)

    @validates('rated_load')
    def check_rated_load(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)

    @validates('load_efficiency')
    def check_load_efficiency(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)

    @validates('insulation_type')
    def check_insulation_type(self, value):
        vd.xString(value)
        item_options = ["PVC", "XLPE", "MIN_LT_500", "MIN_LT_750","MIN_HT_500", "MIN_HT_750"]
        vd.xChoice(value, item_options)

    @validates_schema()
    def check_conductor_type(self, data):
        if ('insulation_type' not in data):
            return

        fName = 'conductor_type'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        insulation_type = data['insulation_type']['_val']
        item_options= get_available_conductors(insulation_type)
        vd.xChoice(value, item_options, fName)

    @validates('cable_type')
    def check_cable_type(self, value):
        vd.xString(value)
        item_options = get_available_cables()
        vd.xChoice(value, item_options)


    @validates_schema()
    def check_installation_method(self, data):
        if ('insulation_type' not in data):
            return
        if ('cable_type' not in data):
            return

        fName = 'installation_method'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        insulation_type = data['insulation_type']['_val']
        cable_type = data['cable_type']['_val']
        item_options= get_available_installationMethods(insulation_type, cable_type)
        vd.xChoice(value, item_options, fName)

    @validates('Tamb')
    def check_Tamb(self, value):
        vd.xNumber(value)
        value['_val'] = int(value['_val'])
        item_options = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
        vd.xChoice(value, item_options)


    @validates_schema()
    def check_installation_type(self, data):
        if ('installation_method' not in data):
            return
        if (data['installation_method']['_val'] not in ["C","E", "F", "G"]):
            return
        if ('cable_type' not in data):
            return

        fName = 'installation_type'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        installation_method = data['installation_method']['_val']
        cable_type = data['cable_type']['_val']
        item_options= get_available_installationTypes(installation_method, cable_type)
        vd.xChoice(value, item_options, fName)


    @validates_schema()
    def check_no_grpcables(self,data):
        if 'installation_method' not in data:
            return
        installation_method = data['installation_method']['_val']

        if (installation_method =="G"):
            return

        fName = 'no_grpcables'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xInteger(value, fName)
        vd.xGrtThanEq(value, 1, fName)
        item_options = get_available_no_grpcables(installation_method)
        value['_val'] = int(value['_val'])
        vd.xChoice(value, item_options, fName)

    @validates_schema()
    def check_no_layers(self,data):
        if 'installation_method' not in data:
            return
        installation_method = data['installation_method']['_val']
        if (installation_method not in ["E", "F"]):
            return
        if 'installation_type' not in data:
            return
        installation_type = data['installation_type']['_val']
        if (installation_type =="bunched"):
            return
        fName = 'no_layers'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xInteger(value, fName)
        vd.xGrtThanEq(value, 1, fName)
        installation_type = data['installation_type']['_val']
        item_options = get_available_layers(installation_type)
        value['_val'] = int(value['_val'])
        vd.xChoice(value, item_options, fName)

    @validates_schema()
    def check_Tground(self, data):
        if ('installation_method' not in data):
            return
        if (data['installation_method']['_val'] not in ["D1","D2"]):
            return
        fName = 'Tground'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        value['_val'] = roundit(float(value['_val']))
        item_options = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
        vd.xChoice(value, item_options, fName)

    @validates_schema()
    def check_soil_thermal_resistivity(self, data):
        if ('installation_method' not in data):
            return
        if (data['installation_method']['_val'] not in ["D1","D2"]):
            return
        fName = 'soil_thermal_resistivity'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        value['_val'] = roundit(float(value['_val']))
        item_options = [0.5,0.7,1,1.5,2,2.5,3]
        vd.xChoice(value, item_options, fName)


    @validates_schema()
    def check_underground_spacing(self, data):
        if ('installation_method' not in data):
            return
        if (data['installation_method']['_val'] not in ["D1","D2"]):
            return
        fName = 'underground_spacing'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        installation_method = data['installation_method']['_val']
        item_options= get_available_underground_spacing(installation_method)
        vd.xChoice(value, item_options, fName)


    @validates('voltage_drop_calculation')
    def check_voltage_drop_calculation(self, value):
        vd.xString(value)
        item_options = ["yes","no"]
        vd.xChoice(value, item_options)

    @validates_schema()
    def check_cable_section_manual(self, data):
        if ('voltage_drop_calculation' not in data):
            return
        if (data['voltage_drop_calculation']['_val']!='yes'):
            return
        fName = 'cable_section_manual'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        value['_val'] = roundit(float(value['_val']))
        item_options=[1,1.5,2.5,4,6,10,16,25,35,50,70,95,120,150,185,240,300,400,500]
        vd.xChoice(value, item_options, fName)

    @validates_schema()
    def check_cable_run(self, data):
        if ('voltage_drop_calculation' not in data):
            return
        if (data['voltage_drop_calculation']['_val']!='yes'):
            return
        fName = 'cable_run'
        vd.xRequired(data,fName,fName) #field is required
        value = data[fName]
        vd.xNumber(value, fName) # must be number
        vd.xGrtThanEq(value,0, fName)

    @validates_schema()
    def check_allowable_drop(self, data):
        if ('voltage_drop_calculation' not in data):
            return
        if (data['voltage_drop_calculation']['_val']!='yes'):
            return
        fName = 'allowable_drop'
        vd.xRequired(data,fName,fName) #field is required
        value = data[fName]
        vd.xNumber(value, fName) # must be number
        vd.xGrtThanEq(value,0, fName)

    @validates('short_circuit_calculation')
    def check_short_circuit_calculation(self, value):
        vd.xString(value)
        item_options = ["yes","no"]
        vd.xChoice(value, item_options)

    @validates_schema()
    def check_I_sc(self, data):
        if ('short_circuit_calculation' not in data):
            return
        if (data['short_circuit_calculation']['_val']!='yes'):
            return
        fName = 'I_sc'
        vd.xRequired(data,fName,fName) #field is required
        value = data[fName]
        vd.xNumber(value, fName) # must be number
        vd.xGrtThanEq(value,0, fName)

    @validates_schema()
    def check_t_fault(self, data):
        if ('short_circuit_calculation' not in data):
            return
        if (data['short_circuit_calculation']['_val']!='yes'):
            return
        fName = 't_fault'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value,0, fName)

    @validates_schema()
    def check_Tc_basis(self, data):
        if ('short_circuit_calculation' not in data):
            return
        if (data['short_circuit_calculation']['_val']!='yes'):
            return
        fName = 'Tc_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        item_options = ["default","custom"]
        vd.xChoice(value, item_options, fName)

    @validates_schema()
    def check_Tc_init(self, data):
        if ('short_circuit_calculation' not in data):
            return
        if (data['short_circuit_calculation']['_val']!='yes'):
            return
        if ('Tc_basis' not in data):
            return
        if (data['Tc_basis']['_val']!='custom'):
            return

        fName = 'Tc_init'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)

    @validates_schema()
    def check_Tc_final(self, data):
        if ('short_circuit_calculation' not in data):
            return
        if (data['short_circuit_calculation']['_val']!='yes'):
            return
        if ('Tc_basis' not in data):
            return
        if (data['Tc_basis']['_val']!='custom'):
            return

        fName = 'Tc_final'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)






class docResult(Schema):
    FLC = fields.Nested(sXfld)
    Ibase = fields.Nested(sXfld)
    Ibase_ref = fields.Nested(sXfld)
    Iderated = fields.Nested(sXfld)
    k1 = fields.Nested(sXfld)
    k1_Ref = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
