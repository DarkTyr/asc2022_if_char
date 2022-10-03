# -*- coding: utf-8 -*-
'''
Module Keysight_PXA_Eth
=================================
This module is responsible for communicating with the Keysight PXA Signal Analyzer over
Ethernet using the pyvisa infrastructure. 
'''
# System level imports
import pyvisa
import numpy as np
import pylab as pl
pl.ion()

# local imports
import adaura_4chan_attenuator_usb as adaura
import keysight_ena_eth

'''In the future make these passable by command line interfaces, for now hard code is fine'''
ATTEN_COM_PORT = "COM11"
ENA_IP = "192.168.0.15"
ATTEN_START = 0.0
ATTEN_STOP = 50
ATTEN_STEP_SIZE = 0.25
FREQ_INDEX_START = 1111

rm = pyvisa.ResourceManager()
ena = keysight_ena_eth.Keysight_ENA_Eth(rm, resource_name="TCPIP::{}::inst0::INSTR".format(ENA_IP))
ena.open()

'''
Some notes:
The user is expected to have connected the ENA to the attenuator channels you want to calibrate
and configured trace 1 as the first channels and trace 2 and the seconds channels

'''

att = adaura.Adaura_4Chan_Attenuator_USB(ATTEN_COM_PORT)

nSteps = int((ATTEN_STOP - ATTEN_START)/ATTEN_STEP_SIZE + 1)
nPoints_ENA = int(ena.getNumberPoints())
measured_attenuations_chan1 = np.zeros((nSteps,nPoints_ENA))
measured_attenuations_chan2 = np.zeros((nSteps,nPoints_ENA))
freqs_Hz = ena.getXValues_Hz()
att_step_value = np.linspace(ATTEN_START, ATTEN_STOP, nSteps)

for i in range(nSteps):
    print("Measuring Step {} out of {}".format(i, nSteps))
    att.set_all_atten(att_step_value[i])
    ena.setAverageReset()
    ena.triggerSweepAverage()
    measured_attenuations_chan1[i] = ena.getFormattedData(1)
    measured_attenuations_chan2[i] = ena.getFormattedData(2)
    
print("Complete")

pl.figure()
for i in range(nSteps):
    pl.plot(freqs_Hz[FREQ_INDEX_START:]/1e6, measured_attenuations_chan1[i][FREQ_INDEX_START:])

pl.figure()
for i in range(nSteps):
    pl.plot(freqs_Hz[FREQ_INDEX_START:]/1e6, measured_attenuations_chan2[i][FREQ_INDEX_START:])

np.savez_compressed("cal_data/adaura_Channel1_Cal",
                    channel=1, 
                    nSteps=nSteps, 
                    nPoints_ENA=nPoints_ENA, 
                    measured_attenuations_chan=measured_attenuations_chan1, 
                    freqs_Hz=freqs_Hz, 
                    att_step_value=att_step_value)

np.savez_compressed("cal_data/adaura_Channel2_Cal",
                    channel=2, 
                    nSteps=nSteps, 
                    nPoints_ENA=nPoints_ENA, 
                    measured_attenuations_chan=measured_attenuations_chan2, 
                    freqs_Hz=freqs_Hz, 
                    att_step_value=att_step_value)
                

