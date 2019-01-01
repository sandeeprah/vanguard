import math

def candela2lumens(candela, apex_angle):
    solid_angle = 2*math.pi*(1-math.cos(apex_angle/2))
    lumens = candela*solid_angle
    return lumens

def lumens2candela(lumens, apex_angle):
    solid_angle = 2*math.pi*(1-math.cos(apex_angle/2))
    candela = lumens/solid_angle
    return candela

def candela2lux(candela, distance):
    lux = candela/math.pow(distance,2)
    return lux

def lux2candela(lux, distance):
    candela = lux*math.pow(distance,2)
    return candela

def lumens2lux(lumens, radius=None, area=None):
    if radius is not None:
        area = 4*math.pi*math.pow(radius,2)
    lux = lumens/area
    return lux

def lux2lumens(lux, radius=None, area=None):
    if radius is not None:
        area = 4*math.pi*math.pow(radius,2)

    lumens = lux*area
    return lumens

def watts2lumens(watts, luminous_efficacy):
    lumens = watts*luminous_efficacy
    return lumens

def lumens2watts(lumens, luminous_efficacy):
    watts = lumens/luminous_efficacy
    return watts
