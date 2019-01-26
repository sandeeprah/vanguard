from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd

class docInput(Schema):
    Shape = fields.Nested(sXfld)
    Orientation = fields.Nested(sXfld)
    D_basis = fields.Nested(sXfld)
    D = fields.Nested(sXfld)
    Do = fields.Nested(sXfld)
    Z = fields.Nested(sXfld)
    Pi = fields.Nested(sXfld)
    Ti = fields.Nested(sXfld)
    Tt = fields.Nested(sXfld)
    full_vacuum = fields.Nested(sXfld)
    ca = fields.Nested(sXfld)
    E = fields.Nested(sXfld)
    Ec = fields.Nested(sXfld)
    El = fields.Nested(sXfld)
    MOC = fields.Nested(sXfld)
    S = fields.Nested(sXfld)
    St = fields.Nested(sXfld)
    tn = fields.Nested(sXfld)
    Head1 = fields.Nested(sXfld)
    beta1 = fields.Nested(sXfld)
    L1 = fields.Nested(sXfld)
    r1 = fields.Nested(sXfld)
    alpha1 = fields.Nested(sXfld)
    tn1 = fields.Nested(sXfld)
    Head2 = fields.Nested(sXfld)
    beta2 = fields.Nested(sXfld)
    L2 = fields.Nested(sXfld)
    r2 = fields.Nested(sXfld)
    alpha2 = fields.Nested(sXfld)
    tn2 = fields.Nested(sXfld)
    zeta = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_Shape(self, data):
        fName = 'Shape'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        Shape_options = ["cylindrical", "spherical"]
        vd.xChoice(value, Shape_options, fName)

    @validates_schema()
    def check_Orientation(self, data):
        fName = 'Orientation'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        Orientation_options = ["horizontal", "vertical"]
        vd.xChoice(value, Orientation_options, fName)


    @validates_schema()
    def check_D_basis(self, data):
        fName = 'D_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        D_basis_options = ["inner","outer"]
        vd.xChoice(value, D_basis_options, fName)

    @validates_schema()
    def check_D(self, data):
        if ('D_basis' not in data):
            return
        if (data['D_basis']['_val'] !='inner'):
            return
        fName = 'D'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['length'],fName)
        vd.xGrtThan(value, 0, fName)


    @validates_schema()
    def check_Do(self, data):
        if ('D_basis' not in data):
            return
        if (data['D_basis']['_val'] !='outer'):
            return
        fName = 'Do'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_Z(self, data):
        fName = 'Z'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['length'],fName)


    @validates_schema()
    def check_Pi(self, data):
        fName = 'Pi'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['pressure'],fName)

    @validates_schema()
    def check_Ti(self, data):
        fName = 'Ti'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_Tt(self, data):
        fName = 'Tt'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['temperature'],fName)

    @validates_schema()
    def check_full_vacuum(self, data):
        fName = 'full_vacuum'
#        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        full_vacuum_options = ["yes", "no"]
        vd.xChoice(value, full_vacuum_options, fName)

    @validates_schema()
    def check_ca(self, data):
        fName = 'ca'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value,['length'],fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_E(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='spherical'):
            return
        fName = 'E'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xLessThanEq(value, 1, fName)

    @validates_schema()
    def check_Ec(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        fName = 'Ec'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xLessThanEq(value, 1, fName)

    @validates_schema()
    def check_El(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        fName = 'El'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xLessThanEq(value, 1, fName)

    @validates_schema()
    def check_MOC(self, data):
        fName = 'MOC'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        MOC_options = ["SA285-GrC", "SA516-Gr55","SA516-Gr60", "SA516-Gr70","SA240-Tp304L","SA240-Tp316L", "Other"]
        vd.xChoice(value, MOC_options, fName)

    @validates_schema()
    def check_S(self, data):
        if ('MOC' not in data):
            return
        if (data['MOC']['_val'] !='Other'):
            return
        fName = 'S'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['pressure'],fName)

    @validates_schema()
    def check_St(self, data):
        if ('MOC' not in data):
            return
        if (data['MOC']['_val'] !='Other'):
            return
        fName = 'St'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['pressure'],fName)

    @validates_schema()
    def check_tn(self, data):
        fName = 'tn'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_Head1(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        fName = 'Head1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        head_options = ["ellipsoidal", "torispherical", "hemispherical", "conical", "toriconical"]
        vd.xChoice(value, head_options, fName)

    @validates_schema()
    def check_beta1(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head1' not in data):
            return
        if (data['Head1']['_val'] !='ellipsoidal'):
            return

        fName = 'beta1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_L1(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head1' not in data):
            return
        if (data['Head1']['_val'] !='torispherical'):
            return

        fName = 'L1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_r1(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head1' not in data):
            return
        if (data['Head1']['_val'] !='torispherical') and (data['Head1']['_val'] !='toriconical'):
            return

        fName = 'r1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_alpha1(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head1' not in data):
            return
        if (data['Head1']['_val'] !='conical') and (data['Head1']['_val'] !='toriconical'):
            return

        fName = 'alpha1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_tn1(self, data):
        fName = 'tn1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_Head2(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return

        fName = 'Head2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        head_options = ["ellipsoidal", "torispherical", "hemispherical", "conical", "toriconical"]
        vd.xChoice(value, head_options, fName)

    @validates_schema()
    def check_beta2(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head2' not in data):
            return
        if (data['Head2']['_val'] !='ellipsoidal'):
            return


        fName = 'beta2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_L2(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head2' not in data):
            return
        if (data['Head2']['_val'] !='torispherical'):
            return

        fName = 'L2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_r2(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head2' not in data):
            return
        if (data['Head2']['_val'] !='torispherical') and (data['Head2']['_val'] !='toriconical'):
            return

        fName = 'r2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_alpha2(self, data):
        if ('Shape' not in data):
            return
        if (data['Shape']['_val'] !='cylindrical'):
            return
        if ('Head2' not in data):
            return
        if (data['Head2']['_val'] !='conical') and (data['Head2']['_val'] !='toriconical'):
            return

        fName = 'alpha2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_tn2(self, data):
        fName = 'tn2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value,['length'],fName)

    @validates_schema()
    def check_zeta(self, data):
        fName = 'zeta'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)


class docResult(Schema):
    R_calc = fields.Nested(sXfld)
    Ro_calc = fields.Nested(sXfld)
    S = fields.Nested(sXfld)

    ta = fields.Nested(sXfld)

    condn_Pc = fields.Nested(sXfld)
    tc = fields.Nested(sXfld)
    condn_tc = fields.Nested(sXfld)
    MAWPc = fields.Nested(sXfld)

    condn_Pl = fields.Nested(sXfld)
    tl = fields.Nested(sXfld)
    condn_tl = fields.Nested(sXfld)
    MAWPl = fields.Nested(sXfld)

    tu = fields.Nested(sXfld)
    t = fields.Nested(sXfld)
    tr = fields.Nested(sXfld)
    MAWP = fields.Nested(sXfld)
    tn_adequate = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
