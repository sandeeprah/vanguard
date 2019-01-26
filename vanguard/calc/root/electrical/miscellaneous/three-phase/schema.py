from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from techlib.schemautils import sDocPrj, sXfld, xisMissing, xisBlank
from techlib.schemautils import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    solve_using = fields.Nested(sXfld, required=True)
    VLL = fields.Nested(sXfld, required=True)
    pf = fields.Nested(sXfld, required=True)
    I = fields.Nested(sXfld)
    kW = fields.Nested(sXfld)
    kVA = fields.Nested(sXfld)
    kVAr = fields.Nested(sXfld)

    @validates('solve_using')
    def check_solve_using(self, value):
        vd.xString(value)
        item_options = ["current", "active_power", "apparent_power","reactive_power"]
        vd.xChoice(value, item_options)

    @validates('VLL')
    def check_VLL(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('pf')
    def check_pf(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xLessThanEq(value, 1)


    @validates_schema()
    def check_I(self,data):
        if ('solve_using' not in data):
            return
        solve_using = data['solve_using']['_val']
        if (solve_using != "current"):
            return

        fName = "I"
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value,fName)

    @validates_schema()
    def check_I(self,data):
        if ('solve_using' not in data):
            return
        solve_using = data['solve_using']['_val']
        if (solve_using != "current"):
            return

        fName = "I"
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value,fName)

    @validates_schema()
    def check_kW(self,data):
        if ('solve_using' not in data):
            return
        solve_using = data['solve_using']['_val']
        if (solve_using != "active_power"):
            return

        fName = "kW"
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value,fName)

    @validates_schema()
    def check_kVA(self,data):
        if ('solve_using' not in data):
            return
        solve_using = data['solve_using']['_val']
        if (solve_using != "apparent_power"):
            return

        fName = "kVA"
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value,fName)

    @validates_schema()
    def check_kVAr(self,data):
        if ('solve_using' not in data):
            return
        solve_using = data['solve_using']['_val']
        if (solve_using != "reactive_power"):
            return

        fName = "kVAr"
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value,fName)

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
