# -*- coding: utf-8 -*-
'''
Script Input Intermodulation Product 3rd Order Measurement
=================================
This script uses the Adaura digital attenuator and ENA to generate calibration data for the attenuator. 
It is expected that a decent four port calibration using an ECal module on the ENA has been performed
and is active. This removes systematics from the cabling and generates a far better calibration data.

The saved data is a frequency array (which gives an index for frequency), a list of calable attenuations
(which gives you an index for programed attenuation) and then what the actuall attenuation was. 

Now theroetically one could work backwards, knowing the frequency, and desired attenuation to figure
out the closest attenuator value setting to achieve the desired attenuation. We aren't doing any of these
calculations here.
'''

import numpy as np
import time
import pylab as pl
pl.ion()

# calibration File names
CAL_CABLEA_F = "cal_data/cableA.npz"
CAL_CABLEB_F = "cal_data/cableB.npz"
CAL_CABLEC_F = "cal_data/cableC.npz"
CAL_ATTEN_CHAN3 = "cal_data/adaura_Channel3_Cal.npz"
CAL_ATTEN_CHAN4 = "cal_data/adaura_Channel4_Cal.npz"

# Filenames for test data
# TEST_DATA_F = "ipx_data/SN0013_IIP3_2022-10-11_1847.npz"
# SN0013, IIP3 dataset, stimulating the RF port and looking at the BB port 4
TEST_DATA_F = "ipx_data/SN0013_IIP3_DN-BB4_2022-10-12_1153.npz"

'''This needs to be a value that is stored in the test_data'''
P_TONE1_STIM_dBm = -2.1 + 19.88 # dBm
P_TONE2_STIM_dBm = -2.1 + 19.88 # dBm

class Load_Atten_Cal():
    def __init__(self, f_name:str):
        self.debug = False
        self.fname = f_name
        self.data = np.load(self.fname)
        self.keys = list(self.data.keys())
        self.freqs_Hz = self.data["freqs_Hz"]
        self.all_data = self.data["measured_attenuations_chan"]

    def atten_curve_at_freq(self, desired_freq_Hz:float):
        '''Extract the desired atten vs real attenuation at a specific frequency'''
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        data = self.data[:, freq_idx]
        return data

    def _nearest_frequency_Hz(self, desired_freqeucy_Hz:float) -> int:
        ''' Returns the freq index that is closest to the desired frequency'''
        diff_array = np.absolute(self.freqs_Hz - desired_freqeucy_Hz)
        idx = diff_array.argmin()
        if(self.debug):
            print("Load_Atten_Cal._nearest_frequency_Hz():{} Hz".format(desired_freqeucy_Hz))
            print("  Found nearest Frequency : {} Hz".format(self.freqs_Hz[idx]))
            print("  IDX : {}".format(idx))
        '''Pretty simple once you think about it but the code is reference and soured from:
        https://www.geeksforgeeks.org/find-the-nearest-value-and-the-index-of-numpy-array/#:~:text=The%20approach%20to%20finding%20the%20nearest%20value%20and,values%20in%20a%20difference%20array%2C%20say%20difference_array%20%5B%5D.
        '''
        return int(idx)
    
    def real_atten(self, atten_setting:float, desired_freq_Hz:float) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        if(atten_setting % 0.25):
            print("atten_setting needs to be modulo 0.25")
            return 1e9
        atten_idx = int(atten_setting*4)
        real_atten_dB = self.all_data[atten_idx, freq_idx]
        return real_atten_dB

    def real_atten_avg(self, atten_setting:float, desired_freq_Hz:float, avg_width=10) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        if(atten_setting % 0.25):
            print("atten_setting needs to be modulo 0.25")
            return 1e9
        atten_idx = int(atten_setting*4)
        real_atten_dB = np.average(self.all_data[atten_idx, freq_idx-avg_width:freq_idx+avg_width+1])
        return real_atten_dB

class Load_Cable_Atten():
    def __init__(self, f_name:str):
        self.debug = False
        self.fname = f_name
        self.data = np.load(self.fname)
        self.keys = list(self.data.keys())
        self.freqs_Hz = self.data["freqs"]
        self.all_data = self.data["data"]     

    def _nearest_frequency_Hz(self, desired_freqeucy_Hz:float) -> int:
        ''' Returns the freq index that is closest to the desired frequency'''
        diff_array = np.absolute(self.freqs_Hz - desired_freqeucy_Hz)
        idx = diff_array.argmin()
        if(self.debug):
            print("Load_Atten_Cal._nearest_frequency_Hz():{} Hz".format(desired_freqeucy_Hz))
            print("  Found nearest Frequency : {} Hz".format(self.freqs_Hz[idx]))
            print("  IDX : {}".format(idx))
        '''Pretty simple once you think about it but the code is reference and soured from:
        https://www.geeksforgeeks.org/find-the-nearest-value-and-the-index-of-numpy-array/#:~:text=The%20approach%20to%20finding%20the%20nearest%20value%20and,values%20in%20a%20difference%20array%2C%20say%20difference_array%20%5B%5D.
        '''
        return int(idx)
    
    def real_atten(self, desired_freq_Hz:float) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        real_atten_dB = self.all_data[freq_idx]
        return real_atten_dB

    def real_atten(self, desired_freq_Hz:float, avg_width=10) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        real_atten_dB = np.average(self.all_data[freq_idx-avg_width:freq_idx+avg_width+1])
        return real_atten_dB

atten_chan3 = Load_Atten_Cal(CAL_ATTEN_CHAN3)
atten_chan4 = Load_Atten_Cal(CAL_ATTEN_CHAN4)
atten_cableA = Load_Cable_Atten(CAL_CABLEA_F)
atten_cableB = Load_Cable_Atten(CAL_CABLEB_F)
atten_cableC = Load_Cable_Atten(CAL_CABLEC_F)

test_data = np.load(TEST_DATA_F)
test_data_keys = list(test_data.keys())

# f_RF1 = 4400 MHz
# f_RF2 = 4410 MHz
# f_LO = 4500 MHz
# 
# f1 = f_RF1 - f_LO = Marker1
# f2 = f_RF2 - f_LO = Marker2
# f3 = 2*f_RF1 - f_RF2 - f_LO = Maker3
# f4 = 2*f_RF2 - f_RF1 - f_LO = Maker4
marker1 = test_data["marker1"]
marker2 = test_data["marker2"]
marker3 = test_data["marker3"]
marker4 = test_data["marker4"]
marker1_freq = test_data["f_marker1_Hz"]
marker2_freq = test_data["f_marker2_Hz"]
marker3_freq = test_data["f_marker3_Hz"]
marker4_freq = test_data["f_marker4_Hz"]
nSteps = test_data["nSteps"]
atten_list_stim = test_data["atten_list_stim"]
atten_list_result = test_data["atten_list_result"]


P_in1 = np.zeros(nSteps)
P_out1 = np.zeros(nSteps)
P_in2 = np.zeros(nSteps)
P_out2 = np.zeros(nSteps)
P_out3 = np.zeros(nSteps)
P_out4 = np.zeros(nSteps)

'''
Finaly some calculations here

P_in = P_TONE1_STIM_dBm + Atten_setting + CableB
P_out = Marker - CableC - CableA - Atten_setting
'''
for idx in range(nSteps):
    stim_atten1 = atten_chan3.real_atten_avg(atten_list_stim[idx], marker1_freq)
    stim_atten2 = atten_chan3.real_atten_avg(atten_list_stim[idx], marker2_freq)
    stim_atten1 += atten_cableB.real_atten(marker1_freq)
    stim_atten2 += atten_cableB.real_atten(marker2_freq)


    P_in1[idx] = P_TONE1_STIM_dBm + stim_atten1
    P_in2[idx] = P_TONE2_STIM_dBm + stim_atten2

    result_atten1 = atten_chan4.real_atten_avg(atten_list_result[idx], marker1_freq)
    result_atten2 = atten_chan4.real_atten_avg(atten_list_result[idx], marker2_freq)
    result_atten3 = atten_chan4.real_atten_avg(atten_list_result[idx], marker3_freq)
    result_atten4 = atten_chan4.real_atten_avg(atten_list_result[idx], marker4_freq)
    result_atten1 += atten_cableA.real_atten(marker1_freq) + atten_cableC.real_atten(marker1_freq)
    result_atten2 += atten_cableA.real_atten(marker2_freq) + atten_cableC.real_atten(marker2_freq)
    result_atten3 += atten_cableA.real_atten(marker3_freq) + atten_cableC.real_atten(marker3_freq)
    result_atten4 += atten_cableA.real_atten(marker4_freq) + atten_cableC.real_atten(marker4_freq)

    P_out1[idx] = marker1[idx] - result_atten1
    P_out2[idx] = marker2[idx] - result_atten2
    P_out3[idx] = marker3[idx] - result_atten3
    P_out4[idx] = marker4[idx] - result_atten4
    

''' First attempt at a linear fit of somew sort'''
# linear space for plugging into line fits
x_imd3 = np.linspace(-5, 36, 100)
# find the general gain of the circuit by looking at the 0dBm input power result
G_idx = np.absolute(P_in1 - 0.0).argmin()
Gain = P_out1[G_idx]
imd1 = 1 * x_imd3 + Gain
imd3_b = P_out3[G_idx]
imd3 = 3 * x_imd3 + imd3_b

pl.figure()
pl.plot(P_in1, P_out1) # IMD1
pl.plot(P_in1, P_out3) # IMD3
pl.plot(x_imd3, imd1)
pl.plot(x_imd3, imd3)
pl.axis('equal')



