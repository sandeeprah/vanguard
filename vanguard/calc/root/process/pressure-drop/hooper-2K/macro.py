import math
import CoolProp.CoolProp as CP
from fluids.friction import friction_factor
from fluids.core import Reynolds, K_from_f, K_from_L_equiv, dP_from_K
from fluids.fittings import Hooper2K, entrance_sharp, exit_normal
from fluids.piping import nearest_pipe
import fluids
from techlib.pressuredrop.line import get_hooper_list, get_roughness
from techlib.units import treeUnitConvert, SI_UNITS
from techlib.mathutils import roundit
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    K_pipe = 0
    K_fittings = 0
    K_entry = 0
    K_exit = 0
    K_fixed = 0
    K_LbyD = 0
    K_total = 0
    LbyD_total = 0
    deltaP_fixed = 0
    deltaP_total = 0

    size_definition = doc['input']['pipe']['size_definition']['_val']
    if (size_definition =="NPS"):
        nps = float(doc['input']['pipe']['NPS']['_val'])
        schedule = doc['input']['pipe']['schedule']['_val']
        NPS, Di, Do, t = nearest_pipe(NPS=nps, schedule=schedule)
    else:
        Di = float(doc['input']['pipe']['Dia_inner']['_val'])
        NPS = math.nan
        Do = math.nan
        t = math.nan

    doc['result'].update({'Di' : {'_val': str(Di), '_dim': 'length_mili'} })
    doc['result'].update({'Do' : {'_val':str(Do), '_dim': 'length_mili'}})
    doc['result'].update({'t' : {'_val':str(t), '_dim': 'length_mili'}})

    area = math.pi*pow(Di/2, 2)
    Q = float(doc['input']['fluidData']['Q']['_val'])
    V = roundit(Q/area)
    doc['result'].update({'V' : {'_val':str(V), '_dim': 'speed'}})

    mu = float(doc['input']['fluidData']['mu']['_val'])
    rho = float(doc['input']['fluidData']['rho']['_val'])
    Re = roundit(Reynolds(V=V, D=Di, rho=rho, mu=mu))
    doc['result'].update({'Re' : {'_val':str(Re)}})

    Hdyn = roundit(rho*pow(V,2)/2)
    doc['result'].update({'Hdyn' : {'_val': str(Hdyn), '_dim': 'length'}})

    #K calculation for straigth pipe
    roughness_basis = doc['input']['pipe']['roughness_basis']['_val']
    if (roughness_basis =="Material"):
        material = doc['input']['pipe']['material']['_val']
        roughness = get_roughness(material)
    else:
        roughness = float(doc['input']['pipe']['roughness']['_val'])

    eD = roughness/Di

    doc['result'].update({'eD' : {'_val': str(eD)} })
    fd = roundit(friction_factor(Re=Re, eD=eD, Method="Moody"))
    doc['result'].update({'fd_Moody' : {'_val': str(fd) }})


    length = float(doc['input']['pipe']['length']['_val'])
    K_pipe = roundit(K_from_f(fd=fd, L=length, D=Di))
    doc['result'].update({'K_pipe' : {'_val': str(K_pipe) }})
    deltaP_pipe = roundit(dP_from_K(K_pipe, rho, V))
    doc['result'].update({'deltaP_pipe' : {'_val': str(deltaP_pipe), '_dim': 'pressure'}})


    #calculating pressure drop for entrance

    entry_type = doc['input']['entrance']['entry_type']['_val']
    print('entry type is')
    print(entry_type)
    if entry_type=='none':
        K_entry = 0
    elif entry_type=='Sharp':
        K_entry = fluids.fittings.entrance_sharp()
    elif entry_type=='Rounded':
        Rc = float(doc['input']['entrance']['Rc']['_val'])
        K_entry = fluids.fittings.entrance_rounded(Di, Rc)
    elif entry_type=='Angled':
        angle_radians = float(doc['input']['entrance']['angle']['_val'])
        angle = angle_radians*57.2958
        K_entry = fluids.fittings.entrance_angled(angle)
    elif entry_type=='Projecting':
        wall_thickness = float(doc['input']['entrance']['wall_thickness']['_val'])
        K_entry = fluids.fittings.entrance_distance(Di, wall_thickness)

    K_entry = roundit(K_entry)
    doc['result'].update({'K_entry' : {'_val': str(K_entry)}})
    deltaP_entry = roundit(dP_from_K(K_entry, rho, V))
    doc['result'].update({'deltaP_entry' : {'_val':str(deltaP_entry), '_dim': 'pressure'}})

    #calculating pressure drop for exit
    exit_type = doc['input']['exit']['exit_type']['_val']
    print('exit_type')
    print(exit_type)
    if (exit_type=='Normal'):
        K_exit = exit_normal()
    else:
        K_exit = 0

    K_exit = roundit(K_exit)
    doc['result'].update({'K_exit' : {'_val': str(K_exit) }})
    deltaP_exit = roundit(dP_from_K(K_exit, rho, V))
    doc['result'].update({'deltaP_exit' : {'_val': str(deltaP_exit), '_dim': 'pressure'}})


    #calculating pressure drop for fittings
    fittings_list = doc['input']['fittings']
    for fitting in fittings_list:
        name = get_hooper_list()[fitting['index']]
        Di_inch = Di*39.3701
        K_fitting = Hooper2K(Di_inch, Re, name=name)
        K_fittings += K_fitting*fitting['quantity']

    K_fittings = roundit(K_fittings)
    doc['result'].update({'K_fittings' : {'_val':str(K_fittings)}})
    deltaP_fittings = dP_from_K(K_fittings, rho, V)
    deltaP_fittings = roundit(deltaP_fittings)
    doc['result'].update({'deltaP_fittings' : {'_val':str(deltaP_fittings), '_dim': 'pressure'}})


    #calculating pressure drop for sharp contractions
    deltaP_contractions_sharp = 0
    contractions_sharp = doc['input']['contractions_sharp']['_list']
    for contraction in contractions_sharp:
        D1 = contraction['D1']
        D2 = contraction['D2']
        A2 = 3.1416 * (D2 ** 2) / 4
        V2 = Q / A2
        K_contraction = fluids.fittings.contraction_sharp(D1, D2)
        deltaP = dP_from_K(K_contraction, rho, V2)
        deltaP_contractions_sharp += deltaP

    deltaP_contractions_sharp = roundit(deltaP_contractions_sharp)
    doc['result'].update({'deltaP_contractions_sharp' : {'_val':str(deltaP_contractions_sharp), '_dim': 'pressure'}})

    #calculating pressure drop for rounded contractions
    deltaP_contractions_rounded = 0
    contractions_rounded = doc['input']['contractions_rounded']['_list']
    for contraction in contractions_rounded:
        D1 = contraction['D1']
        D2 = contraction['D2']
        Rc = contraction['Rc']
        A2 = 3.1416 * (D2 ** 2) / 4
        V2 = Q / A2
        K_contraction = fluids.fittings.contraction_round(D1, D2, Rc)
        deltaP = dP_from_K(K_contraction, rho, V2)
        deltaP_contractions_rounded += deltaP

    deltaP_contractions_rounded = roundit(deltaP_contractions_rounded)
    doc['result'].update({'deltaP_contractions_rounded' : {'_val': str(deltaP_contractions_rounded), '_dim': 'pressure'}})

    #calculating pressure drop for conical contractions
    deltaP_contractions_conical = 0
    contractions_conical = doc['input']['contractions_conical']['_list']
    for contraction in contractions_conical:
        D1 = contraction['D1']
        D2 = contraction['D2']
        L = contraction['L']
        A2 = 3.1416 * (D2 ** 2) / 4
        V2 = Q / A2
        K_contraction = fluids.fittings.contraction_conical(D1, D2, fd=fd, l=L)
        deltaP = dP_from_K(K_contraction, rho, V2)
        deltaP_contractions_conical += deltaP

    deltaP_contractions_conical = roundit(deltaP_contractions_conical)
    doc['result'].update({'deltaP_contractions_conical' : {'_val': str(deltaP_contractions_conical), '_dim': 'pressure'}})

    #calculating pressure drop for pipe reducers contractions
    deltaP_contractions_reducer = 0
    contractions_reducer = doc['input']['contractions_reducer']['_list']
    for contraction in contractions_reducer:
        reducer_size = contraction['reducer_size']
        D1, D2, L = reducer_dimensions(reducer_size)
        A2 = 3.1416 * (D2 ** 2) / 4
        V2 = Q / A2
        K_contraction = fluids.fittings.contraction_conical(D1, D2, fd=fd, l=L)
        deltaP = dP_from_K(K_contraction, rho, V2)
        deltaP_contractions_reducer += deltaP

    deltaP_contractions_reducer = roundit(deltaP_contractions_reducer)
    doc['result'].update({'deltaP_contractions_reducer' : {'_val':str(deltaP_contractions_reducer), '_dim': 'pressure'}})

    # calculating total pressure drop in all contractions
    deltaP_contractions = deltaP_contractions_sharp + deltaP_contractions_rounded + deltaP_contractions_conical+ deltaP_contractions_reducer
    deltaP_contractions = roundit(deltaP_contractions)
    doc['result'].update({'deltaP_contractions' : {'_val': str(deltaP_contractions), '_dim': 'pressure'}})

    #calculating pressure drop for sharp expansions
    deltaP_expansions_sharp = 0
    expansions_sharp = doc['input']['expansions_sharp']['_list']
    for contraction in expansions_sharp:
        D1 = contraction['D1']
        D2 = contraction['D2']
        A1 = 3.1416 * (D1 ** 2) / 4
        V1 = Q / A1
        K_contraction = fluids.fittings.diffuser_sharp(D1, D2)
        deltaP = dP_from_K(K_contraction, rho, V1)
        deltaP_expansions_sharp += deltaP

    deltaP_expansions_sharp = roundit(deltaP_expansions_sharp)
    doc['result'].update({'deltaP_expansions_sharp' : {'_val':str(deltaP_expansions_sharp), '_dim': 'pressure'}})

    #calculating pressure drop for conical expansions
    deltaP_expansions_conical = 0
    expansions_conical = doc['input']['expansions_conical']['_list']
    for contraction in expansions_conical:
        D1 = contraction['D1']
        D2 = contraction['D2']
        L = contraction['L']
        A1 = 3.1416 * (D1 ** 2) / 4
        V1 = Q / A1
        K_contraction = fluids.fittings.diffuser_conical(D1, D2, fd=fd, l=L)
        deltaP = dP_from_K(K_contraction, rho, V1)
        deltaP_expansions_conical += deltaP

    deltaP_expansions_conical = roundit(deltaP_expansions_conical)
    doc['result'].update({'deltaP_expansions_conical' : {'_val':str(deltaP_expansions_conical), '_dim': 'pressure'}})

    #calculating pressure drop for pipe reducer expansions
    deltaP_expansions_reducer = 0
    expansions_reducer = doc['input']['expansions_reducer']['_list']
    for contraction in expansions_reducer:
        reducer_size = contraction['reducer_size']
        D2, D1, L = reducer_dimensions(reducer_size)
        A1 = 3.1416 * (D1 ** 2) / 4
        V1 = Q / A1
        K_contraction = fluids.fittings.diffuser_conical(D1, D2, fd=fd, l=L)
        deltaP = dP_from_K(K_contraction, rho, V1)
        deltaP_expansions_reducer += deltaP

    deltaP_expansions_reducer = roundit(deltaP_expansions_reducer)
    doc['result'].update({'deltaP_expansions_reducer' : {'_val':str(deltaP_expansions_reducer), '_dim': 'pressure'}})

    # calculating total pressure drop in all expansions
    deltaP_expansions = deltaP_expansions_sharp + deltaP_expansions_conical+ deltaP_expansions_reducer
    doc['result'].update({'deltaP_expansions' : {'_val':deltaP_expansions, '_dim': 'pressure'}})


    fixed_K_loss = doc['input']['fixed_K_losses']['_list']
    for loss in fixed_K_loss:
        K_fixed += loss['K']*loss['quantity']
    deltaP_fixed_K = dP_from_K(K_fixed, rho, V)

    fixed_LbyD_loss = doc['input']['fixed_LbyD_losses']['_list']
    for loss in fixed_LbyD_loss:
        L_D = loss['LbyD']
        K_LbyD += K_from_L_equiv(L_D = L_D, fd=fd)*loss['quantity']
    deltaP_fixed_LbyD = dP_from_K(K_LbyD, rho, V)

    fixed_deltaP_loss = doc['input']['fixed_deltaP_losses']['_list']
    for loss in fixed_deltaP_loss:
        deltaP_fixed += loss['deltaP']*loss['quantity']
    deltaP_fixed_deltaP = deltaP_fixed

    deltaP_fixed_all = deltaP_fixed_K + deltaP_fixed_LbyD + deltaP_fixed_deltaP

    deltaP_fixed_all = roundit(deltaP_fixed_all)
    doc['result'].update({'deltaP_fixed_all' : {'_val':str(deltaP_fixed_all), '_dim': 'pressure'}})

    deltaP_total = deltaP_pipe + deltaP_entry + deltaP_exit + deltaP_fittings + deltaP_contractions + deltaP_expansions+deltaP_fixed_all
    deltaP_total = roundit(deltaP_total)
    doc['result'].update({'deltaP_total' : {'_val':str(deltaP_total), '_dim': 'pressure'}})

#    doc_original['input'].update(doc['input'])
    doc_original['result'].update(doc['result'])
    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    return True
