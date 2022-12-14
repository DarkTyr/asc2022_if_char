'''
Copy and paste Prototypes for use with iPython. 
'''
import pyvisa
import numpy as np
import pylab as pl
pl.ion()
import adaura_4chan_attenuator_usb as adaura
import keysight_ena_eth
import keysight_pxa_eth

ENA_IP = "192.168.0.15"
PXA_IP = "192.168.0.16"

PORT_SYNTH0 = "COM11"
PORT_SYNTH1 = "COM10"
PORT_ATT = "COM13"
port_ena = "TCPIP::{}::inst0::INSTR".format(ENA_IP)
port_pxa = "TCPIP::{}::inst0::INSTR".format(PXA_IP)


att = adaura.Adaura_4Chan_Attenuator_USB(port=PORT_ATT)
rm = pyvisa.ResourceManager()
ena = keysight_ena_eth.Keysight_ENA_Eth(rm, resource_name=port_ena)
ena.open()
ena.ena.timeout=30000 # ms is the unit  

pxa = keysight_pxa_eth.Keysight_PXA_Eth(rm, resource_name=port_pxa)


freqs = ena.getXValues_Hz()
data_s11 = ena.getFormattedData(1)
data_s22 = ena.getFormattedData(2)
# data_s32 = ena.getFormattedData(3)
# data_s41 = ena.getFormattedData(4)
# data_s12 = ena.getFormattedData(5)
# data_s11 = ena.getFormattedData(6)
# data_s22 = ena.getFormattedData(7)
np.savez_compressed("s_data/SN013L_S55_rf_bbterm_5p5GHz", freqs = freqs, data=data_s11)
np.savez_compressed("s_data/SN013L_S66_rf_bbterm_5p5GHz", freqs = freqs, data=data_s22)
np.savez_compressed("s_data/SN020L_S32_rf_Loopback_4p5GHz", freqs = freqs, data=data_s32)
np.savez_compressed("s_data/SN020L_S41_rf_Loopback_4p5GHz", freqs = freqs, data=data_s41)
np.savez_compressed("s_data/SN020L_S12_rf_Loopback_4p5GHz", freqs = freqs, data=data_s12)
np.savez_compressed("s_data/SN020L_S11_rf_Loopback_4p5GHz", freqs = freqs, data=data_s11)
np.savez_compressed("s_data/SN020L_S22_rf_Loopback_4p5GHz", freqs = freqs, data=data_s22)




data_lower_band = pxa.getData(2)
data_upper_band = pxa.getData(3)
freq_start = pxa.getStartFrequency_Hz()
freq_stop = pxa.getStopFrequency_Hz()
npoints = pxa.getNumberPoints()
power_scale = 0.5 # DAC amplitude

np.savez_compressed("cal_data/SN0013_Natural_Image_supression_5p5GHz_0p5scale_tone", 
                    data_lower_band = data_lower_band,
                    data_upper_band = data_upper_band,
                    freq_start = freq_start,
                    freq_stop = freq_stop,
                    npoints = npoints,
                    power_scale = power_scale,
                    notes="Matches the DAC power CAL that was taken"
                    )