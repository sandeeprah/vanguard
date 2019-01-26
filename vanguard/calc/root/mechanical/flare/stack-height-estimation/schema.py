from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    qm = fields.Nested(sXfld)
    MW = fields.Nested(sXfld)
    T = fields.Nested(sXfld)
    Z = fields.Nested(sXfld)
    LHV = fields.Nested(sXfld)
    p2 = fields.Nested(sXfld)
    Uinf = fields.Nested(sXfld)
    Ma2 = fields.Nested(sXfld)
    d_basis = fields.Nested(sXfld)
    d_manual = fields.Nested(sXfld)
    R = fields.Nested(sXfld)
    tau = fields.Nested(sXfld)
    F = fields.Nested(sXfld)
    K = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_qm(self, data):
        fName = 'qm'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xDim(value, ['massflow'], fName)

    @validates_schema()
    def check_MW(self, data):
        fName = 'MW'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['molecularMass'], fName)

    @validates_schema()
    def check_T(self, data):
        fName = 'T'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_Z(self, data):
        fName = 'Z'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_LHV(self, data):
        fName = 'LHV'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['specificEnergy'], fName)

    @validates_schema()
    def check_p2(self, data):
        fName = 'p2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['pressure'], fName)

    @validates_schema()
    def check_Uinf(self, data):
        fName = 'Uinf'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['speed'], fName)

    @validates_schema()
    def check_Ma2(self, data):
        fName = 'Ma2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_d_basis(self, data):
        fName = 'd_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        calculation_options = ["calculated","manual"]
        vd.xChoice(value, calculation_options, fName)

    @validates_schema()
    def check_d_manual(self, data):
        if ('d_basis' not in data):
            return
        if (data['d_basis']['_val'] !='manual'):
            return
        fName = 'd_manual'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['length'], fName)

    @validates_schema()
    def check_R(self, data):
        fName = 'R'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['length'], fName)

    @validates_schema()
    def check_tau(self, data):
        fName = 'tau'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_F(self, data):
        fName = 'F'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_K(self, data):
        fName = 'K'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['intensity'], fName)


class docResult(Schema):
    d = fields.Nested(sXfld)
    Q = fields.Nested(sXfld)
    L = fields.Nested(sXfld)
    rho = fields.Nested(sXfld)
    Uj = fields.Nested(sXfld)
    Uinf_by_Uj = fields.Nested(sXfld)
    Sdy_by_L = fields.Nested(sXfld)
    Sdx_by_L = fields.Nested(sXfld)
    Sdy = fields.Nested(sXfld)
    Sdx = fields.Nested(sXfld)
    D = fields.Nested(sXfld)
    R_prime = fields.Nested(sXfld)
    H_prime = fields.Nested(sXfld)
    H = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
