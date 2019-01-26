from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
from techlib.pressuredrop.line import reducer_sizes

import CoolProp.CoolProp as CP


class sFluidData(Schema):
    medium = fields.Nested(sXfld) #Capacity, m3/s
    Q = fields.Nested(sXfld, required=True) #Capacity, m3/s
    rho = fields.Nested(sXfld, required=True) #Density, kg/m3
    mu = fields.Nested(sXfld, required=True) #Dynamic Viscosity, Pa.s
    class Meta:
        ordered = True

    @validates('medium')
    def check_medium(self, value):
        vd.xString(value)

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

    @validates('mu')
    def check_mu(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['dynViscosity'])


class sPipe(Schema):
    size_definition = fields.Nested(sXfld)
    NPS = fields.Nested(sXfld)
    Dia_inner = fields.Nested(sXfld)
    schedule = fields.Nested(sXfld )
    material = fields.Nested(sXfld)
    roughness_basis = fields.Nested(sXfld )
    roughness = fields.Nested(sXfld)
    length = fields.Nested(sXfld)
    elevation = fields.Nested(sXfld)

    class Meta:
        ordered = True


    @validates('size_definition')
    def check_size_definition(self, value):
        vd.xString(value)
        size_definition_options = ["NPS", "Custom"]
        vd.xChoice(value, size_definition_options)

    @validates('NPS')
    def check_NPS(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        nps_options = ["0.125", "0.25", "0.375", "0.5", "0.75",
                    "1", "1.25", "1.5", "2", "2.5", "3", "3.5",
                    "4", "5", "6", "8", "10", "12", "14", "16",
                    "18", "20", "22", "24", "26", "28", "30",
                    "32", "34", "36"]
        vd.xChoice(value, nps_options)

    @validates('Dia_inner')
    def check_Dia_inner(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])


    @validates('schedule')
    def check_schedule(self, value):
        vd.xString(value)
        schedule_options= ['5', '10', '20', '30', '40', '60', '80', '100', '120', '140', '160', 'STD', 'XS', 'XXS', '5S', '10S', '40S', '80S']
        vd.xChoice(value, schedule_options)

    @validates('material')
    def check_material(self, value):
        vd.xString(value)
        material_options = ["Carbon Steel(non-corroded)",
                        "Carbon Steel(corroded)",
                        "Stainless Steel",
                        "Titanium and Cu-Ni",
                        "Glass Reinforced Pipe",
                        "Polyethylene (PVC)"]

        vd.xChoice(value, material_options)

    @validates('roughness_basis')
    def check_roughness_basis(self, value):
        vd.xString(value)
        roughness_basis_options = ["Material", "Custom"]
        vd.xChoice(value, roughness_basis_options)

    @validates('roughness')
    def check_roughness(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili', 'length_micro'])

    @validates('length')
    def check_length(self, value):
        vd.xNumber(value)
        vd.xGrtThanEq(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('elevation')
    def check_elevation(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['length','length_mili'])


    @validates_schema(pass_original=True)
    def check_missing(self,data, original_data):
        err_fields = []
        if 'roughness_basis' in data:
            if (data['roughness_basis']['_val']=='Material'):
                if xisMissing(original_data,'material'):
                    err_fields.append('material')
            elif (data['roughness_basis']['_val']=='Custom'):
                if xisMissing(original_data,'roughness'):
                    err_fields.append('roughness')
        if 'size_definition' in data:
            if (data['size_definition']['_val']=='NPS'):
                if xisMissing(original_data,'NPS'):
                    err_fields.append('NPS')
                if xisMissing(original_data,'schedule'):
                    err_fields.append('schedule')
            elif (data['size_definition']['_val']=='Custom'):
                if xisMissing(original_data,'Dia_inner'):
                    err_fields.append('Dia_inner')

            if (len(err_fields)>0):
                raise ValidationError("valid input required", err_fields)





class sEntrance(Schema):
    entry_type = fields.Nested(sXfld)
    Rc = fields.Nested(sXfld)
    angle = fields.Nested(sXfld)
    wall_thickness = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates('entry_type')
    def check_entry_type(self, value):
        vd.xString(value)
        entry_type_list = ["None", "Sharp", "Rounded", "Angled", "Projecting"]
        vd.xChoice(value, entry_type_list)

    @validates('Rc')
    def check_Rc(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])

    @validates('angle')
    def check_angle(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['angle'])

    @validates('wall_thickness')
    def check_wall_thickness(self, value):
        if (xisBlank(value)):
            return
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['length','length_mili'])


    @validates_schema(pass_original=True)
    def check_missing(self,data, original_data):
        err_fields = []
        if 'entry_type' in data:
            if (data['entry_type']['_val']=='Rounded'):
                if xisMissing(original_data,'Rc'):
                    err_fields.append('Rc')
            elif (data['entry_type']['_val']=='Angled'):
                if xisMissing(original_data,'angle'):
                    err_fields.append('angle')
            elif (data['entry_type']['_val']=='Projecting'):
                if xisMissing(original_data,'wall_thickness'):
                    err_fields.append('wall_thickness')

            if (len(err_fields)>0):
                raise ValidationError("Field is required", err_fields)

    '''
    @validates_schema()
    def check_blank(self,data):
        err_fields = []
        if 'entry_type' in data:
            if (data['entry_type']['_val']=='Rounded'):
                if vd.isBlank(data,'Di'):
                    err_fields.append('Di')
                if vd.isBlank(data,'Rc'):
                    err_fields.append('Rc')
            elif (data['entry_type']['_val']=='Angled'):
                if vd.isBlank(data,'angle'):
                    err_fields.append('angle')
            elif (data['entry_type']['_val']=='Projecting'):
                if vd.isBlank(data,'Di'):
                    err_fields.append('Di')
                if vd.isBlank(data,'wall_thickness'):
                    err_fields.append('wall_thickness')

            if (len(err_fields)>0):
                raise ValidationError("Invalid Number", err_fields)
    '''

class sExit(Schema):
    exit_type = fields.Nested(sXfld)
    class Meta:
        ordered = True

    @validates('exit_type')
    def check_exit_type(self, value):
        vd.xString(value)
        exit_type_list = ["None", "Normal"]
        vd.xChoice(value, exit_type_list)


class sFitting_quantity(Schema):
    index = fields.Integer(required=True)
    quantity = fields.Integer(required=True, missing=0)
    class Meta:
        ordered = True

class sColdim_contraction(Schema):
    allowable_dims_length = ['length', 'length_mili']
    D1 = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    D2 = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    Rc = fields.String(validate=validate.OneOf(choices=allowable_dims_length))
    L = fields.String(validate=validate.OneOf(choices=allowable_dims_length))


class sContraction_sharp(Schema):
    D1 = fields.Float(required=True)
    D2 = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        ordered = True

    @validates('D1')
    def check_D1(self, value):
        vd.fGrtThan(value, 0)

    @validates('D2')
    def check_D2(self, value):
        vd.fGrtThan(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class sContractions_sharp(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_sharp, many=True)


class sContraction_rounded(Schema):
    D1 = fields.Float(required=True)
    D2 = fields.Float(required=True)
    Rc = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        ordered = True

    @validates('D1')
    def check_D1(self, value):
        vd.fGrtThan(value, 0)

    @validates('D2')
    def check_D2(self, value):
        vd.fGrtThan(value, 0)

    @validates('Rc')
    def check_Rc(self, value):
        vd.fGrtThan(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class sContractions_rounded(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_rounded, many=True)


class sContraction_conical(Schema):
    D1 = fields.Float(required=True)
    D2 = fields.Float(required=True)
    L = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        ordered = True

    @validates('D1')
    def check_D1(self, value):
        vd.fGrtThan(value, 0)

    @validates('D2')
    def check_D2(self, value):
        vd.fGrtThan(value, 0)

    @validates('L')
    def check_L(self, value):
        vd.fGrtThan(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

    @validates_schema()
    def check_contraction(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] < data['D2']):
                raise ValidationError("D1 > D2 required")

class sContractions_conical(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_conical, many=True)

class sContraction_reducer(Schema):
    size_list = reducer_sizes()
    reducer_size = fields.String(required=True, validate=validate.OneOf(choices=size_list))
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

class sContractions_reducer(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sContraction_reducer, many=True)


class sExpansion_sharp(Schema):
    D1 = fields.Float(required=True)
    D2 = fields.Float(required=True)
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

    @validates('D1')
    def check_D1(self, value):
        vd.fGrtThan(value, 0)

    @validates('D2')
    def check_D2(self, value):
        vd.fGrtThan(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class sExpansions_sharp(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_sharp, many=True)

class sExpansion_rounded(Schema):
    D1 = fields.Float(required=True)
    D2 = fields.Float(required=True)
    Rc = fields.Float(required=True)
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

    @validates('D1')
    def check_D1(self, value):
        vd.fGrtThan(value, 0)

    @validates('D2')
    def check_D2(self, value):
        vd.fGrtThan(value, 0)

    @validates('Rc')
    def check_Rc(self, value):
        vd.fGrtThan(value, 0)

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class sExpansions_rounded(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_rounded, many=True)


class sExpansion_conical(Schema):
    D1 = fields.Float(required=True)
    D2 = fields.Float(required=True)
    L = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        ordered = True

    @validates('D1')
    def check_D1(self, value):
        vd.fGrtThan(value, 0)

    @validates('D2')
    def check_D2(self, value):
        vd.fGrtThan(value, 0)

    @validates('L')
    def check_L(self, value):
        vd.fGrtThan(value, 0)

    @validates_schema()
    def check_expansion(self,data):
        if ('D1' in data) and ('D2' in data):
            if (data['D1'] > data['D2']):
                raise ValidationError("D1 < D2 required")

class sExpansions_conical(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_conical, many=True)


class sExpansion_reducer(Schema):
    size_list = reducer_sizes()
    reducer_size = fields.String(required=True, validate=validate.OneOf(choices=size_list))
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)



class sExpansions_reducer(Schema):
    _coldim = fields.Nested(sColdim_contraction)
    _list = fields.Nested(sExpansion_reducer, many=True)

class sOrifice(Schema):
    orifice_type_list = ["Thin_Sharp", "Thick"]
    orifice_type = fields.String(required=True, validate=validate.OneOf(choices=orifice_type_list))
    quantity = fields.Integer()
    class Meta:
        ordered = True

class sColdim_loss(Schema):
    deltaP = fields.String()


class sFixed_K_loss(Schema):
    K = fields.Float(required=True, validate=validate.Range(min=0))
    remark = fields.String()
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    class Meta:
        ordered = True

    @validates('K')
    def check_K(self, value):
        vd.fGrtThanEq(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)


class sFixed_K_losses(Schema):
    _coldim = fields.Nested(sColdim_loss)
    _list = fields.Nested(sFixed_K_loss, many=True)
    class Meta:
        ordered = True

class sFixed_LbyD_loss(Schema):
    LbyD = fields.Float(required=True)
    remark = fields.String()
    quantity = fields.Integer(required=True)
    class Meta:
        ordered = True

    @validates('LbyD')
    def check_LbyD(self, value):
        vd.fGrtThanEq(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

class sFixed_LbyD_losses(Schema):
    _coldim = fields.Nested(sColdim_loss)
    _list = fields.Nested(sFixed_LbyD_loss, many=True)
    class Meta:
        ordered = True



class sFixed_deltaP_loss(Schema):
    deltaP = fields.Float(required=True)
    remark = fields.String()
    quantity = fields.Integer(required=True)

    @validates('deltaP')
    def check_deltaP(self, value):
        vd.fGrtThanEq(value, 0)

    @validates('quantity')
    def check_quantity(self, value):
        vd.fGrtThanEq(value, 0)

    class Meta:
        ordered = True


class sFixed_deltaP_losses(Schema):
    _coldim = fields.Nested(sColdim_loss)
    _list = fields.Nested(sFixed_deltaP_loss, many=True)

    class Meta:
        ordered = True


class docInput(Schema):
    fluidData = fields.Nested(sFluidData)
    pipe = fields.Nested(sPipe)
    entrance = fields.Nested(sEntrance)
    exit = fields.Nested(sExit)
    fittings = fields.Nested(sFitting_quantity, many=True)
    contractions_sharp = fields.Nested(sContractions_sharp)
    contractions_rounded = fields.Nested(sContractions_rounded)
    contractions_conical = fields.Nested(sContractions_conical)
    contractions_reducer = fields.Nested(sContractions_reducer)
    expansions_sharp = fields.Nested(sExpansions_sharp)
    expansions_rounded = fields.Nested(sExpansions_rounded)
    expansions_conical = fields.Nested(sExpansions_conical)
    expansions_reducer = fields.Nested(sExpansions_reducer)
    orifice = fields.Nested(sOrifice, many=True)
    fixed_K_losses = fields.Nested(sFixed_K_losses)
    fixed_LbyD_losses = fields.Nested(sFixed_LbyD_losses)
    fixed_deltaP_losses = fields.Nested(sFixed_deltaP_losses)

    class Meta:
        ordered = True

class docResult(Schema):
    deltaP = fields.Nested(sXfld)

    @validates('deltaP')
    def check_deltaP(self, value):
        vd.xNumber(value)
        vd.xDim(value,'pressure')

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
