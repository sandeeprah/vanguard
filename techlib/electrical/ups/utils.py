import os
from math import *
import pandas as pd
from collections import OrderedDict
from techlib.mathutils import roundit, getindex, linear_interp, linarray_interp


def getCellSize(amp_data_known, amp_data_random, cell_range, Veod, T, design_margin, aging_factor):
    size = 0
    AH_calculated = getInitialAH(amp_data_known, amp_data_random)
    cellAh_selected, strings = selectCellAh(AH_calculated, cell_range)
#    print("Cell Ah selected is {}".format(cellAh_selected))
    iterate = True
    iteration = 0

    while (iterate):
        iteration = iteration + 1
#        print("iteration is {}".format(iteration))
        # no of sections is the same as the number of Periods hence
        N = len(amp_data_known)
        #loop through all Sections to get Fs_max
        Fs_max = 0
        for S in range(1,N+1):
#            print("section is {}".format(S))
            #loop through periods upto section no
            Fs = 0
            for P in range(1, S+1):
#                print("period is {}".format(P))
                A1 = amp_data_known.loc[P,'A']
                if (P==1):
                    A2 = 0
                else:
                    A2 = amp_data_known.loc[P-1,'A']
                delA = (A1 - A2)/float(strings)
                t = 0
                for m in range(P, S+1):
#                    print("M"+str(m))
                    t = t + amp_data_known.loc[m,'duration']
#                print("t is {}".format(t))
                Kt = getKt(cellAh_selected, t, cell_range, Veod)
#                print("Kt is {}".format(Kt))
                Td = getTd(T, t, cell_range)
#                print("Td is {}".format(Td))
                Fs = Fs + delA*Kt*Td

#            print("Fs is {}".format(Fs))
            if (Fs > Fs_max):
                Fs_max = Fs
#        print("Fs_max is {}".format(Fs_max))

        Fs_random = 0
        for index, row in amp_data_random.iterrows():
            t = row['duration']
            A =  row['A']/float(strings)
            Kt = getKt(cellAh_selected, t, cell_range, Veod)
            Td = getTd(T, t, cell_range)
            Fs_random = Fs_random + Kt*A*Td
#        print("Fs_random is {}".format(Fs_random))

        Fs_uncorrected = Fs_max + Fs_random
        Fs_corrected = Fs_uncorrected*design_margin*aging_factor
        Fs_corrected_total = Fs_corrected*strings

#        print("Fs corrected total is {}".format(Fs_corrected_total))
#        print("Strings is {}".format(strings))
        cellAh_selected_new, strings_new = selectCellAh(Fs_corrected_total, cell_range)
#        print("cellAh_selected is {}".format(cellAh_selected))
#        print("cellAh_selected_new is {}".format(cellAh_selected_new))
        if (cellAh_selected_new == cellAh_selected) and (strings_new==strings):
            iterate = False
        if (iteration > 5):
            iterate = False
        cellAh_selected = cellAh_selected_new
        strings = strings_new


    return  Fs_max, Fs_random, Fs_uncorrected, Fs_corrected, cellAh_selected, strings


def getAmpDataKnown(loads_known, Vmin):
    time = []
    for ld in loads_known:
        try:
            t= float(ld['begin'])
            if (t not in time):
                time.append(t)
        except:
            pass

        try:
            t= float(ld['end'])
            if (t not in time):
                time.append(t)
        except:
            pass

    time.sort()
    n_period = len(time)-1
    cell_data = []

    df = pd.DataFrame(columns=['period','duration','A'])
    df = df.set_index('period')

    for i in range(0, n_period):
        period_begins_at = time[i]
        period_ends_at = time[i+1]
        period_midval = (period_begins_at + period_ends_at)/2
        duration = period_ends_at - period_begins_at
        period = i+1
        A= getInstantAmpereLoad(loads_known, period_midval, Vmin)
        df.loc[period] = [duration, A]
    return df


def getAmpDataRandom(loads_random, Vmin):
    cell_data=[]
    n = len(loads_random)
    df = pd.DataFrame(columns=['No.','duration','A'])
    df = df.set_index('No.')

    for index, ld in enumerate(loads_random):
        no = index+1
        duration = float(ld['duration'])
        if (ld['unit']=='A'):
            A = float(ld['load'])
        elif(ld['unit']=='W'):
            A = float(ld['load'])/Vmin
        else:
            raise Exception('Invalid Units')

        df.loc[no] = [duration, A]

    return df



def getInstantAmpereLoad(loads_known, time_instant, Vmin):
    amps_total = 0
    for ld in loads_known:
        begin = float(ld['begin'])
        end = float(ld['end'])
        if (time_instant >=begin) and (time_instant < end):
            if (ld['unit']=='A'):
                amps_total = amps_total + float(ld['load'])
            elif (ld['unit']=='W'):
                amps_total = amps_total + float(ld['load'])/Vmin
            else:
                raise Exception('Invalid units')

    return amps_total



def getInitialAH(amp_data_known, amp_data_random):
    AH_total = 0
    for index, row in amp_data_known.iterrows():
        AH_total = AH_total + row['duration']*row['A']/60

    for index, row in amp_data_random.iterrows():
        AH_total = AH_total + row['duration']*row['A']/60

    return AH_total

def selectCellAh(calculatedAH, cell_range):
    cellAh = -1
    if (cell_range=='L'):
        data_file = "L_Cell_1000mV_EOD.csv"
    elif(cell_range=='M'):
        data_file = "M_Cell_1000mV_EOD.csv"
    elif (cell_range=='H'):
        data_file = "H_Cell_1000mV_EOD.csv"
    else:
        raise Exception('Invalid choice of cell range')

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        rates_df = pd.read_csv(data_file_path)
        rates_df = rates_df.set_index('Ah')

        not_found = True
        strings = 1
        while (not_found):
            AHperCell = float(calculatedAH)/float(strings)
            for index, row in rates_df.iterrows():
                if (index > AHperCell):
                    cellAh = index
                    not_found = False
                    break
            if (not_found):
                strings = strings+1
                if (strings>3):
                    raise Exception('too many strings in parallel required. Check with manufacturer')

    except Exception as e:
        raise e
        raise Exception('cellAh could not be found')

    return cellAh, strings

def getKt(AH_Rating, time, cell_range, Veod):
    Kt = 0
    #data_file = "cell_discharge_rates.csv"
    if (cell_range=='L'):
        a = "L_Cell_"
    elif (cell_range=='M'):
        a = "M_Cell_"
    elif (cell_range=='H'):
        a = "H_Cell_"
    else:
        raise Exception('Invalid choice of cell range')

    if (Veod<1) or (Veod>1.14):
        raise Exception('End of discharge voltage not in acceptable range (1V to 1.14V). Can not calculate Kt. Check if the no. of cells in series are in permitted range.')

    Veod_values = [1,1.05, 1.1, 1.14]
    Veod_labels = ["1000mV", "1050mV", "1100mV", "1140mV"]
    index_lower, index_higher =getindex(Veod_values, Veod)
    b_lower = Veod_labels[index_lower]
    b_higher = Veod_labels[index_higher]
    data_file_lower = a + b_lower + "_EOD.csv"
    data_file_higher = a + b_higher + "_EOD.csv"

    Veod_lower = Veod_values[index_lower]
    Veod_higher = Veod_values[index_higher]


    t1_lower, A1_lower, t2_lower, A2_lower = readDischargeRate(data_file_lower, AH_Rating, time)
    t1_higher, A1_higher, t2_higher, A2_higher = readDischargeRate(data_file_higher, AH_Rating, time)

    A1 = linear_interp(Veod, Veod_lower, A1_lower, Veod_higher, A1_higher)
    A2 = linear_interp(Veod, Veod_lower, A2_lower, Veod_higher, A2_higher)
    t1 = t1_lower
    t2 = t2_lower
    Kt1 = AH_Rating/A1
    Kt2 = AH_Rating/A2
    Kt = linear_interp(time, t1, Kt1, t2, Kt2)


    return Kt


def getTd(temperature, time, cell_range):
    if (temperature > 25):
        Td = 1
        return Td

    if (cell_range =='L'):
        data_file = 'L_cell_deration.csv'
        time_values = [60, 300]
        if time < 60:
            time = 60
        if time > 300:
            time = 300

        index_lower, index_higher = getindex(time_values, time)
        time_lower = time_values[index_lower]
        time_higher = time_values[index_higher]
    elif(cell_range=='H'):
        data_file='H_cell_deration.csv'
        time_values = [1, 30, 300]
        if time < 1:
            time = 1
        if time > 300:
            time = 300
        index_lower, index_higher = getindex(time_values, time)
        time_lower = time_values[index_lower]
        time_higher = time_values[index_higher]
    elif(cell_range=='M'):
        data_file ='M_cell_deration.csv'
        time_values = [15, 60, 300]
        if time < 15:
            time = 15
        if time > 300:
            time = 300
        index_lower, index_higher = getindex(time_values, time)
        time_lower = time_values[index_lower]
        time_higher = time_values[index_higher]
    else:
        raise Exception('Failed to calculate Td. Invalid choice of cell range')

    '''
    data_file = "T_derate.csv"
    time_values = [10, 30, 60, 180, 300]
    '''
    T_lower = "T_"+str(time_values[index_lower])
    C_lower = "C_"+str(time_values[index_lower])

    T_higher = "T_"+str(time_values[index_higher])
    C_higher = "C_"+str(time_values[index_higher])
    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        rates_df = pd.read_csv(data_file_path)
        rates_df = rates_df.set_index('S_No')
        T_lower_values = rates_df[T_lower].tolist()
        C_lower_values = rates_df[C_lower].tolist()
        deration_lower = linarray_interp(T_lower_values, C_lower_values, temperature)

        T_higher_values = rates_df[T_higher].tolist()
        C_higher_values = rates_df[C_higher].tolist()
        deration_higher = linarray_interp(T_higher_values, C_higher_values, temperature)

        deration = linear_interp(time, time_lower, deration_lower, time_higher, deration_higher)

    except Exception as e:
        raise e
        raise Exception('Td could not be calculated')

    Td = (1/deration)

    return Td




def readDischargeRate(data_file, AH_Rating, time):
    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        rates_df = pd.read_csv(data_file_path)
        rates_df = rates_df.set_index('Ah')
        #print("AH rating in lookup is {}".format(AH_Rating))
        discharge_rates = rates_df.loc[AH_Rating]
        discharge_rates = discharge_rates.drop(['Model'])
        time_values = discharge_rates.index.tolist()
        current_values = discharge_rates.values.tolist()
        for index, val  in enumerate(time_values):
            time_values[index] = float(val)

        time_values.reverse()
        current_values.reverse()

        index_lower, index_higher = getindex(time_values, time)
        t1 = time_values[index_lower]
        t2 = time_values[index_higher]
        A1 = current_values[index_lower]
        A2 = current_values[index_higher]
        A1 = roundit(A1)
        A2 = roundit(A2)
    except KeyError:
        raise Exception('Error occured while reading cell discharge rates. Ah rating not found in cell range selected.')
    except TypeError:
        raise Exception('Error occured while reading cell discharge rates. Time used to obtain cell discharge rate outside defined range for the cell.')
    except FileNotFoundError:
        raise Exception('Error occured while reading cell discharge rates. File for cell range selected could not be found. Check if correct cell range and cell End of Discharge values are used.')
    except Exception as e:
        raise Exception('Error occured while reading cell discharge rates. ' + str(e))

    return t1, A1, t2, A2
