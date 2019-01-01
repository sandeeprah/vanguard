from math import *

def motor_starting_time(Nr,Jm,Jl,Cs,Cmax,Cl,load_type):
    if load_type =="lift":
        Kl = 1
    elif load_type =="fan":
        Kl = 0.33
    elif load_type =="piston_pump":
        Kl = 0.5
    elif load_type == "flywheel":
        Kl = 0
    else :
        raise Exception("Invalid Load Type")


    Cacc = 0.45*(Cs+Cmax)-Kl*Cl
    print(Cacc)
    Ta = 2*pi*Nr*(Jm+Jl)/(60*Cacc)

    return Ta

'''
Nr = 3000
Cs = 1500
Cmax = 1600
Jm = 1.4
Jl = 30
load_type = "fan"
Cl = 600


Ta = motor_starting_time(Nr,Jm,Jl,Cs,Cmax,Cl,load_type)
print(Ta)
'''
