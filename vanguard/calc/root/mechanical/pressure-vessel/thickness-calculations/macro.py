from math import *
from copy import deepcopy
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import parseFloat, roundit
from techlib.mechanical.static import pressurevessel as pv

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    D = None
    tn = parseFloat(doc['input']['tn']['_val'])
    Z = parseFloat(doc['input']['Z']['_val'])
    Pi = parseFloat(doc['input']['Pi']['_val'])
    Ti = parseFloat(doc['input']['Ti']['_val'])
    Tt = parseFloat(doc['input']['Tt']['_val'])
    ca = parseFloat(doc['input']['ca']['_val'])
    MOC = doc['input']['MOC']['_val']

    D_basis = doc['input']['D_basis']['_val']
    if (D_basis=='inner'):
        D = parseFloat(doc['input']['D']['_val'])
        Do = D+2*tn
    elif(D_basis=='outer'):
        Do = parseFloat(doc['input']['Do']['_val'])
        D = Do - 2*tn
    else:
        doc[errors].append('Invalid value for "Shell Diameter given as"')


    doc['result'].update({'D':{'_val' : str(roundit(D)), '_dim':'length'}})
    doc['result'].update({'Do':{'_val' : str(roundit(Do)), '_dim':'length'}})

    # get inner radius and outer radius
    R = D/2
    Ro = Do/2

    # get inner radius in corroded condition
    Dcor = D + 2*ca
    Rcor = R + ca

    doc['result'].update({'Rcor':{'_val' : str(roundit(Rcor)), '_dim':'length'}})

    # set the available thickness after deducting corrosion
    tcor = tn - ca
    doc['result'].update({'tcor':{'_val' : str(roundit(tcor)), '_dim':'length'}})

    # determine the value of allowable stress
    if (MOC=='Other'):
        S = parseFloat(doc['input']['S']['_val'])
        St = parseFloat(doc['input']['St']['_val'])
    else:
        S = pv.getAllowableStress(MOC, Ti)
        St = pv.getAllowableStress(MOC, Tt)

    doc['result'].update({'S':{'_val' : str(roundit(S)), '_dim':'pressure'}})
    doc['result'].update({'St':{'_val' : str(roundit(St)), '_dim':'pressure'}})

    density = 7850

    # set the minimum required thickness as per UG-15
    tu = 1.5/1000
    doc['result'].update({'tu':{'_val' : str(roundit(tu)), '_dim':'length'}})

    # check whether the geometry is sphere or cylinder
    Shape = doc['input']['Shape']['_val']

    if (Shape=='cylindrical'):
        Ec = parseFloat(doc['input']['Ec']['_val'])
        El = parseFloat(doc['input']['El']['_val'])

        # Circumferential Stress Evaluation
        try:
            tc, condn_Pc, eqn_ref_tc = pv.thicknessCylinderCircumStress(S, El, Pi, Rcor)
        except Exception as e:
            tc = nan
            condn_Pc = ""
            eqn_ref_tc = ""
            error_message = "Failed to calculate thickness(circumferential stress) for cylindrical shell" + " " + str(e)
            doc['errors'].append(error_message)

        doc['result'].update({'tc':{'_val' : str(roundit(tc)), '_dim':'length'}})
        doc['result'].update({'condn_Pc':{'_val' : condn_Pc}})
        doc['result'].update({'eqn_ref_tc':{'_val' : eqn_ref_tc}})

        # Longitudinal Stress Evaluation
        try:
            tl, condn_Pl, eqn_ref_tl = pv.thicknessCylinderLongStress(S, Ec, Pi, Rcor)
        except Exception as e:
            tl = nan
            condn_Pl = ""
            eqn_ref_tl = ""
            error_message = "Failed to calculate thickness(longitudinal stress) for cylindrical shell" + " " + str(e)
            doc['errors'].append(error_message)

        doc['result'].update({'tl':{'_val' : str(roundit(tl)), '_dim':'length'}})
        doc['result'].update({'condn_Pl':{'_val' : condn_Pl}})
        doc['result'].update({'eqn_ref_tl':{'_val' : eqn_ref_tl}})

        # get the highest of the shell thickness determined as per circumferential analysis, longitudinal analysis and UG-15 requirement
        t = max([tu,tc,tl])

        try:
            MAWPc, condn_tc, eqn_ref_pc = pv.pressureCylinderCircumStress(S, El, tcor, Rcor)
        except Exception as e:
            MAWPc = nan
            condn_tc = ""
            eqn_ref_pc = ""
            error_message = "Failed to calculate MAWP(circumferential stress) for cylindrical shell" + " " + str(e)
            doc['errors'].append(error_message)

        doc['result'].update({'MAWPc':{'_val' : str(roundit(MAWPc)), '_dim':'pressure'}})
        doc['result'].update({'condn_tc'  :{'_val' : condn_tc}})
        doc['result'].update({'eqn_ref_pc':{'_val' : eqn_ref_pc}})


        try:
            MAWPl, condn_tl, eqn_ref_pl = pv.pressureCylinderLongStress(S, Ec, tcor, Rcor)
        except Exception as e:
            MAWPl = nan
            condn_tl = ""
            eqn_ref_pl = ""
            error_message = "Failed to calculate MAWP(longitudinal stress) for cylindrical shell" + " " + str(e)
            doc['errors'].append(error_message)

        doc['result'].update({'MAWPl':{'_val' : str(roundit(MAWPl)), '_dim':'pressure'}})
        doc['result'].update({'condn_tl'  :{'_val' : condn_tl}})
        doc['result'].update({'eqn_ref_pl':{'_val' : eqn_ref_pl}})

        # get the least of the MAWP from circumferential and longitudinal analysis to get governing MAWP
        MAWPsh = min([MAWPc,MAWPl])
        doc['result'].update({'MAWPsh':{'_val' : str(roundit(MAWPsh)), '_dim':'pressure'}})


        try:
            shell_volume, shell_matlVolume =  pv.cylindricalShellVolume(tn, Z, D=D)
        except Exception as e:
            shell_volume = nan
            shell_matlVolume = nan
            error_message = "Failed to calculate volume for cylindrical shell" + " " + str(e)
            doc['errors'].append(error_message)

        # carry out head evaluation
        Head1 = doc['input']['Head1']['_val']
        tn1 = parseFloat(doc['input']['tn1']['_val'])
        D1 = D
        Do1 = D1 + 2*tn1
        R1 = D1/2
        Dcor1 = D1 + 2*ca
        Rcor1 = Dcor1/2
        tcor1 = tn1 - ca
        doc['result'].update({'D1':{'_val' : str(roundit(D1)), '_dim':'length'}})
        doc['result'].update({'Do1':{'_val' : str(roundit(Do1)), '_dim':'length'}})
        doc['result'].update({'tcor1':{'_val' : str(roundit(tcor1)), '_dim':'length'}})

        t1 = nan
        tcone1 = nan
        tknuckle1 = nan
        MAWP1 = nan
        Pcone1 = nan
        Pknuckle1 = nan
        L1 = nan
        Kcor1 = nan
        Mcor1 = nan
        condn_P1 = ""
        condn_t1 = ""
        eqn_ref_t1 = ""
        eqn_ref_p1 = ""
        eqn_refconet1 = ""
        eqn_ref_knucklet1 = ""
        eqn_ref_coneP1 = ""
        eqn_ref_knuckleP1 = ""
        V1 = nan
        Vm1 = nan

        if (Head1=='ellipsoidal'):
            beta1 = parseFloat(doc['input']['beta1']['_val'])
            h1 = D1/(2*beta1)
            hcor1 = h1 + ca
            betacor1 = Dcor1/(2*hcor1)

            try:
                th1, Kcor1, eqn_ref_t1 =  pv.thicknessEllipsoidalHead(S, Ec, P=Pi, D=Dcor1, ar = betacor1)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for ellipsoidal head, Side 1." + " " + str(e))

            try:
                MAWP1, Kcor1, eqn_ref_p1 = pv.pressureEllipsoidalHead(S, Ec, t=tcor1, D=Dcor1, ar = betacor1)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for ellipsoidal head, Side 1." + " " + str(e))

            try:
                V1, Vm1 = pv.volumeEllipsoidalHead(tn1, beta1, D=D1)
            except Exception as e:
                doc['errors'].append("Failed to calculate ellipsoidal Head volume, Side 1." + " " + str(e))

            doc['result'].update({'Kcor1':{'_val' : str(roundit(Kcor1))}})

        elif (Head1=='torispherical'):
            L1 = parseFloat(doc['input']['L1']['_val'])
            r1 = parseFloat(doc['input']['r1']['_val'])

            Lcor1 = L1 + ca
            rcor1 = r1 + ca

            try:
                th1, Mcor1, eqn_ref_t1 = pv.thicknessTorisphericalHead(S, Ec, P=Pi, Do=Do1, L=Lcor1, r=rcor1)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for torispherical head, Side 1." + " " + str(e))

            try:
                MAWP1, Mcor1, eqn_ref_p1 = pv.pressureTorisphericalHead(S, Ec, t=tcor1, Do=Do1, L=Lcor1, r=rcor1)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for torispherical head, Side 1." + " " + str(e))

            try:
                V1, Vm1 = pv.volumeTorisphericalHead(tn1, L=L1, r=r1, D=D1)
            except Exception as e:
                doc['errors'].append("Failed to calculate torispherical Head volume, Side 1." + " " + str(e))

            doc['result'].update({'Mcor1':{'_val' : str(roundit(Mcor1))}})

        elif (Head1=='hemispherical'):

            try:
                th1, condn_P1, eqn_ref_t1 =  pv.thicknessSphere(S, Ec, P=Pi, R=Rcor1)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for  head, Side 1." + " " + str(e))

            try:
                MAWP1, condn_t1, eqn_ref_p1 = pv.pressureSphere(S, Ec, t=tcor1, R=Rcor1)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for hemispherical head, Side 1." + " " + str(e))

            try:
                V1, Vm1 = pv.volumeHemisphericalHead(tn1, D=D1)
            except Exception as e:
                doc['errors'].append("Failed to calculate volume for hemispherical Head, Side 1." + " " + str(e))

            doc['result'].update({'condn_P1':{'_val' : condn_P1}})
            doc['result'].update({'condn_t1':{'_val' : condn_t1}})

        elif (Head1=='conical'):
            alpha1 = parseFloat(doc['input']['alpha1']['_val'])

            try:
                th1, eqn_ref_t1 = pv.thicknessConicalHead(S, Ec, P=Pi, D=Dcor1, alpha=alpha1)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for conical Head, Side 1." + " " + str(e))

            try:
                MAWP1, eqn_ref_p1 = pv.pressureConicalHead(S, Ec, t=tcor1, D=D1, alpha=alpha1)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for conical Head, Side 1." + " " + str(e))

            try:
                V1, Vm1 = pv.volumeConicalHead(tn1, alpha1, D=D1)
            except Exception as e:
                doc['errors'].append("Failed to calculate volume for conical Head, Side 1." + " " + str(e))


        elif (Head1=='toriconical'):
            r1 = parseFloat(doc['input']['r1']['_val'])
            alpha1 = parseFloat(doc['input']['alpha1']['_val'])
            rcor1 = r1 + ca
            Dicor1 = Dcor1 - 2*rcor1*(2-cos(alpha1))

            try:
                th1, tcone1, eqn_ref_conet1, tknuckle1, Lcor1, Mcor1, eqn_ref_knucklet1 =  pv.thicknessToriConicalHead(S, Ec, P=Pi, Do=Do1, tn=tn1, Di=Dicor1, r=rcor1, alpha=alpha1)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for toriconical head, Side 1." + " " + str(e))

            try:
                MAWP1, Pcone1, eqn_ref_coneP1, Pknuckle1, Lcor1, Mcor1, eqn_ref_knuckleP1 = pv.pressureToriConicalHead(S, Ec, t=tcor1, Do=Do1, tn=tn1, Di=Dicor1, r=rcor1, alpha=alpha1)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for toriconical head, Side 1." + " " + str(e))

            eqn_ref_t1 = ""
            eqn_ref_p1 = ""

            try:
                V1, Vm1 = pv.volumeToriconicalHead(tn1, r1, alpha1, D=D1)
            except Exception as e:
                doc['errors'].append("Failed to calculate volume for toriconical Head, Side 1." + " " + str(e))

            doc['result'].update({'Dicor1':{'_val' : str(roundit(Dicor1)), '_dim':'length'}})
            doc['result'].update({'Lcor1':{'_val' : str(roundit(Lcor1)), '_dim':'length'}})
            doc['result'].update({'Mcor1':{'_val' : str(roundit(Mcor1))}})

            doc['result'].update({'tcone1':{'_val' : str(roundit(tcone1)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_conet1':{'_val' : eqn_ref_conet1}})
            doc['result'].update({'tknuckle1':{'_val' : str(roundit(tknuckle1)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_knucklet1':{'_val' : eqn_ref_knucklet1}})

            doc['result'].update({'Pcone1':{'_val' : str(roundit(Pcone1)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_coneP1':{'_val' : eqn_ref_coneP1}})
            doc['result'].update({'Pknuckle1':{'_val' : str(roundit(Pknuckle1)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_knuckleP1':{'_val' : eqn_ref_knuckleP1}})

        else:
            doc['errors'].append('Invalid input for Head - Side 1')

        t1 = max([th1,tu])
        tr1 = t1 + ca
        if (tn1>=tr1):
            tn1_adequate = "Yes"
        else:
            tn1_adequate = "No"

        head1_weight = density*Vm1

        doc['result'].update({'th1':{'_val' : str(roundit(th1)), '_dim':'length'}})
        doc['result'].update({'t1':{'_val' : str(roundit(t1)), '_dim':'length'}})
        doc['result'].update({'eqn_ref_t1':{'_val' : eqn_ref_t1}})
        doc['result'].update({'tr1':{'_val' : str(roundit(tr1)), '_dim':'length'}})
        doc['result'].update({'tn1_adequate':{'_val' : tn1_adequate}})
        doc['result'].update({'MAWP1':{'_val' : str(roundit(MAWP1)), '_dim':'pressure'}})
        doc['result'].update({'eqn_ref_p1':{'_val' : eqn_ref_p1}})
        doc['result'].update({'head1_weight':{'_val' : str(roundit(head1_weight)), '_dim':'mass'}})
        doc['result'].update({'V1':{'_val' : str(roundit(V1)), '_dim':'volume'}})


        Head2 = doc['input']['Head2']['_val']
        tn2 = parseFloat(doc['input']['tn2']['_val'])
        D2 = D
        Do2 = D2 + 2*tn2
        R2 = D2/2
        Dcor2 = D2 + 2*ca
        Rcor2 = Dcor2/2
        tcor2 = tn2 - ca
        doc['result'].update({'D2':{'_val' : str(roundit(D2)), '_dim':'length'}})
        doc['result'].update({'Do2':{'_val' : str(roundit(Do2)), '_dim':'length'}})
        doc['result'].update({'tcor2':{'_val' : str(roundit(tcor2)), '_dim':'length'}})

        t2 = nan
        tcone2 = nan
        tknuckle2 = nan
        MAWP2 = nan
        Pcone2 = nan
        Pknuckle2 = nan
        L2 = nan
        Kcor2 = nan
        Mcor2 = nan
        condn_P2 = ""
        condn_t2 = ""
        eqn_ref_t2 = ""
        eqn_ref_p2 = ""
        eqn_refconet2 = ""
        eqn_ref_knucklet2 = ""
        eqn_ref_coneP2 = ""
        eqn_ref_knuckleP2 = ""
        V2 = nan
        Vm2 = nan

        if (Head2=='ellipsoidal'):
            beta2 = parseFloat(doc['input']['beta2']['_val'])
            h2 = D2/(2*beta2)
            hcor2 = h2 + ca
            betacor2 = Dcor2/(2*hcor2)

            try:
                th2, Kcor2, eqn_ref_t2 =  pv.thicknessEllipsoidalHead(S, Ec, P=Pi, D=Dcor2, ar = betacor2)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for ellipsoidal head, Side 2." + " " + str(e))

            try:
                MAWP2, Kcor2, eqn_ref_p2 = pv.pressureEllipsoidalHead(S, Ec, t=tcor2, D=Dcor2, ar = betacor2)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for ellipsoidal head, Side 2." + " " + str(e))

            try:
                V2, Vm2 = pv.volumeEllipsoidalHead(tn2, beta2, D=D2)
            except Exception as e:
                doc['errors'].append("Failed to calculate ellipsoidal Head volume, Side 2." + " " + str(e))

            doc['result'].update({'Kcor2':{'_val' : str(roundit(Kcor2))}})

        elif (Head2=='torispherical'):
            L2 = parseFloat(doc['input']['L2']['_val'])
            r2 = parseFloat(doc['input']['r2']['_val'])
            Lcor2 = L2 + ca
            rcor2 = r2 + ca

            try:
                th2, Mcor2, eqn_ref_t2 = pv.thicknessTorisphericalHead(S, Ec, P=Pi, Do=Do2, L=Lcor2, r=rcor2)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for torispherical head, Side 2." + " " + str(e))

            try:
                MAWP2, Mcor2, eqn_ref_p2 = pv.pressureTorisphericalHead(S, Ec, t=tcor2, Do=Do2, L=Lcor2, r=rcor2)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for torispherical head, Side 2." + " " + str(e))

            try:
                V2, Vm2 = pv.volumeTorisphericalHead(tn2, L=L2, r=r2, D=D2)
            except Exception as e:
                doc['errors'].append("Failed to calculate torispherical Head volume, Side 2." + " " + str(e))

            doc['result'].update({'Mcor2':{'_val' : str(roundit(Mcor2))}})

        elif (Head2=='hemispherical'):
            try:
                th2, condn_P2, eqn_ref_t2 =  pv.thicknessSphere(S, Ec, P=Pi, R=Rcor2)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for  head, Side 2." + " " + str(e))

            try:
                MAWP2, condn_t2, eqn_ref_p2 = pv.pressureSphere(S, Ec, t=tcor2, R=Rcor2)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for hemispherical head, Side 2." + " " + str(e))

            try:
                V2, Vm2 = pv.volumeHemisphericalHead(tn2, D=D2)
            except Exception as e:
                doc['errors'].append("Failed to calculate volume for hemispherical Head, Side 2." + " " + str(e))

            doc['result'].update({'condn_P2':{'_val' : condn_P2}})
            doc['result'].update({'condn_t2':{'_val' : condn_t2}})

        elif (Head2=='conical'):
            alpha2 = parseFloat(doc['input']['alpha2']['_val'])

            try:
                th2, eqn_ref_t2 = pv.thicknessConicalHead(S, Ec, P=Pi, D=Dcor2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for conical Head, Side 2." + " " + str(e))

            try:
                MAWP2, eqn_ref_p2 = pv.pressureConicalHead(S, Ec, t=tcor2, D=Dcor2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for conical Head, Side 2." + " " + str(e))

            try:
                V2, Vm2 = pv.volumeConicalHead(tn2, alpha2, D=D2)
            except Exception as e:
                doc['errors'].append("Failed to calculate volume for conical Head, Side 2." + " " + str(e))


        elif (Head2=='toriconical'):
            r2 = parseFloat(doc['input']['r2']['_val'])
            alpha2 = parseFloat(doc['input']['alpha2']['_val'])
            rcor2 = r2 + ca
            Dicor2 = Dcor2 - 2*rcor2*(2-cos(alpha2))

            try:
                th2, tcone2, eqn_ref_conet2, tknuckle2, L2, Mcor2, eqn_ref_knucklet2 =  pv.thicknessToriConicalHead(S, Ec, P=Pi, Do=Do2, tn=tn2, Di=Dicor2, r=rcor2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append("Failed to calculate thickness for toriconical head, Side 2." + " " + str(e))

            try:
                MAWP2, Pcone2, eqn_ref_coneP2, Pknuckle2, Lcor2, Mcor2, eqn_ref_knuckleP2 = pv.pressureToriConicalHead(S, Ec, t=tcor2, Do=Do2, tn=tn2, Di=Dicor2, r=rcor2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append("Failed to calculate MAWP for toriconical head, Side 2." + " " + str(e))

            eqn_ref_t2 = ""
            eqn_ref_p2 = ""

            try:
                V2, Vm2 = pv.volumeToriconicalHead(tn2, r2, alpha2, D=D2)
            except Exception as e:
                doc['errors'].append("Failed to calculate volume for toriconical Head, Side 2." + " " + str(e))

            doc['result'].update({'Dicor2':{'_val' : str(roundit(Dicor2)), '_dim':'length'}})
            doc['result'].update({'Lcor2':{'_val' : str(roundit(Lcor2)), '_dim':'length'}})
            doc['result'].update({'Mcor2':{'_val' : str(roundit(Mcor2))}})

            doc['result'].update({'tcone2':{'_val' : str(roundit(tcone2)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_conet2':{'_val' : eqn_ref_conet2}})
            doc['result'].update({'tknuckle2':{'_val' : str(roundit(tknuckle2)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_knucklet2':{'_val' : eqn_ref_knucklet2}})

            doc['result'].update({'Pcone2':{'_val' : str(roundit(Pcone2)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_coneP2':{'_val' : eqn_ref_coneP2}})
            doc['result'].update({'Pknuckle2':{'_val' : str(roundit(Pknuckle2)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_knuckleP2':{'_val' : eqn_ref_knuckleP2}})

        else:
            doc['errors'].append('Invalid input for Head - Side 2')

        t2 = max([th2,tu])
        tr2 = t2 + ca
        if (tn2>=tr2):
            tn2_adequate = "Yes"
        else:
            tn2_adequate = "No"

        head2_weight = density*Vm2

        doc['result'].update({'th2':{'_val' : str(roundit(th2)), '_dim':'length'}})
        doc['result'].update({'t2':{'_val' : str(roundit(t2)), '_dim':'length'}})
        doc['result'].update({'eqn_ref_t2':{'_val' : eqn_ref_t2}})
        doc['result'].update({'tr2':{'_val' : str(roundit(tr2)), '_dim':'length'}})
        doc['result'].update({'tn2_adequate':{'_val' : tn2_adequate}})
        doc['result'].update({'MAWP2':{'_val' : str(roundit(MAWP2)), '_dim':'pressure'}})
        doc['result'].update({'eqn_ref_p2':{'_val' : eqn_ref_p2}})
        doc['result'].update({'head2_weight':{'_val' : str(roundit(head2_weight)), '_dim':'mass'}})
        doc['result'].update({'V2':{'_val' : str(roundit(V2)), '_dim':'volume'}})

        # get the least of the MAWP from circumferential and longitudinal analysis to get governing MAWP
        MAWP = min([MAWPc,MAWPl, MAWP1, MAWP2])

        shell_weight = density*shell_matlVolume
        vessel_volume = shell_volume + V1 + V2
        vslhd_weight = shell_weight + head1_weight + head2_weight

    elif (Shape=='spherical'):
        # Spherical Stress Evaluation
        E = parseFloat(doc['input']['E']['_val'])

        if (R is not None):
            ts, condn_Ps, eqn_ref_ts = pv.thicknessSphere(S, E, Pi, R)
            MAWPs, condn_ts, eqn_ref_ps = pv.pressureSphere(S, E, tcor, R)
        else:
            ts, condn_Ps, eqn_ref_ts = pv.thicknessSphere(S, E, Pi, Ro)
            MAWPs, condn_ts, eqn_ref_ps = pv.pressureSphere(S, E, tcor, Ro)

        # get the highest of the shell thickness determined as per circumferential analysis, longitudinal analysis and UG-15 requirement
        t = max([tu,ts])

        # get the least of the MAWP from circumferential and longitudinal analysis to get governing MAWP
        MAWPsh = MAWPs
        doc['result'].update({'MAWPsh':{'_val' : str(roundit(MAWPsh)), '_dim':'pressure'}})


        if (D is not None):
            shell_volume, shell_matlVolume =  pv.sphericalShellVolume(tn, D=D)
        else:
            shell_volume, shell_matlVolume =  pv.sphericalShellVolume(tn, Do=Do)

        shell_weight = density*shell_matlVolume
        vessel_volume = shell_volume
        vslhd_weight = shell_weight


        MAWP = MAWPsh
        doc['result'].update({'ts':{'_val' : str(roundit(ts)), '_dim':'length'}})
        doc['result'].update({'condn_Ps':{'_val' : condn_Ps}})
        doc['result'].update({'eqn_ref_ts':{'_val' : eqn_ref_ts}})
        doc['result'].update({'MAWPs':{'_val' : str(roundit(MAWPs)), '_dim':'pressure'}})
        doc['result'].update({'condn_ts'  :{'_val' : condn_ts}})
        doc['result'].update({'eqn_ref_ps':{'_val' : eqn_ref_ps}})

    else:
        doc['errors'].append('Invalid Shape')


    # add the corrosion allowance to get minimum thickness requirement
    tr = t + ca
    if (tn >= tr):
        tn_adequate = "Yes"
    else:
        tn_adequate = "No"

    Pt = pv.pressureHydroUG99(MAWP=MAWP, S=S,St=St)

    zeta = parseFloat(doc['input']['zeta']['_val'])

    vessel_weight = vslhd_weight*(1 + (zeta/100))
    vessel_weight_hydrotest = vessel_weight + 1000*vessel_volume


    doc['result'].update({'t' :{'_val' : str(roundit(t)),  '_dim':'length'}})
    doc['result'].update({'tr':{'_val' : str(roundit(tr)), '_dim':'length'}})
    doc['result'].update({'tn_adequate':{'_val' : tn_adequate}})

    doc['result'].update({'shell_weight':{'_val' : str(roundit(shell_weight)), '_dim':'mass'}})
    doc['result'].update({'shell_volume':{'_val' : str(roundit(shell_volume)), '_dim':'volume'}})

    doc['result'].update({'MAWP' :{'_val' : str(roundit(MAWP)),  '_dim':'pressure'}})
    doc['result'].update({'Pt' :{'_val' : str(roundit(Pt)),  '_dim':'pressure'}})
    doc['result'].update({'vslhd_weight':{'_val' : str(roundit(vslhd_weight)), '_dim':'mass'}})
    doc['result'].update({'vessel_weight':{'_val' : str(roundit(vessel_weight)), '_dim':'mass'}})
    doc['result'].update({'vessel_volume':{'_val' : str(roundit(vessel_volume)), '_dim':'volume'}})
    doc['result'].update({'vessel_weight_hydrotest':{'_val' : str(roundit(vessel_weight_hydrotest)), '_dim':'mass'}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
