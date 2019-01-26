from math import *
from techlib.units import treeUnitConvert, SI_UNITS
from copy import deepcopy
from techlib.mathutils import roundit
from techlib.mechanical.cfgpump.pump import motor_syncspeed, specific_speed, efficiency_overall, head_coefficient, nozzle_size, getNPSHR, model_select, pump_power, pump_dimensions, DN2NPS
from fluids import nearest_pipe
from techlib.electrical.motor.core import motor_params

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]

    Q = float(doc['input']['Q']['_val'])
    H = float(doc['input']['H']['_val'])
    rho = float(doc['input']['rho']['_val'])
    mu = float(doc['input']['mu']['_val'])
    poles = int(doc['input']['poles']['_val'])
    frequency = float(doc['input']['frequency']['_val'])
    design_type = doc['input']['design_type']['_val']


    try:
        Nsync = motor_syncspeed(frequency, poles)

        #assume relative slip to be zero, this can later be changed if a  better estimate is available from iec motor data
        relative_slip = 0
        Nslip = Nsync*(relative_slip/100)
        Nmotor = Nsync - Nslip

        #assuming a gear ratio of 1
        gear_ratio = 1
        Npump = Nmotor*gear_ratio
        if (design_type=='OH'):
            Qimpeller=Q
            impeller_stages=1
            Himpeller = H/impeller_stages
            Ktuning = 1
        elif(design_type=='DS1'):
            Qimpeller=Q/2
            impeller_stages=1
            Himpeller = H/impeller_stages
            Ktuning = 0.94
        elif(design_type=='SS2'):
            Qimpeller=Q
            impeller_stages=2
            Himpeller = H/impeller_stages
            Ktuning = 0.8
        elif(design_type=='DS2'):
            Qimpeller=Q/2
            impeller_stages=2
            Qimpeller=Q
            impeller_stages=2
            Himpeller = H/impeller_stages
            Ktuning = 0.80
        else:
            raise Exception('Invalid Design Type')

        try:
            Nq = specific_speed(Qimpeller, Himpeller, Npump)
        except Exception as e:
            Nq = nan
            doc['errors'].append(str(e))

        try:
            eta = efficiency_overall(Qimpeller, Nq)
        except Exception as e:
            eta = nan
            doc['errors'].append(str(e))


        try:
            psi = head_coefficient(Nq)
            psi = psi*Ktuning
        except Exception as e:
            psi = nan
            doc['errors'].append(str(e))

        try:
            g = 9.81
            u2 = sqrt((2*g*Himpeller/psi))
            d2 = (u2*60)/(pi*Npump)
        except Exception as e:
            psi = nan
            u2 = nan
            d2 = nan
            doc['errors'].append(str(e))

        try:
            NPSHR = getNPSHR(Nq, Qimpeller, Npump, design_type)
        except Exception as e:
            NPSHR = nan
            doc['errors'].append(str(e))

        try:
            Phydraulic, P, Pmotor = pump_power(Q, H, eta, rho)
        except Exception as e:
            P = nan
            Phydraulic = nan
            Pmotor = nan
            doc['errors'].append(str(e))

        try:
            selected_model = model_select(d2, Q, poles, design_type)
        except Exception as e:
            selected_model ="None"
            doc['errors'].append(str(e))

        if selected_model == 'None':
            tentative_availability = "No"
        else:
            tentative_availability = "Yes"

        try:
            Ds,Dd,L,W,H,Wpump,Wbase = pump_dimensions(selected_model, design_type)
            NPS_suction = DN2NPS(Ds)
            NPS_discharge = DN2NPS(Dd)
        except Exception as e:
            NPS_suction = nan
            NPS_discharge = nan
            L = nan
            W = nan
            H = nan
            Wpump = nan
            Wbase = nan
            Wmotor = nan
            Wtotal = nan
            doc['errors'].append(str(e))


        try:
            mtr =  motor_params(Pmotor/1000, poles)
            Wmotor = mtr['weight']
            Wtotal = Wpump+Wbase+Wmotor
        except Exception as e:
            Wmotor = nan
            Wtotal = nan
            doc['errors'].append(str(e))

    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append("Failed to calculate pump estimates. Check Inputs")

    Nq = roundit(Nq)
    eta = roundit(eta)
    psi = roundit(psi)
    u2 = roundit(u2)
    d2 = roundit(d2)
    Phydraulic = roundit(Phydraulic)
    P = roundit(P)
    NPSHR = roundit(NPSHR)

    doc['result'].update({'Nq':{'_val' : str(Nq)}})
    doc['result'].update({'eta':{'_val' : str(eta)}})
    doc['result'].update({'psi':{'_val' : str(psi)}})
    doc['result'].update({'u2':{'_val' : str(u2), '_dim':'speed'}})
    doc['result'].update({'d2':{'_val' : str(d2), '_dim':'length'}})
    doc['result'].update({'NPSHR':{'_val' : str(NPSHR), '_dim':'length'}})
    doc['result'].update({'Phydraulic':{'_val' : str(Phydraulic), '_dim':'power'}})
    doc['result'].update({'P':{'_val' : str(P), '_dim':'power'}})
    doc['result'].update({'Pmotor':{'_val' : str(Pmotor), '_dim':'power'}})

    doc['result'].update({'tentative_availability':{'_val' : str(tentative_availability)}})
    doc['result'].update({'NPS_suction':{'_val' : str(NPS_suction)}})
    doc['result'].update({'NPS_discharge':{'_val' : str(NPS_discharge)}})
    doc['result'].update({'L':{'_val' : str(L), '_dim':'length'}})
    doc['result'].update({'W':{'_val' : str(W), '_dim':'length'}})
    doc['result'].update({'H':{'_val' : str(H), '_dim':'length'}})
    doc['result'].update({'Wpump':{'_val' : str(Wpump), '_dim':'mass'}})
    doc['result'].update({'Wbase':{'_val' : str(Wbase), '_dim':'mass'}})
    doc['result'].update({'Wmotor':{'_val' : str(Wmotor), '_dim':'mass'}})
    doc['result'].update({'Wtotal':{'_val' : str(Wtotal), '_dim':'mass'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
