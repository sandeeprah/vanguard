import math
from techlib.mathutils import roundit

def getSPL(PWL, distance, Q):
    '''
    Calculates Sound Pressure Level for a point source of sound.

    Args:
        PWL : Sound Power Level in dB
        Q : Directivity Factor for transmission.
            Q = 1 : Spherical Transmission. Sound uniformly distributes in open space in all directions.
            Q = 2 : Hemispherical Transmission. When the source of sound is located on a reflective plane e.g. on surface of ground.
            Q = 4 : Quarter Spherical Transmission. When the source of sound is located on the intersection of two orthogonal reflective planes(e.g.
                    At the edge of two walls)
            Q = 8 : Semi-Quarter Spherical Transmission. When the source of sound is located on the intersection of three orthogonal reflecive planes (e.g. in a corner)
        distance : Distance in m

    Returns:
        SPL : Sound Pressure Level in dB
    '''
    Area = 4*math.pi*math.pow(distance,2)/Q
    try:
        SPL = PWL - 10*math.log10(Area)
        SPL = round(SPL,1)
    except Exception:
        SPL = math.nan

    return SPL


def getPWL(SPL, distance, Q):
    '''
    Calculates Sound Power Level for a point source.

    Args:
        SPL : Sound Pressure Level in dB
        Q : Directivity Factor for transmission.
            Q = 1 : Spherical Transmission. Sound uniformly distributes in open space in all directions.
            Q = 2 : Hemispherical Transmission. When the source of sound is located on a reflective plane e.g. on surface of ground.
            Q = 4 : Quarter Spherical Transmission. When the source of sound is located on the intersection of two orthogonal reflective planes(e.g.
                    At the edge of two walls)
            Q = 8 : Semi-Quarter Spherical Transmission. When the source of sound is located on the intersection of three orthogonal reflecive planes (e.g. in a corner)
        distance : Distance in m

    Returns:
        PWL : Sound Power Level in dB
    '''
    Area = 4*math.pi*math.pow(distance,2)/Q
    PWL = SPL + 10*math.log10(Area)
    PWL = round(PWL,1)
    return PWL


def getDistance(PWL, SPL, Q):
    '''
    Calculates Distance between a point source of sound and listener.

    Args:
        PWL : Sound Power Level in dB
        Q : Directivity Factor for transmission.
            Q = 1 : Spherical Transmission. Sound uniformly distributes in open space in all directions.
            Q = 2 : Hemispherical Transmission. When the source of sound is located on a reflective plane e.g. on surface of ground.
            Q = 4 : Quarter Spherical Transmission. When the source of sound is located on the intersection of two orthogonal reflective planes(e.g.
                    At the edge of two walls)
            Q = 8 : Semi-Quarter Spherical Transmission. When the source of sound is located on the intersection of three orthogonal reflecive planes (e.g. in a corner)
        SPL : Sound Pressure Level in dB
    Returns:
        distance : Distance in m
    '''
    term = (PWL-SPL)/10
    Area = pow(10, term)*Q
    distance = math.sqrt(Area/(4*math.pi))
    distance = round(distance,2)
    return distance

def response_getDistance(data):
    PWL = data.get('PWL')
    SPL = data.get('SPL')
    Q = data.get('Q')
    response_data = {}
    distance = getDistance(PWL=PWL, SPL=SPL,Q=Q)
    response_data['distance'] = distance
#    response_data['message'] = ['OK']
    return response_data


def addNoise(noiseLevelList):
    '''
    Gives the sum total noise of all noise provided as a list. The function carries out logarithmic addition.

    Args:
        noise_list : List of noise levels in dB
    Returns:
        total noise levels in dB
    '''

    sum_noise_intensity = 0
    noise_intensity = 0
    if (len(noiseLevelList)>0):
        for n in noiseLevelList:
            noise_intensity = math.pow(10, n/10)
            sum_noise_intensity= sum_noise_intensity+ noise_intensity

        noise_sum = 10*math.log10(sum_noise_intensity)
        noise_sum = round(noise_sum,2)
    else:
        noise_sum = 0
    return noise_sum


def correctBackNoise(noiseTotal, noiseBackground):
    '''Performs correction due to background noise
    args:
        noise_total : noise level as measured along with background noise in dB
        background_noise : noise level of background noise in dB
    returns:
        noise level attributable to the source in dB.

    '''
    try:
        noise_intensity_total = math.pow(10, noiseTotal/10)
        noise_intensity_background = math.pow(10, noiseBackground/10)
        noise_intensity_source = noise_intensity_total - noise_intensity_background

        noiseSource = 10*math.log10(noise_intensity_source)
        noiseSource = round(noiseSource,2)
    except Exception:
        noiseSource = math.nan


    return noiseSource


def correctSpectrum(totalSpectrum, backgroundSpectrum):
    '''Performs correction due to background noise
    args:
        noise_total_spectrum : dictionary of total noise levels(along with background noise) in dB at following mean band frequencies in Hz as key:
        f63, f125, f250, f500, f1000, f2000, f4000, f8000
        background_noise_spectrum : dictionary of background noise level in dB at following mean band frequencies in Hz as key:
        f63, f125, f250, f500, f1000, f2000, f4000, f8000
    returns:
        noise level attributable to the source in dB as a dictionary with frequency as key.

    '''
    correctedSpectrum = {}
    bands = ["f63", "f125", "f250", "f500", "f1000", "f2000", "f4000", "f8000"]
    for frequency in bands:
        correctedSpectrum[frequency] = correctBackNoise(totalSpectrum[frequency], backgroundSpectrum[frequency])
    return correctedSpectrum

'''
def response_correctSpectrum(data):
    totalSpectrum = data.get('totalSpectrum')
    backgroundSpectrum = data.get('backgroundSpectrum')
    correctedSpectrum = correctSpectrum(totalSpectrum=totalSpectrum, backgroundSpectrum=backgroundSpectrum)
    response_data = {}
    response_data['correctedSpectrum']=correctedSpectrum
    return response_data
'''

def aWeightedSpectrum(spectrum):
    '''Applies A filter to the noise spectrum and returns the filtered spectrum.
    Args:
        spectrum: dictionary of noise levels in dB at following mean band frequencies in Hz as key:
        f63, f125, f250, f500, f1000, f2000, f4000, f8000
    Returns:
        filtered spectrum as a dictionary of noise levels similar to spectrum above.

    '''
    bands = ["f63", "f125", "f250", "f500", "f1000", "f2000", "f4000", "f8000"]
    spectrum_filtered = {}

    A_filter = {"f63":-26.2,
                "f125":-16.1,
                "f250":-8.6,
                "f500":-3.2,
                "f1000":0,
                "f2000":1.2,
                "f4000":1,
                "f8000":-1.1
                    }

    for frequency in bands:
        spectrum_filtered[frequency] = roundit(spectrum[frequency] + A_filter[frequency])

    return spectrum_filtered


spt =  {"f63":96,
        "f125":89,
        "f250":82,
        "f500":79,
        "f1000":77,
        "f2000":76,
        "f4000":76,
        "f8000":75
        }

def spectrumTotal(spectrum):
    ''' Get the overall noise level of a spectrum.
    Args:
        spectrum: dictionary of noise levels in dB at following mean band frequencies in Hz as key:
        f63, f125, f250, f500, f1000, f2000, f4000, f8000
    Returns:
        overall summation of noise levels in spectrum in dB.
    '''
    noise_list = []
    for band in spectrum:
        band_level = spectrum[band]
        noise_list.append(band_level)

    total_noise = addNoise(noise_list)
    return total_noise


def distAttenPoint(SPL1, R1, R2):
    '''
    Attenuation due to distance from a point source of sound. (Follows the 6db reduction rule per doubling of distance)
    Args:
        SPL1 : Sound Pressure Level at distance R1
        R1 : Distance at which reference noise level SPL1 is measured
        R2 : Distance at which noise level is to be determined
    Returns:
        Sound Pressure Level and distance R2.
    '''
    try:
        SPL2 = SPL1 - 20*math.log10(R2/R1)
    except Exception:
        SPL2 = math.nan

    SPL2 = round(SPL2,2)
    return SPL2



def distAttenLine(SPL1, R1, R2):
    '''
    Attenuation due to distance from a (infinite) line source of sound. (Follows the 6db reduction rule per doubling of distance)
    Args:
        SPL1 : Sound Pressure Level at distance R1
        R1 : Distance at which reference noise level SPL1 is measured
        R2 : Distance at which noise level is to be determined
    Returns:
        Sound Pressure Level and distance R2.
    '''
    try:
        SPL2 = SPL1 - 10*math.log10(R2/R1)
    except Exception:
        SPL2 = math.nan

    SPL2 = round(SPL2,2)
    return SPL2


def distAttenWall(SPL1, R1, R2, width, height):
    '''
    Attenuation due to distance from a line source of sound. (Follows the 6db reduction rule per doubling of distance)
    Args:
        SPL1 : Sound Pressure Level at distance R1
        R1 : Distance at which reference noise level SPL1 is measured
        R2 : Distance at which noise level is to be determined
        width: width of the wall in m.
        height: height of the wall in m.
    Returns:
        Sound Pressure Level and distance R2.
    '''

    R_ultranear = width/math.pi
    R_near = height

    try:
        # determine if R1 is in ultranear, near or far.
        if (R1 > R_near):
            zone1 = "farfield"
        if (R1 <= R_near):
            zone1 = "nearfield"
            if (R1 < R_ultranear):
                zone1 = "ultranearfield"
        if (zone1=="farfield"):
            SPL_nearfield = SPL1 -20*math.log10(R_near/R1)
        if (zone1=="nearfield"):
            SPL_nearfield = SPL1 -10*math.log10(R_near/R1)
        if (zone1=="ultranearfield"):
            SPL_nearfield = SPL1 -10*math.log10(R_near/R_ultranear)
        if (R2 > R_near):
            zone2 = "farfield"
        if (R2 <= R_near):
            zone2 = "nearfield"
            if (R2 < R_ultranear):
                zone2 = "ultranearfield"
        if (zone2=="farfield"):
            SPL2 = SPL_nearfield -20*math.log10(R2/R_near)
        if (zone2=="nearfield"):
            SPL2 = SPL_nearfield -10*math.log10(R2/R_near)
        if (zone2=="ultranearfield"):
            SPL2 = SPL_nearfield -10*math.log10(R_ultranear/R_near)

    except Exception:
        SPL2 = math.nan

    SPL2 = round(SPL2,2)
    return SPL2

def test():
    locations = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    width = 20
    height = 10
    spl1 = 107

    outstr = "distance {} - Noise {}"
    for loc in locations:
        spl2 = distance_attenuation_wall(SPL1=107, R1=0.5, R2=loc, width=width, height=height)
        print(outstr.format(loc, spl2))


def noiseMap(emissionPoints, immisionPoints):
    Q = 2
    noiseField = []
    for listener in immisionPoints:
        intensity = 0
        sumIntensity = 0
        x_listener = float(listener['x'])
        y_listener = float(listener['y'])

        for source in emissionPoints:
            pwl = float(source['pwl'])
            x_source = float(source['x'])
            y_source = float(source['y'])
            distance = math.sqrt((x_source - x_listener)**2 + (y_source - y_listener)**2)
            spl = getSPL(PWL=pwl, Q=Q, distance=distance)
            intensity = math.pow(10, spl/10)
            sumIntensity = sumIntensity+intensity

        spl_total = 10*math.log10(sumIntensity)

        point_noise = {"x": x_listener, "y": y_listener, "noise": spl_total}
        noiseField.append(point_noise)

    return noiseField





def spl2pwl():
    pass
