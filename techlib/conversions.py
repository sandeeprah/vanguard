from collections import OrderedDict
import json
import os
from marshmallow import Schema, fields, pprint, pre_load, validate, validates, ValidationError
from collections import OrderedDict

def SSU2cSt(SSU):
    r'''
    Parameters
    ----------
    SSU : kinematic viscosity in SSU

    Returns
    -------
    cSt : kinematic viscosity in centiStokes (cSt)

    '''

#    cSt = 0.22*SSU - 180/SSU

    Nr = 10000*(SSU+17.06)
    Dr = 0.9341*pow(SSU,3) + 9.01*pow(SSU,2) - 83.62*SSU + 53340
    cSt = 0.2159*SSU - (Nr/Dr)
    return cSt


def cSt2SSU(cSt):
    r'''
    Parameters
    ----------
    cSt : kinematic viscosity in centiStokes (cSt)

    Returns
    -------
    SSU : kinematic viscosity in SSU

    '''

#    SSU = (cSt + pow(cSt**2+158.4, 0.5))/0.44

    Nr = 1.0 + 0.03264*cSt
    Dr = (3930.2 + 262.7*cSt - 23.97*pow(cSt,2) + 1.646*pow(cSt,3))*1e-5

    SSU = 4.6324*cSt + (Nr/Dr)

    return SSU



def cSt2cP(cSt, SG):
    r'''
    Parameters
    ----------
    cSt : kinematic viscosity in centiStokes (cSt)
    SG  : Specific Gravity

    Returns
    -------
    cP : dynamic viscosity in centiPoise(cP)
    '''
    cP = cSt*SG
    return cP

def cP2cSt(cP, SG):
    r'''
    Parameters
    ----------
    cP : dynamic viscosity in centiPoise(cP)
    SG  : Specific Gravity

    Returns
    -------
    cSt : kinematic viscosity in centiStokes (cSt)

    '''
    cSt = cP/SG
    return cSt


def dyn2kinVisc(dynVisc, density):
    return dynVisc/density

def kin2dynVisc(kinVisc, density):
    return kinVisc*density
