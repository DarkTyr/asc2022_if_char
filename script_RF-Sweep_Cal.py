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
SYNTH0_COM_PORT = "COM16"
SYNTH1_COM_PORT = "COM17"
ENA_IP = "192.168.0.15"
PXA_IP = "192.168.0.16"

WAIT_BETWEEN_STEPS_S = 0.20
FREQ_START_HZ = 4e9
FREQ_STOP_HZ = 5e9
FREQ_STEP_SIZE_HZ = 1e6
rm = pyvisa.ResourceManager()
pxa = keysight_pxa_eth.Keysight_PXA_Eth(rm, resource_name="TCPIP::{}::inst0::INSTR".format(PXA_IP))
pxa.open()

synth0 = phasematrix_serial.PhaseMatrix_Serial(port=SYNTH0_COM_PORT)
synth1 = phasematrix_serial.PhaseMatrix_Serial(port=SYNTH1_COM_PORT)
synth0.open()
synth1.open()

'''

'''

nSteps = int(np.absolute(FREQ_STOP_HZ - FREQ_START_HZ)/FREQ_STEP_SIZE_HZ + 1)    # Add 1 to include insertion loss, 0 dB setting
freq_list_Hz = np.linspace(FREQ_START_HZ, FREQ_STOP_HZ, nSteps)
pxa.setNumberPoints(nSteps)
pxa.setStartFrequnecy_Hz(FREQ_START_HZ)
pxa.setStopFrequency_Hz(FREQ_STOP_HZ)

idx = 0
print("Estimated time to take data: {} Minutes".format(nSteps*WAIT_BETWEEN_STEPS_S/60.0))
print("IDX : {}, freq : {} MHz".format(idx, freq_list_Hz[idx]/1e6))
while (idx < nSteps):
    if((idx % 50) == False):
        print("IDX : {}, freq : {} MHz".format(idx, freq_list_Hz[idx]/1e6))
    synth1.setFrequencyHz(freq_list_Hz[idx])
    time.sleep(WAIT_BETWEEN_STEPS_S)
    idx += 1

power_list_dBm = pxa.getData(1)

'''Serial number_IIP3_{UP_mix|DN_Mix}-{Measured port BB|RF}'''
np.savez_compressed("cal_data/Power_Cal_IQ_2022-10-14_1205", 
                    power_list_dBm = power_list_dBm,
                    nSteps = nSteps,
                    freq_list_Hz = freq_list_Hz,                    
                    WAIT_BETWEEN_STEPS_S = WAIT_BETWEEN_STEPS_S,
                    FREQ_START_HZ = FREQ_START_HZ,
                    FREQ_STOP_HZ = FREQ_STOP_HZ,
                    FREQ_STEP_SIZE_HZ = FREQ_STEP_SIZE_HZ
                    )

