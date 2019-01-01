import math
import os
import fluids
import pandas as pd
from fluids.friction import friction_factor
from fluids.core import Reynolds, K_from_f, K_from_L_equiv, dP_from_K
from fluids.fittings import Hooper2K, entrance_sharp, exit_normal
from fluids.piping import nearest_pipe
from marshmallow import Schema, fields, pprint, pre_load, validate, validates,  validates_schema, ValidationError
from collections import OrderedDict

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def reducer_sizes():
    my_file = os.path.join(THIS_FOLDER, 'reducer.csv')
    reducerdf = pd.read_csv(my_file)
    reducerdf = reducerdf.set_index('size_inches')
    return reducerdf.index.tolist()

def reducer_dimensions(reducer_size):
    my_file = os.path.join(THIS_FOLDER, 'reducer.csv')
    reducerdf = pd.read_csv(my_file)
    reducerdf = reducerdf.set_index('size_inches')
    D1 = reducerdf.loc[reducer_size, 'D1']/1000
    D2 = reducerdf.loc[reducer_size, 'D2']/1000
    L = reducerdf.loc[reducer_size, 'L']/1000
    return D1, D2, L

def pdrop_NPSreducer(reducer_size, Q, rho, mu, roughness):
    Dinlet, Doutlet, L = reducer_dimensions(reducer_size)
    Aoutlet = 3.1416 * (Dinlet ** 2) / 4
    Voutlet = Q / Aoutlet
    Re = fluids.core.Reynolds(Voutlet, Doutlet, rho, mu)
    relative_roughness = roughness/Dinlet
    fd = fluids.friction.friction_factor(Re, relative_roughness)
    K = fluids.fittings.contraction_conical(Dinlet, Doutlet, fd=fd, l=L)
    deltaP = fluids.core.dP_from_K(K,rho, Vinlet)
    return deltaP

def pdrop_NPSexpander(reducer_size, Q, rho, mu, roughness):
    Doutlet, Dinlet, L = reducer_dimensions(reducer_size)
    Ainlet = 3.1416 * (Dinlet ** 2) / 4
    Vinlet = Q / Ainlet
    Re = fluids.core.Reynolds(Vinlet, Dinlet, rho, mu)
    relative_roughness = roughness/Dinlet
    fd = fluids.friction.friction_factor(Re, relative_roughness)
    Kf = fluids.fittings.diffuser_pipe_reducer(Dinlet, Doutlet, l=L, fd1=fd)
    Kl = fluids.fittings.diffuser_conical(Dinlet, Doutlet, l=L*0.6, fd=fd)
    K = Kf+Kl
    deltaP = fluids.core.dP_from_K(K,rho, Vinlet)
    return deltaP


def get_hooper_list():
    Hooper = []
    Hooper.append('Elbow, 90°, Standard (R/D = 1), Screwed')
    Hooper.append('Elbow, 90°, Standard (R/D = 1), Flanged/welded')
    Hooper.append('Elbow, 90°, Long-radius (R/D = 1.5), All types')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 1 weld (90° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 2 weld (45° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 3 weld (30° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 4 weld (22.5° angle)')
    Hooper.append('Elbow, 90°, Mitered (R/D = 1.5), 5 weld (18° angle)')
    Hooper.append('Elbow, 45°, Standard (R/D = 1), All types')
    Hooper.append('Elbow, 45°, Long-radius (R/D 1.5), All types')
    Hooper.append('Elbow, 45°, Mitered (R/D=1.5), 1 weld (45° angle)')
    Hooper.append('Elbow, 45°, Mitered (R/D=1.5), 2 weld (22.5° angle)')
    Hooper.append('Elbow, 45°, Standard (R/D = 1), Screwed')
    Hooper.append('Elbow, 180°, Standard (R/D = 1), Flanged/welded')
    Hooper.append('Elbow, 180°, Long-radius (R/D = 1.5), All types')
    Hooper.append('Elbow, Used as, Standard, Screwed')
    Hooper.append('Elbow, Elbow, Long-radius, Screwed')
    Hooper.append('Elbow, Elbow, Standard, Flanged/welded')
    Hooper.append('Elbow, Elbow, Stub-in type branch')
    Hooper.append('Tee, Run, Screwed')
    Hooper.append('Tee, Through, Flanged or welded')
    Hooper.append('Tee, Tee, Stub-in type branch')
    Hooper.append('Valve, Gate, Full line size, Beta = 1')
    Hooper.append('Valve, Ball, Reduced trim, Beta = 0.9')
    Hooper.append('Valve, Plug, Reduced trim, Beta = 0.8')
    Hooper.append('Valve, Globe, Standard')
    Hooper.append('Valve, Globe, Angle or Y-type')
    Hooper.append('Valve, Diaphragm, Dam type')
    Hooper.append('Valve, Butterfly,')
    Hooper.append('Valve, Check, Lift')
    Hooper.append('Valve, Check, Swing')
    Hooper.append('Valve, Check, Tilting-disc')
    return Hooper

def hooper_name(item_index):
    Hooper = get_hooper_list()
    return Hooper[item_index]


def get_darby_list():
    Darby = []
    Darby.append('Elbow, 90°, threaded, standard, (r/D = 1)')
    Darby.append('Elbow, 90°, threaded, long radius, (r/D = 1.5)')
    Darby.append('Elbow, 90°, flanged, welded, bends, (r/D = 1)')
    Darby.append('Elbow, 90°, (r/D = 2)')
    Darby.append('Elbow, 90°, (r/D = 4)')
    Darby.append('Elbow, 90°, (r/D = 6)')
    Darby.append('Elbow, 90°, mitered, 1 weld, (90°)')
    Darby.append('Elbow, 90°, 2 welds, (45°)')
    Darby.append('Elbow, 90°, 3 welds, (30°)')
    Darby.append('Elbow, 45°, threaded standard, (r/D = 1)')
    Darby.append('Elbow, 45°, long radius, (r/D = 1.5)')
    Darby.append('Elbow, 45°, mitered, 1 weld, (45°)')
    Darby.append('Elbow, 45°, mitered, 2 welds, (22.5°)')
    Darby.append('Elbow, 180°, threaded, close-return bend, (r/D = 1)')
    Darby.append('Elbow, 180°, flanged, (r/D = 1)')
    Darby.append('Elbow, 180°, all, (r/D = 1.5)')
    Darby.append('Tee, Through-branch, (as elbow), threaded, (r/D = 1)')
    Darby.append('Tee, Through-branch,(as elbow), (r/D = 1.5)')
    Darby.append('Tee, Through-branch, (as elbow), flanged, (r/D = 1)')
    Darby.append('Tee, Through-branch, (as elbow), stub-in branch')
    Darby.append('Tee, Run-through, threaded, (r/D = 1)')
    Darby.append('Tee, Run-through, flanged, (r/D = 1)')
    Darby.append('Tee, Run-through, stub-in branch')
    Darby.append('Valve, Angle valve, 45°, full line size, β = 1')
    Darby.append('Valve, Angle valve, 90°, full line size, β = 1')
    Darby.append('Valve, Globe valve, standard, β = 1')
    Darby.append('Valve, Plug valve, branch flow')
    Darby.append('Valve, Plug valve, straight through')
    Darby.append('Valve, Plug valve, three-way (flow through)')
    Darby.append('Valve, Gate valve, standard, β = 1')
    Darby.append('Valve, Ball valve, standard, β = 1')
    Darby.append('Valve, Diaphragm, dam type')
    Darby.append('Valve, Swing check')
    Darby.append('Valve, Lift check')
    return Darby


roughness_dict = OrderedDict()
roughness_dict.update({"Carbon Steel(non-corroded)" : 5e-5})
roughness_dict.update({"Carbon Steel(corroded)" : 5e-4})
roughness_dict.update({"Stainless Steel" : 5e-5})
roughness_dict.update({"Titanium and Cu-Ni" : 5e-5})
roughness_dict.update({"Glass Reinforced Pipe" : 2e-5})
roughness_dict.update({"Polyethylene (PVC)" : 5e-6})

def darby_name(item_index):
    Darby = get_darby_list()
    return Darby[item_index]

def roughness_material_list():
    matl_list = []
    for item in roughness_dict:
        matl_list.append(item)
    return matl_list

def get_roughness(matl_name):
    roughness = roughness_dict[matl_name]
    print(roughness)
    return roughness
