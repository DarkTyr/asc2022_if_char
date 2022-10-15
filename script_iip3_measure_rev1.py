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
import phasematrix_serial


'''In the future make these passable by command line interfaces, for now hard code is fine'''
ATTEN_COM_PORT = "COM11"
SYNTH0_COM_PORT = "COM16"
SYNTH1_COM_PORT = "COM17"
ENA_IP = "192.168.0.15"
PXA_IP = "192.168.0.16"
ATTEN_START = 23.0
ATTEN_STOP = 45.0
POWER_START = -3.0
POWER_STOP = -25.0
SYNTH0_POWER_OFFSET = 0.3
SYNTH1_POWER_OFFSET = 0.0
ATTEN_STEP_SIZE = 0.25 # Has to be modulo 0.25
POWER_STEP_SIZE = ATTEN_STEP_SIZE # has to match ATTEN step size to keep the same applied power on the PXA
POWER_CAL_F = "cal_data/Power_List_2tone_2022-10-13.npz"
# FREQ_INDEX_START = 1111 # Used for plotting
RESULT_ATT_CHANNEL = 3
WAIT_BETWEEN_STEPS_S = 0.25

rm = pyvisa.ResourceManager()
pxa = keysight_pxa_eth.Keysight_PXA_Eth(rm, resource_name="TCPIP::{}::inst0::INSTR".format(PXA_IP))
pxa.open()

synth0 = phasematrix_serial.PhaseMatrix_Serial(port=SYNTH0_COM_PORT)
synth1 = phasematrix_serial.PhaseMatrix_Serial(port=SYNTH1_COM_PORT)
synth0.open()
synth1.open()

att = adaura.Adaura_4Chan_Attenuator_USB(ATTEN_COM_PORT)
att.debug = False


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

nSteps = int((ATTEN_STOP - ATTEN_START)/ATTEN_STEP_SIZE + 1)    # Add 1 to the end point value
atten_list_result = np.linspace(ATTEN_START, ATTEN_STOP, nSteps)
nSteps_pow = int(np.absolute(POWER_STOP - POWER_START)/POWER_STEP_SIZE + 1)    # Add 1 to include the endpoint value

if(nSteps_pow != nSteps):
    print("nSteps_pow and nSteps must be equal, this is going to break")

power_list_dBm = np.linspace(POWER_STOP, POWER_START, nSteps)

''' Make variables to store useful data'''
marker1 = np.zeros(nSteps)
marker2 = np.zeros(nSteps)
marker3 = np.zeros(nSteps)
marker4 = np.zeros(nSteps)

''' Just for record, get the frequencies of the markers. Helps in keeping track of which marker power is which tone'''
f_marker1_Hz = pxa.getMarkFreq_Hz(1)
f_marker2_Hz = pxa.getMarkFreq_Hz(2)
f_marker3_Hz = pxa.getMarkFreq_Hz(3)
f_marker4_Hz = pxa.getMarkFreq_Hz(4)

idx = 0
print("Estimated time to take data: {} Minutes".format(nSteps*WAIT_BETWEEN_STEPS_S/60.0))
while (idx < nSteps):
    print("IDX : {}, atten_result : {}, power_list_dBm : {}".format(idx, atten_list_result[idx], power_list_dBm[idx]))
    # Set stimulus attenuator channel
    synth0.setPowerdBm(power_list_dBm[idx] + SYNTH0_POWER_OFFSET)
    synth1.setPowerdBm(power_list_dBm[idx] + SYNTH1_POWER_OFFSET)
    # Set Response attenuator channel
    att.set_atten(RESULT_ATT_CHANNEL, atten_list_result[idx])
    time.sleep(WAIT_BETWEEN_STEPS_S)
    marker1[idx] = pxa.getMarkPower(1)
    marker2[idx] = pxa.getMarkPower(2)
    marker3[idx] = pxa.getMarkPower(3)
    marker4[idx] = pxa.getMarkPower(4)
    idx += 1

NOTES = \
"Power calibration data does not remove the cable loss from cableA, so that has been added to the cable list" \
"and should be removed. This is Rev1 Method in which I change the Synth0 and Synth1 output power to change" \
"the P_in on the DUT. THen I use an attenuator to change the P_out to keep the power more or less constant" \
"on the PXA."

'''Serial number_IIP3_{UP_mix|DN_Mix}-{Measured port BB|RF}'''
np.savez_compressed("ipx_data/SN0013_IIP3_DN-BB_2022-10-13_1753",
                    rev = "Rev1 Method",
                    nSteps = nSteps,
                    power_list_dBm = power_list_dBm,
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
                    RESULT_ATT_CHANNEL = RESULT_ATT_CHANNEL,
                    cables = "INPUT : Power_cal, CableA, OUTPUT : CableC, Atten_CHan3, CableA",
                    POWER_CAL_F = POWER_CAL_F,
                    notes = NOTES
                    )

