from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisBlank, xisMissing
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class schema_fluidfraction(Schema):
    fluid_list = CP.FluidsList()
    fluid = fields.String(required=True, validate=validate.OneOf(choices=fluid_list))
    molefraction = fields.Float(required=True)
    class Meta:
        ordered = True

    @validates('molefraction')
    def check_molefraction(self, value):
        vd.fGrtThanEq(value,0)
        vd.fLessThanEq(value,1)



class docInput(Schema):
    P1 = fields.Nested(sXfld, required=True)
    T1 = fields.Nested(sXfld, required=True)
    P2 = fields.Nested(sXfld, required=True)
    m = fields.Nested(sXfld, required=True)
    kZ_basis = fields.Nested(sXfld, required=True)
    MW = fields.Nested(sXfld, required=True)
    k1 = fields.Nested(sXfld)
    k2 = fields.Nested(sXfld)
    kavg = fields.Nested(sXfld)
    Z1 = fields.Nested(sXfld)
    Z2 = fields.Nested(sXfld)
    Zavg = fields.Nested(sXfld)
    predict_etaP = fields.Nested(sXfld, required=True)
    etaP = fields.Nested(sXfld)
    Tlimit = fields.Nested(sXfld, required=True)
    interstage_cooling = fields.Nested(sXfld, required=True)
    Tcoolant = fields.Nested(sXfld)
    Tapproach = fields.Nested(sXfld)
    deltaP_cooler = fields.Nested(sXfld)
    Pinlet_cooler_basis = fields.Nested(sXfld)
    Pinlet_cooler = fields.Nested(sXfld)

    mixture = fields.Nested(schema_fluidfraction, many=True)
    class Meta:
        ordered = True

    @validates('P1')
    def check_P1(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('T1')
    def check_T1(self, value):
        vd.xNumber(value)
        vd.xDim(value, ['temperature'])


    @validates('P2')
    def check_P2(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['pressure'])

    @validates('m')
    def check_m(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['massflow'])

    @validates('kZ_basis')
    def check_kZ_basis(self, value):
        vd.xString(value)
        kZ_basis_options = ["A", "B"]
        vd.xChoice(value, kZ_basis_options)

    @validates('MW')
    def check_MW(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['molecularMass'])

    @validates_schema()
    def check_k1(self, data):
        if ('kZ_basis' not in data):
            return
        if (data['kZ_basis']['_val'] !='A'):
            return
        fName = 'k1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_k2(self, data):
        if ('kZ_basis' not in data):
            return
        if (data['kZ_basis']['_val'] !='A'):
            return
        fName = 'k2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Z1(self, data):
        if ('kZ_basis' not in data):
            return
        if (data['kZ_basis']['_val'] !='A'):
            return
        fName = 'Z1'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_Z2(self, data):
        if ('kZ_basis' not in data):
            return
        if (data['kZ_basis']['_val'] !='A'):
            return
        fName = 'Z2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)


    @validates_schema()
    def check_etaP(self, data):
        if ('predict_etaP' not in data):
            return
        if (data['predict_etaP']['_val'] =='Yes'):
            return
        fName = 'etaP'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)


    @validates('Tlimit')
    def check_Tlimit(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value, ['temperature'])

    @validates('interstage_cooling')
    def check_interstage_cooling(self, value):
        vd.xString(value)
        interstage_cooling_options = ["Conditional", "Yes", "No"]
        vd.xChoice(value, interstage_cooling_options)

    @validates_schema()
    def check_Tcoolant(self, data):
        if ('interstage_cooling' not in data):
            return
        if (data['interstage_cooling']['_val'] =='No'):
            return

        fName = 'Tcoolant'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_Tapproach(self, data):
        if ('interstage_cooling' not in data):
            return
        if (data['interstage_cooling']['_val'] =='No'):
            return
        fName = 'Tapproach'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)

    @validates_schema()
    def check_deltaP_cooler(self, data):
        if ('interstage_cooling' not in data):
            return
        if (data['interstage_cooling']['_val'] =='No'):
            return
        fName = 'deltaP_cooler'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['pressure'], fName)


    @validates_schema()
    def check_Pinlet_cooler_basis(self, data):
        if ('interstage_cooling' not in data):
            return
        if (data['interstage_cooling']['_val'] =='No'):
            return
        fName = 'Pinlet_cooler_basis'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        Pinlet_cooler_basis_options = ["as_specified", "geometric_mean"]
        vd.xChoice(value, Pinlet_cooler_basis_options, fName)

    @validates_schema()
    def check_Pinlet_cooler(self, data):
        if ('interstage_cooling' not in data):
            return
        if (data['interstage_cooling']['_val'] =='No'):
            return

        if ('Pinlet_cooler_basis' not in data):
            return
        if (data['Pinlet_cooler_basis']['_val'] =='geometric_mean'):
            return

        fName = 'Pinlet_cooler'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThan(value, 0, fName)
        vd.xDim(value, ['pressure'], fName)

    @validates_schema()
    def check_mixture(self, data):
        if ('kZ_basis' not in data):
            return
        if (data['kZ_basis']['_val'] !='B'):
            return
        fName = 'material'
        vd.xRequired(data,fName,fName)


    @validates_schema()
    def check_mixture(self, data):
        if ('mixture' in data):
            mixture = data['mixture']
            sigma_y = 0
            for component in mixture:
                if ('molefraction' in component):
                    sigma_y = sigma_y + component['molefraction']

            if (sigma_y <=0):
                raise ValidationError('Invalid Gas Composition Entered','schema_mixture')

class docResult(Schema):
    MW = fields.Nested(sXfld)
    Pabsorbed = fields.Nested(sXfld)
    Tdischarge = fields.Nested(sXfld)

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
