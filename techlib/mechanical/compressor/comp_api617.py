from scipy.interpolate import interp1d
from math import *
from techlib.thermochem.thermochem_utils import mixture_props


def Qactual (MW, P, T, Z, m_rate):
    R = 8.314
    Rg = R/float(MW)
    v = Z*Rg*T/P
    #v = Z*Rg*T
    _Qactual = m_rate*v

    return round(_Qactual,2)


def nexp(k, polyeff):
    exp = ((k-1)/k)/polyeff
    _n = 1/(1-exp)
    return round(_n,4)


def Tdischarge(T1, P1, P2 , n = None, etap=None, mixture=None):
    rp = P2/P1
    if ((mixture is None or etap is None) and n is None):
        raise Exception('Insufficient Inputs. Td can not be calculated')
    if ((mixture is not None) and (etap is not None)):
        props1 = mixture_props(mixture, P=P1, T=T1)
        k1 = props1['k']
        T2_old = T1
        iteration = 0
        while True:
            iteration +=1
            props2 = mixture_props(mixture, P=P2, T=T2_old)
            k2 = props2['k']
            kavg = (k1 + k2)/2
            n = nexp(kavg, etap)
            T2 = T1*(rp**((n-1)/n))
            if (abs(T2 - T2_old) < 0.25):
                break
            else:
                T2_old = T2

            if (iteration > 20):
                break


    if (n is not None):
        f = rp**((n-1)/n)
        T2 = T1*f

    return T2




def polyeff(Q):

    xy = [(856.203,66.3929),
            (895.545,67.1591),
            (965.459,67.9254),
            (1209.84,70.0115),
            (1610.74,71.9703),
            (2312.88,73.9720),
            (2900.05,75.0369),
            (3863.34,75.9744),
            (4918.80,76.7414),
            (6857.46,77.5089),
            (8601.57,77.9355),
            (19160.5,79.0456),
            (28815.7,79.5156),
            (39579.8,79.8575),
            (48906.0,80.1138),
            (78138.7,80.5415),
            (163894,81.0981)]

    x, y = zip(*xy)
    func = interp1d(x, y)
    #x1 = linspace(900,160000,500)
    #y1 = func(x1)
    #plt.semilogx(x, y, basex=10, color='darkred', linewidth = 0.5)
    #plt.plot(x,y,color='darkred', linewidth = 0.5)
    #plt.xlim(100,1000000)
    #plt.savefig('effcurve')
    Qcheck = Q*3600

    if (Qcheck < 857):
        Qcheck = 857

    if (Qcheck > 163894):
        Qcheck = 163894

    _polyeff = float(func(Qcheck)/100)
    return _polyeff


def flowcoeff(Q,d2,u2):
    Qsi = Q/float(3600)
    d2si = d2/float(1000)
    _flowcoeff = Qsi/((pi/4)*(d2si**2)*u2)
    return round(_flowcoeff,3)

def hpolypsi(Psi, u2):
    _hpoly = Psi*(u2**2/2)/1000
    return _hpoly


'''
def headcoeff(Q,d2,u2):
    Qsi = Q/float(3600)
    d2si = d2/float(1000)
    _flowcoeff = Qsi/((pi/4)*(d2si**2)*u2)
    return round(_flowcoeff,3)
'''

def headcoeff(phi):
    xy = [(0.0119687,0.871177),
        (0.0129673,0.881990),
        (0.0138457,0.889692),
        (0.0148375,0.897384),
        (0.0160755,0.908197),
        (0.0174798,0.917425),
        (0.0190075,0.929803),
        (0.0200751,0.937534),
        (0.0221494,0.949873),
        (0.0239098,0.959121),
        (0.0255307,0.969972),
        (0.0279641,0.980756),
        (0.0300771,0.990014),
        (0.0337937,1.00231),
        (0.0367442,1.00838),
        (0.0388061,1.01297),
        (0.0400977,1.01445),
        (0.0434393,1.01897),
        (0.0474039,1.02504),
        (0.0500607,1.02489),
        (0.0558319,1.02776),
        (0.0600465,1.03229),
        (0.0655181,1.02891),
        (0.0702021,1.02716),
        (0.0774408,1.02532),
        (0.0854203,1.01877),
        (0.0945567,1.00590),
        (0.101310,0.999420),
        (0.112141,0.983405),
        (0.121449,0.965873),
        (0.134905,0.940400),
        (0.144527,0.927621),
        (0.151498,0.916474)]

    x, y = zip(*xy)
    func = interp1d(x, y)
    _headcoeff = float(func(phi))
    return _headcoeff

def etacoeff(phi):
    xy = [(0.0101001,0.636972),
        (0.0108244,0.646166),
        (0.0119872,0.658389),
        (0.0134706,0.675283),
        (0.0145949,0.684437),
        (0.0158135,0.695165),
        (0.0174492,0.708976),
        (0.0193952,0.724335),
        (0.0208624,0.735091),
        (0.0232714,0.745712),
        (0.0257721,0.759510),
        (0.0279232,0.768664),
        (0.0301440,0.777831),
        (0.0333790,0.785330),
        (0.0373689,0.795938),
        (0.0404879,0.805092),
        (0.0448331,0.812591),
        (0.0487474,0.817007),
        (0.0522383,0.821477),
        (0.0565948,0.827482),
        (0.0606420,0.827228),
        (0.0671460,0.831577),
        (0.0743407,0.831203),
        (0.0799521,0.834084),
        (0.0872411,0.833763),
        (0.0976482,0.833349),
        (0.105388,0.829918),
        (0.115408,0.826434),
        (0.128686,0.818160),
        (0.138378,0.813168),
        (0.152058,0.800223)]

    x, y = zip(*xy)
    func = interp1d(x, y)
    _etacoeff = float(func(phi))
    return _etacoeff


def workcoeff(phi):
    xy = [(0.0100319,0.662194),
        (0.0111057,0.657095),
        (0.0119864,0.655240),
        (0.0145320,0.649806),
        (0.0163233,0.644654),
        (0.0180712,0.641130),
        (0.0200798,0.639168),
        (0.0226370,0.634002),
        (0.0261793,0.631892),
        (0.0302759,0.629783),
        (0.0348876,0.629261),
        (0.0403468,0.627151),
        (0.0461557,0.626656),
        (0.0501793,0.624774),
        (0.0547523,0.622878),
        (0.0601761,0.619381),
        (0.0654240,0.619073),
        (0.0703536,0.615656),
        (0.0762090,0.613787),
        (0.0807657,0.608849),
        (0.0859146,0.608622),
        (0.0907212,0.603697),
        (0.100795,0.597010),
        (0.113216,0.590283),
        (0.122620,0.580541),
        (0.136237,0.573854),
        (0.151897,0.560855)]

    x, y = zip(*xy)
    func = interp1d(x, y)
    _workcoeff = float(func(phi))
    return _workcoeff


def centframe(Q, phi = 0.14, u2 = 240):
    '''
    d2option = [264,
                303,
                348,
                401,
                461,
                530,
                610,
                701,
                806,
                927,
                1066,
                1226,
                1410,
                1622,
                1865]
    '''
    d2option = [406,
                584,
                762,
                914,
                1120,
                1370]


    d2sel = d2option[0]
    for d2 in d2option:
        d2si = d2/1000
        Qsi = Q/3600
        Qmax = (pi/4)*(d2si**2)*u2*phi
        if Qmax >= Qsi:
            d2sel = d2
            Qnominal = Qmax
            break

    d2selsi=d2sel/1000
    N = (u2*60)/(pi*d2selsi)
    #Hnom = hpolypsi(Psi, u2)
    #phicorr = Qsi/((pi/4)*(d2selsi**2)*u2)

    return d2selsi, N


def HpmaxWheel(theta, sour='No'):
    xy = [(1.0,36),
        (1.1,36),
        (1.2,36),
        (1.3,36),
        (1.36635,33.8981),
        (1.41211,31.9441),
        (1.45552,29.8992),
        (1.50823,27.9417),
        (1.56095,25.9843),
        (1.61143,24.3038),
        (1.66655,22.6211),
        (1.70793,21.4971),
        (1.76539,19.9052),
        (1.80451,18.9662),
        (1.85516,17.8376),
        (1.90819,16.8917),
        (1.96354,15.9448),
        (2.00274,15.2817),
        (2.06510,14.5152),
        (2.10894,13.8499),
        (2.17362,13.0823),
        (2.20599,12.7905),
        (2.26834,12.0240),
        (2.36310,11.0577),
        (2.45330,10.3696),
        (2.50,10)]

    x, y = zip(*xy)
    func = interp1d(x, y)
    if (theta < 1):
        theta = 1
    _HpmaxWheel = float(func(theta))*1000

    if (sour == 'Yes') and (_HpmaxWheel > 27000):
        _HpmaxWheel = 27000

    return _HpmaxWheel


def theta(MW, k1, Z1, T1):
    _theta = (14500*MW/(k1*Z1*T1))**0.5
#    _theta = (14.5*MW/(k1*Z1*T1))**0.5
    return _theta



def Hpolytropic(Zavg, MW, T1, kavg, P1, P2, polyeff):
    n = nexp(kavg, polyeff)
    rp = P2/P1
    a = (n-1)/n

    R = 8.314
    Rg = R/MW
    Hp = Zavg*Rg*T1*(pow(rp, a) - 1)/a
    return Hp


def absPower(MassFlow, Hpolytropic, polyeff):
    P = MassFlow*Hpolytropic/polyeff
    return P
