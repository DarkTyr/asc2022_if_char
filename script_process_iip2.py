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
CAL_P_IN = "cal_data/Power_List_2022-10-12_1639.npz"

# Filenames for test data
# TEST_DATA_F = "ipx_data/SN0013_IIP3_2022-10-11_1847.npz"
# SN0013, IIP3 dataset, stimulating the RF port and looking at the BB port 4
TEST_DATA_IP1_F = "ipx_data/SN0013_IP1_DN_BB_2022-10-12_1742.npz"
TEST_DATA_IP2_F = "ipx_data/SN0013_IP2_DN_BB_2022-10-12_1744.npz"

'''This needs to be a value that is stored in the test_data'''

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
        data = self.all_data[:, freq_idx]
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

    def real_atten_avg(self, desired_freq_Hz:float, avg_width=10) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        real_atten_dB = np.average(self.all_data[freq_idx-avg_width:freq_idx+avg_width+1])
        return real_atten_dB

atten_chan3 = Load_Atten_Cal(CAL_ATTEN_CHAN3)
atten_chan4 = Load_Atten_Cal(CAL_ATTEN_CHAN4)
atten_cableA = Load_Cable_Atten(CAL_CABLEA_F)
atten_cableB = Load_Cable_Atten(CAL_CABLEB_F)
atten_cableC = Load_Cable_Atten(CAL_CABLEC_F)

test_data_ip1 = np.load(TEST_DATA_IP1_F)
test_data_ip1_keys = list(test_data_ip1.keys())
test_data_ip2 = np.load(TEST_DATA_IP2_F)
test_data_ip2_keys = list(test_data_ip2.keys())

p_in_cal = np.load(CAL_P_IN)
p_in_cal_dBm = p_in_cal["marker1"] # The real applied power to the DUT

# f_RF1 = 4400 MHz
# f_RF2 = 4410 MHz
# f_LO = 4500 MHz
# 
# f1 = f_RF1 - f_LO = Marker1
# f2 = f_RF2 - f_LO = Marker2
# f3 = 2*f_RF1 - f_RF2 - f_LO = Maker3
# f4 = 2*f_RF2 - f_RF1 - f_LO = Maker4

ip1_pxa_val = test_data_ip1["marker1"]
# Real power being applied as measured on the PXA in the power_cal file, cal was performed through CabeA
ip1_stim_power_dBm = p_in_cal_dBm - atten_cableA.real_atten_avg(4400e6)
ip1_atten_setting = test_data_ip1["atten_list_result"]

ip2_pxa_val = test_data_ip2["marker1"] # Same measurment as IP1 but with the marker at a different Freq

'''
Finaly some calculations here

P_in = P_TONE1_STIM_dBm + Atten_setting + CableB
P_out = Marker - CableC - CableA - Atten_setting
'''
ip1_data = ip1_pxa_val
ip1_data -= atten_cableA.real_atten_avg(90e6)
ip1_data -= atten_cableC.real_atten_avg(90e6)
ip1_data -= atten_chan3.atten_curve_at_freq(90e6)[23*4:45*4+1]

ip2_data = ip2_pxa_val
ip2_data -= atten_cableA.real_atten_avg(90e6)
ip2_data -= atten_cableC.real_atten_avg(90e6)
ip2_data -= atten_chan3.atten_curve_at_freq(90e6)[23*4:45*4+1]


''' First attempt at a linear fit of some sort'''
# linear space for plugging into line fits
x = np.linspace(-5, 65, 300)
# find the general gain of the circuit by looking at the 0dBm input power result
G_idx = np.absolute(ip1_stim_power_dBm - 0.0).argmin()
Gain = ip1_data[G_idx]
imd1 = 1 * x + Gain
imd2_b = ip2_data[G_idx]
imd2 = 2 * x + imd2_b

pl.figure()
pl.plot(ip1_stim_power_dBm, ip1_data) # IMD1
pl.plot(ip1_stim_power_dBm, ip2_data) # IMD2
pl.plot(x, imd1)
pl.plot(x, imd2)
pl.axis('equal')



