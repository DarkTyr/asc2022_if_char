# -*- coding: utf-8 -*-
'''

=================================

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
TEST_DATA_IP3_F = "ipx_data/SN0013_IIP3_DN-BB4_2022-10-12_1153.npz"

# SN0013, IIP2
CAL_IP1_P_IN_F = "cal_data/Power_List_2022-10-12_1639.npz"
TEST_DATA_IP1_F = "ipx_data/SN0013_IP1_DN_BB_2022-10-12_1742.npz"
TEST_DATA_IP2_F = "ipx_data/SN0013_IP2_DN_BB_2022-10-12_1744.npz"


atten_chan3 = load_digitalattenuator_cal.Load_DigitalAttenuator_Cal(CAL_ATTEN_CHAN3)
atten_chan4 = load_digitalattenuator_cal.Load_DigitalAttenuator_Cal(CAL_ATTEN_CHAN4)
atten_cableA = load_cable_atten.Load_Cable_Atten(CAL_CABLEA_F)
atten_cableB = load_cable_atten.Load_Cable_Atten(CAL_CABLEB_F)
atten_cableC = load_cable_atten.Load_Cable_Atten(CAL_CABLEC_F)

test_data_IP3 = np.load(TEST_DATA_IP3_F)
test_data_keys = list(test_data_IP3.keys())

P_TONE1_STIM_dBm = test_data_IP3["P_TONE1_STIM_dBm"]
P_TONE2_STIM_dBm = test_data_IP3["P_TONE2_STIM_dBm"]
# f_RF1 = 4400 MHz
# f_RF2 = 4410 MHz
# f_LO = 4500 MHz
# 
# f1 = f_RF1 - f_LO = Marker1
# f2 = f_RF2 - f_LO = Marker2
# f3 = 2*f_RF1 - f_RF2 - f_LO = Maker3
# f4 = 2*f_RF2 - f_RF1 - f_LO = Maker4
marker1 = test_data_IP3["marker1"]
marker2 = test_data_IP3["marker2"]
marker3 = test_data_IP3["marker3"]
marker4 = test_data_IP3["marker4"]
marker1_freq = test_data_IP3["f_marker1_Hz"]
marker2_freq = test_data_IP3["f_marker2_Hz"]
marker3_freq = test_data_IP3["f_marker3_Hz"]
marker4_freq = test_data_IP3["f_marker4_Hz"]
nSteps = test_data_IP3["nSteps"]
atten_list_stim = test_data_IP3["atten_list_stim"]
atten_list_result = test_data_IP3["atten_list_result"]

P_in1 = np.zeros(nSteps)
P_out1 = np.zeros(nSteps)
P_in2 = np.zeros(nSteps)
P_out2 = np.zeros(nSteps)
P_out3 = np.zeros(nSteps)
P_out4 = np.zeros(nSteps)

test_data_ip1 = np.load(TEST_DATA_IP1_F)
test_data_ip1_keys = list(test_data_ip1.keys())
test_data_ip2 = np.load(TEST_DATA_IP2_F)
test_data_ip2_keys = list(test_data_ip2.keys())
p_in_ip2_cal = np.load(CAL_IP1_P_IN_F)
p_in_ip2_cal_dBm = p_in_ip2_cal["marker1"] # The real applied power to the DUT


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
    
''' First attempt at a linear fit of some sort '''
# linear space for plugging into line fits
x_imd3 = np.linspace(-5, 26, 100)
# find the general gain of the circuit by looking at the 0dBm input power result
G_idx = np.absolute(P_in1 - 1.0).argmin()
Gain = P_out1[G_idx] - P_in1[G_idx]
imd1 = 1 * x_imd3 + Gain
imd3_b = P_out3[G_idx] - P_in1[G_idx]*3
imd3 = 3 * x_imd3 + imd3_b

p_in_idx = np.absolute(P_in1 - (-5)).argmin()



ip1_pxa_val = test_data_ip1["marker1"]
# Real power being applied as measured on the PXA in the power_cal file, cal was performed through CabeA
ip1_stim_power_dBm = p_in_ip2_cal_dBm - atten_cableA.real_atten_avg(4410e6, 4)
ip1_atten_setting = test_data_ip1["atten_list_result"]

ip2_pxa_val = test_data_ip2["marker1"] # Same measurment as IP1 but with the marker at a different Freq

'''
Finaly some calculations here

P_in = P_TONE1_STIM_dBm + Atten_setting + CableB
P_out = Marker - CableC - CableA - Atten_setting
'''
ip1_data = ip1_pxa_val + 0.52
ip1_data -= atten_cableA.real_atten_avg(90e6, 4)
ip1_data -= atten_cableC.real_atten_avg(90e6, 4)
ip1_data -= atten_chan3.atten_curve_at_freq(90e6)[23*4:45*4+1]

ip2_data = ip2_pxa_val + 0.52
ip2_data -= atten_cableA.real_atten_avg(90e6, 4)
ip2_data -= atten_cableC.real_atten_avg(90e6, 4)
ip2_data -= atten_chan3.atten_curve_at_freq(90e6)[23*4:45*4+1]


''' First attempt at a linear fit of some sort'''
# linear space for plugging into line fits
x_imd1 = np.linspace(-5, 65, 300)
# find the general gain of the circuit by looking at the 0dBm input power result
G_IP1_idx = np.absolute(ip1_stim_power_dBm - 0.0).argmin()
Gain_IP1 = ip1_data[G_IP1_idx]
imd1_ip2 = 1 * x_imd1 + Gain_IP1
imd2_b = ip2_data[G_IP1_idx]
imd2 = 2 * x_imd1 + imd2_b


pl.figure()
pl.plot(P_in1[p_in_idx:], P_out1[p_in_idx:], label="IP1") # IMD1
pl.plot(ip1_stim_power_dBm[:-28], ip2_data[:-28], label="IP2") # IMD2
pl.plot(P_in1[p_in_idx:], P_out3[p_in_idx:], label="IP3") # IMD3
pl.plot(x_imd3, imd1, label="IP1-1:1 Line")
pl.plot(x_imd1, imd2, label="IP2-1:2 Line")
pl.plot(x_imd3, imd3, label="IP3-1:3 Line")
pl.xlim(-5, 10)
pl.ylim(-70, 20)
# pl.axis('equal')
pl.title("IIPn : SN0013")
pl.xlabel("$P_{IN}$ [dBm]")
pl.ylabel("$P_{OUT}$ [dBm]")
pl.legend()
