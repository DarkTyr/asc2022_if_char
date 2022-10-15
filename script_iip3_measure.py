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
# System level imports
import time
import pyvisa
import numpy as np
import pylab as pl
pl.ion()

# local imports
import adaura_4chan_attenuator_usb as adaura
import keysight_pxa_eth


'''In the future make these passable by command line interfaces, for now hard code is fine'''
ATTEN_COM_PORT = "COM11"
ENA_IP = "192.168.0.15"
PXA_IP = "192.168.0.16"
ATTEN_START = 0.0
ATTEN_STOP = 35.0
ATTEN_STEP_SIZE = 0.25
# ATTEN_STEP_SIZE = 0.25
# FREQ_INDEX_START = 1111 # Used for plotting
STIM_ATT_CHANNEL = 3
RESULT_ATT_CHANNEL = 4
WAIT_BETWEEN_STEPS_S = 0.25

rm = pyvisa.ResourceManager()
pxa = keysight_pxa_eth.Keysight_PXA_Eth(rm, resource_name="TCPIP::{}::inst0::INSTR".format(PXA_IP))
pxa.open()

'''
Some notes:

Marker1 = 90MHz
Marker2 = 100MHz
Marker3 = 80MHz
Marker4 = 110MHz
n_Avg = 100
IF_BW = 10 kHz
f_Start = 76.25 MHz
f_Stop = 113.75 MHz
f_Span = 37.5 MHz
f_Center = 95 MHz
ref_level = -28 dBm
nPoint = 8192
P_target = -31 on PXA per tone

units Hz and dBm
'''

att = adaura.Adaura_4Chan_Attenuator_USB(ATTEN_COM_PORT)
att.debug = False

nSteps = int((ATTEN_STOP - ATTEN_START)/ATTEN_STEP_SIZE + 1)    # Add 1 to include insertion loss, 0 dB setting
atten_list_stim = np.linspace(ATTEN_STOP, ATTEN_START, nSteps)
atten_list_result = np.linspace(ATTEN_START, ATTEN_STOP, nSteps)
marker1 = np.zeros(nSteps)
marker2 = np.zeros(nSteps)
marker3 = np.zeros(nSteps)
marker4 = np.zeros(nSteps)

f_marker1_Hz = pxa.getMarkFreq_Hz(1)
f_marker2_Hz = pxa.getMarkFreq_Hz(2)
f_marker3_Hz = pxa.getMarkFreq_Hz(3)
f_marker4_Hz = pxa.getMarkFreq_Hz(4)

idx = 0
print("Estimated time to take data: {} Minutes".format(nSteps*WAIT_BETWEEN_STEPS_S/60.0))
while (idx < nSteps):
    print("IDX : {}, atten_stim : {}".format(idx, atten_list_stim[idx]))
    # Set stimulus attenuator channel
    att.set_atten(STIM_ATT_CHANNEL, atten_list_stim[idx])
    # Set Response attenuator channel
    att.set_atten(RESULT_ATT_CHANNEL, atten_list_result[idx])
    time.sleep(WAIT_BETWEEN_STEPS_S)
    marker1[idx] = pxa.getMarkPower(1)
    marker2[idx] = pxa.getMarkPower(2)
    marker3[idx] = pxa.getMarkPower(3)
    marker4[idx] = pxa.getMarkPower(4)
    idx += 1

'''Serial number_IIP3_{UP_mix|DN_Mix}-{Measured port BB|RF}'''
np.savez_compressed("ipx_data/SN0013_IIP3_DN-BB_2022-10-12_1153", 
                    nSteps = nSteps,
                    atten_list_stim = atten_list_stim,
                    atten_list_result = atten_list_result,
                    marker1 = marker1,
                    marker2 = marker2,
                    marker3 = marker3,
                    marker4 = marker4,
                    f_marker1_Hz = f_marker1_Hz,
                    f_marker2_Hz = f_marker2_Hz,
                    f_marker3_Hz = f_marker3_Hz,
                    f_marker4_Hz = f_marker4_Hz,
                    WAIT_BETWEEN_STEPS_S = WAIT_BETWEEN_STEPS_S,
                    ATTEN_START = ATTEN_START,
                    ATTEN_STOP = ATTEN_STOP,
                    ATTEN_STEP_SIZE = ATTEN_STEP_SIZE,
                    STIM_ATT_CHANNEL = STIM_ATT_CHANNEL,
                    RESULT_ATT_CHANNEL = RESULT_ATT_CHANNEL,
                    cables = "INPUT : CableB, OUTPUT : CableC, CableA",
                    P_TONE1_STIM_dBm = -2.1 + 19.88, # dBm
                    P_TONE2_STIM_dBm = -2.1 + 19.88 # dBm
                    )

