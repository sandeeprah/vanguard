
def receiverVolumeHoldUp(t,Qout,Pu, Pl, Tmax, margin):
    Pstd = 101325
    Tstd = 273.15 + 15
    Pband = Pu - Pl
    SF = 1 + (margin/100)
    vol = (SF*Qout*t*Pstd*Tmax)/(Pband*Tstd)
    return vol

def receiverVolumeSwitching(fs,Qin,Qout,Pu,Pl,Tmax,margin):
    Pstd = 101325
    Tstd = 273.15 + 15
    Pband = Pu - Pl
    SF = 1 + (margin/100)
    # load factor is obtained as
    x = Qout/Qin
    # Factor A is obtained as
    A = x*(1-x)
    # Time period of load/unload cycle
    Tcycle = (3600/fs)

    vol =  (SF*A*Qin*Tcycle*Pstd*Tmax)/(Pband*Tstd)

    return vol
