def humidityRatio(P, T, RH):
    # Antoine Constants
    A = 8.07131
    B = 1730.63
    C = 233.426

    T_C = T - 273.15 # convert temperature to degC for antoine equation

    f = A - B/(C+T_C)

    Pw_sat_mmHg = pow(10,f) # gets saturation pressure in mmHg
    Pw_sat = 133.32*Pw_sat_mmHg # gets saturation pressure in Pa
    Pw = Pw_sat*RH/100 # get partial pressure of water vapor in Pa
    X = 0.62198*Pw/(P-Pw) # get humidity ratio

    return X


def moistAirDensity(P, T, RH):
    rho_ma  = None # moist air density
    # Antoine Constants
    A = 8.07131
    B = 1730.63
    C = 233.426

    T_C = T - 273.15 # convert temperature to degC for antoine equation

    f = A - B/(C+T_C)

    Pw_sat_mmHg = pow(10,f) # gets saturation pressure in mmHg
    Pw_sat = 133.32*Pw_sat_mmHg # gets saturation pressure in Pa
    Pw = Pw_sat*RH/100 # get partial pressure of water vapor in Pa
    X = 0.62198*Pw/(P-Pw) # get humidity ratio

    MWda = 0.02897
    R = 8.314
    Rda = R/MWda

    MWw = 0.018
    Rw = R/MWw
    print("Pw_sat is {}".format(Pw_sat))
    print("X is {}".format(X))
    print("f is {}".format(f))

    rho_da = P/(Rda*T)
    rho_ma = rho_da*(1+X)/(1+X*(Rw/Rda))
    return rho_ma
