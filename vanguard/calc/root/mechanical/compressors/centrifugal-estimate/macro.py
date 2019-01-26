import CoolProp.CoolProp as CP
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from techlib.mechanical.compressor.comp_api617 import Hpolytropic, absPower, Tdischarge, Qactual, polyeff, nexp, centframe, theta, HpmaxWheel
from techlib.thermochem.thermochem_utils import mixture_props
from math import *

from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

#    Get essential data
    P1 = float(doc['input']['P1']['_val'])
    T1 = float(doc['input']['T1']['_val'])
    P2 = float(doc['input']['P2']['_val'])
    m = float(doc['input']['m']['_val'])

# check if gas properties are already defined at inlet and outlet or to be determined from gas mixture.
    kZ_basis = doc['input']['kZ_basis']['_val']


# determine inlet properties MW, k1 and Z1
    if (kZ_basis =='A'):
        MW = float(doc['input']['MW']['_val'])
        k1 = float(doc['input']['k1']['_val'])
        Z1 = float(doc['input']['Z1']['_val'])

    elif (kZ_basis =='B'):
        mixture = doc['input']['mixture']
        try:
            props1 = mixture_props(mixture, P=P1, T=T1)
            MW = props1['MW']
            k1 = props1['k']
            Z1 = props1['Z_PR']
        except Exception as e :
            MW = nan
            k1 = nan
            Z1 = nan
            doc['errors'].append(str(e))
            doc['errors'].append('mixture properties could not be evaluated. check inputs')
    else:
        raise Exception('Invalid option for kZ_basis')

# determine actual volume flow rate at inlet
    Qact = Qactual(MW, P1, T1, Z1, m)


# assume single stage compression

# determine polytropic efficiencies if not given from volumetric flow rate
    predict_etaP = doc['input']['predict_etaP']['_val']
    if (predict_etaP == "No"):
        etaP = float(doc['input']['etaP']['_val'])
    else:
        etaP = polyeff(Qact)

# determine outlet k2, Z2 and discharge temperature T2
    if (kZ_basis =='A'):
        k2 = float(doc['input']['k2']['_val'])
        Z2 = float(doc['input']['Z2']['_val'])
        kavg = (k1+k2)/2
        Zavg = (Z1+Z2)/2
        n = nexp(kavg, etaP)
        T2 = Tdischarge(T1, P1, P2, n=n)

    if (kZ_basis =='B'):
        try:
            T2 = Tdischarge(T1, P1, P2, etap = etaP, mixture=mixture)
            props2 = mixture_props(mixture, P=P2, T=T2)
            k2 = props2['k']
            Z2 = props2['Z_PR']
            kavg = (k1+k2)/2
            Zavg = (Z1+Z2)/2
        except Exception as e:
            T2 = nan
            k2 = nan
            kavg = nan
            Zavg = nan
            doc['errors'].append(str(e))
            doc['errors'].append('mixture properties could not be evaluated. check inputs')


# check if discharge temperature limit is exceeded
    Tlimit = float(doc['input']['Tlimit']['_val'])
    if (T2 > Tlimit):
        intercooling_required = True
    else:
        intercooling_required = False

    #    doc['errors'].append('Discharge temperature limit is exceeded. Add intercooling and/or reduce pressure ratio')

# determine intercooling requirement
    interstage_cooling = doc['input']['interstage_cooling']['_val'] # requirement as specified by user

    if (interstage_cooling=='Yes'):
        perform_intercooling = True
    elif (interstage_cooling =='No'):
        perform_intercooling = False
    else:
        if (intercooling_required):
            perform_intercooling = True
        else:
            perform_intercooling = False



    if (not perform_intercooling):
        stages = 1
        try:
            Hp = Hpolytropic(Zavg, MW, T1, kavg, P1, P2, etaP)
            Pabs = absPower(m, Hp, etaP)
        except Exception as e:
            Hp = nan
            Pabs = nan
            doc['errors'].append(str(e))
            doc['errors'].append('polytropic and head could not be calculated. check inputs')



        Qact = roundit(Qact)
        d2, Nnominal = centframe(Qact)
        th =  theta(MW, k1, Z1, T1)
        hpmax = HpmaxWheel(th, sour='Yes')
        Nimpeller = ceil(Hp/hpmax)
        N = Nnominal*sqrt(Hp/(hpmax*Nimpeller))


        T2 = roundit(T2)
        kavg = roundit(kavg)
        Zavg = roundit(Zavg)
        etaP = roundit(etaP)
        Hp = roundit(Hp)
        Pabs = roundit(Pabs)
        N = roundit(N)

        doc['result'].update({'stages':{'_val' : str(stages)}})
        doc['result'].update({'P1':{'_val' : str(P1), '_dim':'pressure'}})
        doc['result'].update({'T1':{'_val' : str(T1), '_dim':'temperature'}})
        doc['result'].update({'P2':{'_val' : str(P2), '_dim':'pressure'}})
        doc['result'].update({'T2':{'_val' : str(T2), '_dim':'temperature'}})
        doc['result'].update({'m':{'_val' : str(m), '_dim':'massflow'}})
        doc['result'].update({'MW':{'_val' : str(MW), '_dim':'molecularMass'}})
        doc['result'].update({'Qact':{'_val' : str(Qact), '_dim':'flow'}})
        doc['result'].update({'kavg':{'_val' : str(kavg)}})
        doc['result'].update({'Zavg':{'_val' : str(Zavg)}})
        doc['result'].update({'etaP':{'_val' : str(etaP)}})
        doc['result'].update({'Hp':{'_val' : str(Hp)}})
        doc['result'].update({'Pabs':{'_val' : str(Pabs), '_dim':'power'}})
        doc['result'].update({'d2':{'_val' : str(d2), '_dim':'length'}})
        doc['result'].update({'N':{'_val' : str(N)}})
        doc['result'].update({'Nimpeller':{'_val' : str(Nimpeller)}})
    else:
        stages = 2

        # check how the interstage pressure is to be determined
        Pinlet_cooler_basis = doc['input']['Pinlet_cooler_basis']['_val'] # requirement as specified by user

        if (Pinlet_cooler_basis =='as_specified'):
            Pinlet_cooler = float(doc['input']['Pinlet_cooler']['_val'])

        elif (Pinlet_cooler_basis =='geometric_mean'):
            Pinlet_cooler = sqrt(P1*P2)
            Pinlet_cooler = roundit(Pinlet_cooler)
        else:
            raise Exception('Invalid choice for Pinlet_cooler_basis')


        Tcoolant = float(doc['input']['Tcoolant']['_val'])
        Tapproach = float(doc['input']['Tapproach']['_val'])
        deltaP_cooler = float(doc['input']['deltaP_cooler']['_val'])

        P1_1 = P1
        P2_1 = Pinlet_cooler
        P1_2 = Pinlet_cooler - deltaP_cooler
        P2_2 = P2
        T1_1 = T1
        T1_2 = Tcoolant + Tapproach



        # determine first stage properties
        if (kZ_basis =='A'):
            k1_1 = k1
            k2_1 = kavg
            k1_2 = kavg
            k2_2 = k2

            Z1_1 = Z1
            Z2_1 = Zavg
            Z1_2 = Zavg
            Z2_2 = Z2

            kavg_1 = (k1_1+k2_1)/2
            kavg_2 = (k1_2+k2_2)/2
            Zavg_1 = (Z1_1+Z2_2)/2
            Zavg_2 = (Z1_2+Z2_2)/2


            '''
            kavg_1 = 0.75*k1 + 0.25*k2
            kavg_2 = 0.25*k1 + 0.75*k2
            Zavg_1 = 0.75*Z1 + 0.25*Z2
            Zavg_2 = 0.25*Z1 + 0.75*Z2
            '''

            MW_1 = MW
            MW_2 = MW
            Z1_1 = Z1
            Z1_2 = (Z1+Z2)/2
            m_1 = m
            m_2 = m
            Qact_1 = Qactual(MW_1, P1_1, T1_1, Z1_1, m_1)
            Qact_2 = Qactual(MW_2, P1_2, T1_2, Z1_2, m_2)
            if (predict_etaP == "No"):
                etaP_1 = etaP
                etaP_2 = etaP
            else:
                etaP_1 = polyeff(Qact_1)
                etaP_2 = polyeff(Qact_2)


            n_1 = nexp(kavg_1, etaP_1)
            T2_1 = Tdischarge(T1_1, P1_1, P2_1, n=n_1)
            n_2 = nexp(kavg_2, etaP_2)
            T2_2 = Tdischarge(T1_2, P1_2, P2_2, n=n_2)


        if (kZ_basis == 'B'):
            # getting all stage 1 properties
            mixture_1 = mixture
            try:
                props1_1 = mixture_props(mixture_1, P=P1_1, T=T1_1)
                MW_1 = props1_1['MW']
                Z1_1 = props1_1['Z_PR']
                k1_1 = props1_1['k']
            except Exception as e:
                MW_1 = nan
                Z1_1 = nan
                k1_1 = nan
                doc['errors'].append(str(e))
                doc['errors'].append('mixture properties could not be evaluated. check inputs')


            m_1 = m
            Qact_1 = Qactual(MW_1, P1_1, T1_1, Z1_1, m_1)
            if (predict_etaP == "No"):
                etaP_1 = etaP
            else:
                etaP_1 = polyeff(Qact_1)

            try:
                T2_1 = Tdischarge(T1_1, P1_1, P2_1, etap = etaP_1, mixture=mixture_1)
                props2_1 = mixture_props(mixture_1, P=P2_1, T=T2_1)
                k2_1 = props2_1['k']
                Z2_1 = props2_1['Z_PR']
                kavg_1 = (k1_1+k2_1)/2
                Zavg_1 = (Z1_1+Z2_1)/2
            except Exception as e:
                T2_1 = nan
                k2_1 = nan
                Z2_1 = nan
                kavg_1 = nan
                Zavg_1 = nan
                doc['errors'].append(str(e))
                doc['errors'].append('mixture properties could not be evaluated. check inputs')


            # getting all stage 2 properties
            mixture_2 = mixture
            try:
                props1_2 = mixture_props(mixture_2, P=P1_2, T=T1_2)
                MW_2 = props1_2['MW']
                Z1_2 = props1_2['Z_PR']
                k1_2 = props1_2['k']
            except Exception as e:
                MW_2 = nan
                Z1_2 = nan
                k1_2 = nan
                doc['errors'].append(str(e))
                doc['errors'].append('mixture properties could not be evaluated. check inputs')


            m_2 = m
            Qact_2 = Qactual(MW_2, P1_2, T1_2, Z1_2, m_2)
            if (predict_etaP == "No"):
                etaP_2 = etaP
            else:
                etaP_2 = polyeff(Qact_2)

            try:
                T2_2 = Tdischarge(T1_2, P1_2, P2_2, etap = etaP_2, mixture=mixture_2)
                props2_2 = mixture_props(mixture_2, P=P2_2, T=T2_2)
                k2_2 = props2_2['k']
                Z2_2 = props2_2['Z_PR']
                kavg_2 = (k1_2+k2_2)/2
                Zavg_2 = (Z1_2+Z2_2)/2
            except Exception as e:
                T2_2 = nan
                props2_2 = nan
                k2_2 = nan
                Z2_2 = nan
                kavg_2 = nan
                Zavg_2 = nan
                doc['errors'].append(str(e))
                doc['errors'].append('mixture properties could not be evaluated. check inputs')


        try:
            Hp_1 = Hpolytropic(Zavg_1, MW_1, T1_1, kavg_1, P1_1, P2_1, etaP_1)
            Pabs_1 = absPower(m_1, Hp_1, etaP_1)
            Hp_2 = Hpolytropic(Zavg_2, MW_2, T1_2, kavg_2, P1_2, P2_2, etaP_2)
            Pabs_2 = absPower(m_2, Hp_2, etaP_2)
        except Exception as e:
            Hp_1 = nan
            Pabs_1 = nan
            Hp_2 = nan
            Pabs_2 = nan
            doc['errors'].append(str(e))
            doc['errors'].append('polytropic and head could not be calculated. check inputs')


        d2, Nnominal = centframe(Qact_1)
        th =  theta(MW_1, k1_1, Z1_1, T1_1)
        hpmax = HpmaxWheel(th, sour='Yes')
        Nimpeller_1 = ceil(Hp_1/hpmax)
        Nimpeller_2 = ceil(Hp_2/hpmax)
        N_1 = Nnominal*sqrt(Hp_1/(hpmax*Nimpeller_1))
        N_2 = Nnominal*sqrt(Hp_2/(hpmax*Nimpeller_2))
        if (N_1 > N_2):
            N = N_1
        else:
            N = N_2

        N = roundit(N)


        m_1 = roundit(m_1)
        MW_1 = roundit(MW_1)
        Qact_1 = roundit(Qact_1)
        kavg_1 = roundit(kavg_1)
        Zavg_1 = roundit(Zavg_1)
        etaP_1 = roundit(etaP_1)
        Hp_1 = roundit(Hp_1)
        Pabs_1 = roundit(Pabs_1)

        m_2 = roundit(m_2)
        MW_2 = roundit(MW_2)
        Qact_2 = roundit(Qact_2)
        kavg_2 = roundit(kavg_2)
        Zavg_2 = roundit(Zavg_2)
        etaP_2 = roundit(etaP_2)
        Hp_2 = roundit(Hp_2)
        Pabs_2 = roundit(Pabs_2)

        doc['result'].update({'stages':{'_val' : str(stages)}})

        doc['result'].update({'P1_1':{'_val' : str(P1_1), '_dim':'pressure'}})
        doc['result'].update({'T1_1':{'_val' : str(T1_1), '_dim':'temperature'}})
        doc['result'].update({'P2_1':{'_val' : str(P2_1), '_dim':'pressure'}})
        doc['result'].update({'T2_1':{'_val' : str(T2_1), '_dim':'temperature'}})
        doc['result'].update({'m_1':{'_val' : str(m_1), '_dim':'massflow'}})
        doc['result'].update({'MW_1':{'_val' : str(MW_1), '_dim':'molecularMass'}})
        doc['result'].update({'Qact_1':{'_val' : str(Qact_1), '_dim':'flow'}})
        doc['result'].update({'kavg_1':{'_val' : str(kavg_1)}})
        doc['result'].update({'Zavg_1':{'_val' : str(Zavg_1)}})
        doc['result'].update({'etaP_1':{'_val' : str(etaP_1)}})
        doc['result'].update({'Hp_1':{'_val' : str(Hp_1)}})
        doc['result'].update({'Pabs_1':{'_val' : str(Pabs_1), '_dim':'power'}})
        doc['result'].update({'d2':{'_val' : str(d2), '_dim':'length'}})
        doc['result'].update({'N':{'_val' : str(N)}})
        doc['result'].update({'Nimpeller_1':{'_val' : str(Nimpeller_1)}})

        doc['result'].update({'P1_2':{'_val' : str(P1_2), '_dim':'pressure'}})
        doc['result'].update({'T1_2':{'_val' : str(T1_2), '_dim':'temperature'}})
        doc['result'].update({'P2_2':{'_val' : str(P2_2), '_dim':'pressure'}})
        doc['result'].update({'T2_2':{'_val' : str(T2_2), '_dim':'temperature'}})
        doc['result'].update({'m_2':{'_val' : str(m_2), '_dim':'massflow'}})
        doc['result'].update({'MW_2':{'_val' : str(MW_2), '_dim':'molecularMass'}})
        doc['result'].update({'Qact_2':{'_val' : str(Qact_2), '_dim':'flow'}})
        doc['result'].update({'kavg_2':{'_val' : str(kavg_2)}})
        doc['result'].update({'Zavg_2':{'_val' : str(Zavg_2)}})
        doc['result'].update({'etaP_2':{'_val' : str(etaP_2)}})
        doc['result'].update({'Hp_2':{'_val' : str(Hp_2)}})
        doc['result'].update({'Pabs_2':{'_val' : str(Pabs_2), '_dim':'power'}})
        doc['result'].update({'d2':{'_val' : str(d2), '_dim':'length'}})
        doc['result'].update({'N':{'_val' : str(N)}})
        doc['result'].update({'Nimpeller_2':{'_val' : str(Nimpeller_2)}})


# determine polytropic head and power

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
