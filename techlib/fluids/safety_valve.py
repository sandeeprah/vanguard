from fluids.safety_valve import API526_A, API526_letters
from vanguard.units import treeUnitConvert, SI_UNITS, unitConvert

def Reynolds(Q, G, mu, A):
    # convert Q from m3/s to lpm
    _Q = unitConvert(Q, 'flow', 'm3/s', 'lpm')
    # convert Viscosity from Pa.s to cP
    _mu = unitConvert(mu, 'dynViscosity', 'Pa.s', 'cP')
    # convert Area from m2 to mm2
    _A = unitConvert(A, 'area', 'm2', 'mm2')
    R = _Q*(18800*G)/(_mu*pow(_A,0.5))
    return R


def Reynolds_SSU(Q, G, SSU, A):
    # convert Q from m3/s to lpm
    _Q = unitConvert(Q, 'flow', 'm3/s', 'lpm')
    # convert Viscosity from Pa.s to cP
    _mu = unitConvert(mu, 'dynViscosity', 'Pa.s', 'cP')
    # convert Area from m2 to mm2
    _A = unitConvert(A, 'area', 'm2', 'mm2')
    R = _Q*(18800*G)/(_mu*pow(_A,0.5))
    return R


def API520_A_l_cert(Q, G, P, Pb, Kd=0.65, Kw=1, Kc=1, Kv=1):
    # convert Q from m3/s to lpm
    _Q = unitConvert(Q, 'flow', 'm3/s', 'lpm')
    # convert P from SI Pa to kPa
    _P = unitConvert(P, 'pressure', 'Pa', 'kPa')
    # convert Pb from SI Pa to kPa
    _Pb = unitConvert(Pb, 'pressure', 'Pa', 'kPa')
    B = pow(G/(_P-_Pb), 0.5)
    _A = 11.78*_Q*B/(Kd*Kw*Kc*Kv)
    # convert P from SI Pa to kPa
    A = unitConvert(_A, 'area', 'mm2', 'm2')
    return A


def API526_letter(A):
    index = API526_A.index(A)
    letter = API526_letters[index]
    return letter
