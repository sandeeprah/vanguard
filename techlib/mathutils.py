import math
import numpy as np

def parseFloat(value):
    try:
        return float(value)
    except Exception:
        return math.nan

def roundit(value,  max_decim=6, allowed_error=0.001):
    try:
        value = float(value)
    except Exception:
        return value


    decims = 1
    rounded_value = round(value, max_decim)

    if (value == 0):
        rounded_value = 0
    else:
        for decims in range(1, max_decim+1):
            rounded_value = round(value, decims)
            abs_error = abs(value - rounded_value)
            rel_error = abs_error/abs(value)
            if rel_error < allowed_error:
                return rounded_value


    if (isinstance(value, str)):
        return str(rounded_value)
    else:
        return rounded_value

def linarray_interp(x,y,x_interp):
    index_lower, index_higher = getindex(x,x_interp)
    if (index_lower < 0):
        raise Exception('Interpolation failed as parameter beyond range')
    if (index_lower == None):
        raise Exception('Interpolation failed as parameter beyond range')

    x_lower = x[index_lower]
    x_higher = x[index_higher]
    y_lower = y[index_lower]
    y_higher = y[index_higher]
    y_interp = linear_interp(x_interp, x1=x_lower, y1=y_lower, x2=x_higher, y2=y_higher)
    return y_interp


def getindex(ascending_sorted_list, searchval):
    '''
    Given a list which is sorted in ascending order and a float value (searchval), this function returns the index position of the first item encountered in the list,
    which is just lower or equal to searchval and the index just next higher to it. In other words, the item at position index+1 would be the first item higher than searchval.

    arguments:
    ----------
    ascending_sorted_list : a list of float/integers in ascending order
    search_value : value to be searched in the list

    returns:
    -------
    integer index_lower in list where item is just lower or equal to searchval.
    integer index_higher in list where item is just higher to searchval.
    '''

    index = 0
    index_lower = None
    index_higher = None

    for item in ascending_sorted_list:
        val = float(item)
        if val > searchval:
            index_lower = index-1
            if (index_lower < 0 ):
                index_lower = None
            index_higher = index
            break
        index +=1


    #check for the case when the length of the list is more than one and the value searched is equal to the highest item in the list.
    n = len(ascending_sorted_list)
    if (n>1):
        val = ascending_sorted_list[n-1]
        if searchval == val:
            index_lower = n-2
            index_higher = n-1


    return index_lower, index_higher


def linear_interp(x, x1, y1, x2, y2):
    '''
    This function returns linear interpolated value (y) at a value (x) lying between two points (x1,y1) and (x2,y2).

    arguments:
    ---------
    x: float value at which interpolation is required
    x1: float value
    y1: value of function at x1
    x2: float value
    y2: value of function at x2

    returns:
    --------
    y : float value given by equation y = y1 + (y2-y1)*(x-x1)/(x2-x1)
    '''
    y = y1 + (y2-y1)*(x-x1)/(x2-x1)
    return y




# Libraries imported for fast mathematical computations.

# Main Function takes in the coefficient of the Cubic Polynomial
# as parameters and it returns the roots in form of numpy array.
# Polynomial Structure -> ax^3 + bx^2 + cx + d = 0

def cubic_solve(a, b, c, d):
    '''
    CUBIC ROOT SOLVER

    Date Created   :    24.05.2017
    Created by     :    Shril Kumar [(shril.iitdhn@gmail.com),(github.com/shril)] &
                        Devojoyti Halder [(devjyoti.itachi@gmail.com),(github.com/devojoyti)]

    Project        :    Classified
    Use Case       :    Instead of using standard numpy.roots() method for finding roots,
                        we have implemented our own algorithm which is ~10x faster than
                        in-built method.

    Algorithm Link :    www.1728.org/cubic2.htm

    This script (Cubic Equation Solver) is an indipendent program for computation of cubic equations. This script, however, has no
    relation with original project code or calculations. It is to be also made clear that no knowledge of it's original project
    is included or used to device this script. This script is complete freeware developed by above signed users, and may furthur be
    used or modified for commercial or non - commercial purpose.

    '''

    if (a == 0 and b == 0):                     # Case for handling Liner Equation
        return np.array([(-d * 1.0) / c])                 # Returning linear root as numpy array.

    elif (a == 0):                              # Case for handling Quadratic Equations

        D = c * c - 4.0 * b * d                       # Helper Temporary Variable
        if D >= 0:
            D = math.sqrt(D)
            x1 = (-c + D) / (2.0 * b)
            x2 = (-c - D) / (2.0 * b)
        else:
            D = math.sqrt(-D)
            x1 = (-c + D * 1j) / (2.0 * b)
            x2 = (-c - D * 1j) / (2.0 * b)

        return np.array([x1, x2])               # Returning Quadratic Roots as numpy array.

    f = findF(a, b, c)                          # Helper Temporary Variable
    g = findG(a, b, c, d)                       # Helper Temporary Variable
    h = findH(g, f)                             # Helper Temporary Variable

    if f == 0 and g == 0 and h == 0:            # All 3 Roots are Real and Equal
        if (d / a) >= 0:
            x = (d / (1.0 * a)) ** (1 / 3.0) * -1
        else:
            x = (-d / (1.0 * a)) ** (1 / 3.0)
        return np.array([x, x, x])              # Returning Equal Roots as numpy array.

    elif h <= 0:                                # All 3 roots are Real

        i = math.sqrt(((g ** 2.0) / 4.0) - h)   # Helper Temporary Variable
        j = i ** (1 / 3.0)                      # Helper Temporary Variable
        k = math.acos(-(g / (2 * i)))           # Helper Temporary Variable
        L = j * -1                              # Helper Temporary Variable
        M = math.cos(k / 3.0)                   # Helper Temporary Variable
        N = math.sqrt(3) * math.sin(k / 3.0)    # Helper Temporary Variable
        P = (b / (3.0 * a)) * -1                # Helper Temporary Variable

        x1 = 2 * j * math.cos(k / 3.0) - (b / (3.0 * a))
        x2 = L * (M + N) + P
        x3 = L * (M - N) + P

        return np.array([x1, x2, x3])           # Returning Real Roots as numpy array.

    elif h > 0:                                 # One Real Root and two Complex Roots
        R = -(g / 2.0) + math.sqrt(h)           # Helper Temporary Variable
        if R >= 0:
            S = R ** (1 / 3.0)                  # Helper Temporary Variable
        else:
            S = (-R) ** (1 / 3.0) * -1          # Helper Temporary Variable
        T = -(g / 2.0) - math.sqrt(h)
        if T >= 0:
            U = (T ** (1 / 3.0))                # Helper Temporary Variable
        else:
            U = ((-T) ** (1 / 3.0)) * -1        # Helper Temporary Variable

        x1 = (S + U) - (b / (3.0 * a))
        x2 = -(S + U) / 2 - (b / (3.0 * a)) + (S - U) * math.sqrt(3) * 0.5j
        x3 = -(S + U) / 2 - (b / (3.0 * a)) - (S - U) * math.sqrt(3) * 0.5j

        return np.array([x1, x2, x3])           # Returning One Real Root and two Complex Roots as numpy array.


# Helper function to return float value of f.
def findF(a, b, c):
    return ((3.0 * c / a) - ((b ** 2.0) / (a ** 2.0))) / 3.0


# Helper function to return float value of g.
def findG(a, b, c, d):
    return (((2.0 * (b ** 3.0)) / (a ** 3.0)) - ((9.0 * b * c) / (a **2.0)) + (27.0 * d / a)) /27.0


# Helper function to return float value of h.
def findH(g, f):
    return ((g ** 2.0) / 4.0 + (f ** 3.0) / 27.0)
