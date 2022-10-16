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
CAL_P_IN = "cal_data/Power_List_2022-10-12_1639.npz"

# Filenames for test data
# TEST_DATA_F = "ipx_data/SN0013_IIP3_2022-10-11_1847.npz"
# SN0013, IIP3 dataset, stimulating the RF port and looking at the BB port 4
TEST_DATA_IP1_F = "ipx_data/SN0013_IP1_DN_BB_2022-10-12_1742.npz"
TEST_DATA_IP2_F = "ipx_data/SN0013_IP2_DN_BB_2022-10-12_1744.npz"

'''This needs to be a value that is stored in the test_data'''

atten_chan3 = load_digitalattenuator_cal.Load_DigitalAttenuator_Cal(CAL_ATTEN_CHAN3)
atten_chan4 = load_digitalattenuator_cal.Load_DigitalAttenuator_Cal(CAL_ATTEN_CHAN4)
atten_cableA = load_cable_atten.Load_Cable_Atten(CAL_CABLEA_F)
atten_cableB = load_cable_atten.Load_Cable_Atten(CAL_CABLEB_F)
atten_cableC = load_cable_atten.Load_Cable_Atten(CAL_CABLEC_F)

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
ip1_stim_power_dBm = p_in_cal_dBm - atten_cableA.real_atten_avg(4410e6, 4)
ip1_atten_setting = test_data_ip1["atten_list_result"]

ip2_pxa_val = test_data_ip2["marker1"] # Same measurment as IP1 but with the marker at a different Freq

'''
Finaly some calculations here

P_in = P_TONE1_STIM_dBm + Atten_setting + CableB
P_out = Marker - CableC - CableA - Atten_setting
'''
ip1_data = ip1_pxa_val
ip1_data -= atten_cableA.real_atten_avg(90e6, 4)
ip1_data -= atten_cableC.real_atten_avg(90e6, 4)
ip1_data -= atten_chan3.atten_curve_at_freq(90e6)[23*4:45*4+1]

ip2_data = ip2_pxa_val
ip2_data -= atten_cableA.real_atten_avg(90e6, 4)
ip2_data -= atten_cableC.real_atten_avg(90e6, 4)
ip2_data -= atten_chan3.atten_curve_at_freq(90e6)[23*4:45*4+1]


''' First attempt at a linear fit of some sort'''
# linear space for plugging into line fits
x_imd1 = np.linspace(-5, 65, 300)
# find the general gain of the circuit by looking at the 0dBm input power result
G_idx = np.absolute(ip1_stim_power_dBm - 0.0).argmin()
Gain = ip1_data[G_idx]
imd1 = 1 * x_imd1 + Gain
imd2_b = ip2_data[G_idx]
imd2 = 2 * x_imd1 + imd2_b

pl.figure()
pl.plot(ip1_stim_power_dBm, ip1_data) # IMD1
pl.plot(ip1_stim_power_dBm, ip2_data) # IMD2
pl.plot(x_imd1, imd1)
pl.plot(x_imd1, imd2)
# pl.axis('equal')
pl.title("IIP2 Measurement : {}".format(TEST_DATA_IP2_F))
pl.xlabel("$P_{IN}$ [dBm]")
pl.ylabel("$P_{OUT}$ [dBm]")


