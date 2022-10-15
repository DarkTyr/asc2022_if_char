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
import phasematrix_serial
import keysight_pxa_eth


'''In the future make these passable by command line interfaces, for now hard code is fine'''
SYNTH_COM_PORT = "COM17"
ENA_IP = "192.168.0.15"
PXA_IP = "192.168.0.16"
POWER_START = -3.0
POWER_STOP = -25.0
POWER_STEP_SIZE = 0.25
WAIT_BETWEEN_STEPS_S = 0.20

rm = pyvisa.ResourceManager()
pxa = keysight_pxa_eth.Keysight_PXA_Eth(rm, resource_name="TCPIP::{}::inst0::INSTR".format(PXA_IP))
pxa.open()

synth = phasematrix_serial.PhaseMatrix_Serial(port=SYNTH_COM_PORT)
synth.open()

'''

'''

nSteps = int(np.absolute(POWER_STOP - POWER_START)/POWER_STEP_SIZE + 1)    # Add 1 to include insertion loss, 0 dB setting
power_list_dBm = np.linspace(POWER_STOP, POWER_START, nSteps)
marker1 = np.zeros(nSteps)

f_marker1_Hz = pxa.getMarkFreq_Hz(1)

idx = 0
print("Estimated time to take data: {} Minutes".format(nSteps*WAIT_BETWEEN_STEPS_S/60.0))
while (idx < nSteps):
    print("IDX : {}, atten_stim : {}".format(idx, np.round(power_list_dBm[idx], 2)))
    # set Power of CW tone
    synth.setPowerdBm(np.round(power_list_dBm[idx], 2))
    time.sleep(WAIT_BETWEEN_STEPS_S)
    marker1[idx] = pxa.getMarkPower(1)
    idx += 1

'''Serial number_IIP3_{UP_mix|DN_Mix}-{Measured port BB|RF}'''
np.savez_compressed("ipx_data/Power_List_2022-10-12_1639", 
                    nSteps = nSteps,
                    power_list_dBm = power_list_dBm,
                    marker1 = marker1,
                    f_marker1_Hz = f_marker1_Hz,
                    WAIT_BETWEEN_STEPS_S = WAIT_BETWEEN_STEPS_S,
                    cables = "INPUT : None, OUTPUT : CableA",
                    )

