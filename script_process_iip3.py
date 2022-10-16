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
# System Imports
import numpy as np
import pylab as pl
pl.ion()

# Local Imports
import load_cable_atten
import load_digitalattenuator_cal

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

atten_chan3 = load_digitalattenuator_cal.Load_DigitalAttenuator_Cal(CAL_ATTEN_CHAN3)
atten_chan4 = load_digitalattenuator_cal.Load_DigitalAttenuator_Cal(CAL_ATTEN_CHAN4)
atten_cableA = load_cable_atten.Load_Cable_Atten(CAL_CABLEA_F)
atten_cableB = load_cable_atten.Load_Cable_Atten(CAL_CABLEB_F)
atten_cableC = load_cable_atten.Load_Cable_Atten(CAL_CABLEC_F)

test_data = np.load(TEST_DATA_F)
test_data_keys = list(test_data.keys())

P_TONE1_STIM_dBm = test_data["P_TONE1_STIM_dBm"]
P_TONE2_STIM_dBm = test_data["P_TONE2_STIM_dBm"]
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
    stim_atten1 = atten_chan3.real_atten_avg(atten_list_stim[idx], 4400e6)
    stim_atten2 = atten_chan3.real_atten_avg(atten_list_stim[idx], 4410e6)
    stim_atten1 += atten_cableB.real_atten_avg(marker1_freq)
    stim_atten2 += atten_cableB.real_atten_avg(marker2_freq)


    P_in1[idx] = P_TONE1_STIM_dBm + stim_atten1
    P_in2[idx] = P_TONE2_STIM_dBm + stim_atten2

    result_atten1 = atten_chan4.real_atten_avg(atten_list_result[idx], marker1_freq)
    result_atten2 = atten_chan4.real_atten_avg(atten_list_result[idx], marker2_freq)
    result_atten3 = atten_chan4.real_atten_avg(atten_list_result[idx], marker3_freq)
    result_atten4 = atten_chan4.real_atten_avg(atten_list_result[idx], marker4_freq)
    result_atten1 += atten_cableA.real_atten_avg(marker1_freq, 4) + atten_cableC.real_atten_avg(marker1_freq, 4)
    result_atten2 += atten_cableA.real_atten_avg(marker2_freq, 4) + atten_cableC.real_atten_avg(marker2_freq, 4)
    result_atten3 += atten_cableA.real_atten_avg(marker3_freq, 4) + atten_cableC.real_atten_avg(marker3_freq, 4)
    result_atten4 += atten_cableA.real_atten_avg(marker4_freq, 4) + atten_cableC.real_atten_avg(marker4_freq, 4)

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

p_in_idx = np.absolute(P_in1 - (-5)).argmin()

pl.figure()
pl.plot(P_in1[p_in_idx:], P_out1[p_in_idx:]) # IMD1
pl.plot(P_in1[p_in_idx:], P_out3[p_in_idx:]) # IMD3
pl.plot(x_imd3, imd1)
pl.plot(x_imd3, imd3)
# pl.axis('equal')
pl.title("IIP3 Measurement : {}".format(TEST_DATA_F))
pl.xlabel("$P_{IN}$ [dBm]")
pl.ylabel("$P_{OUT}$ [dBm]")


