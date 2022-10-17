# -*- coding: utf-8 -*-

from cProfile import label
from matplotlib.pyplot import plot
import pylab as pl
pl.ion()
import numpy as np
import db_math


'''
port 1 = DAC0
port 2 = DAC1
port 3 = ADC0
port 4 = ADC1
port 5 = UP-MIX RF
port 6 = DN-MIZ RF

'''

'''
Baseband Loopback Pass through response
'''
F_S31_BB_LB = "s_data/SN020L_S31_BB_Loopback_4p5GHz.npz"
F_S42_BB_LB = "s_data/SN020L_S42_BB_Loopback_4p5GHz.npz"

f_s31_lb = np.load(F_S31_BB_LB)
f_s42_lb = np.load(F_S42_BB_LB)

freqs_s31 = f_s31_lb["freqs"]
power_s31 = f_s31_lb["data"]
freqs_s42 = f_s42_lb["freqs"]
power_s42 = f_s42_lb["data"]
plot_st_idx = 10
plot_ep_idx = np.absolute(freqs_s31-1e9).argmin()

pl.figure()
pl.plot(freqs_s31[plot_st_idx:plot_ep_idx]/1e6, power_s31[plot_st_idx:plot_ep_idx], label="s31")
pl.plot(freqs_s42[plot_st_idx:plot_ep_idx]/1e6, power_s42[plot_st_idx:plot_ep_idx], label="s42")
pl.title("Baseband Loopback Pass Response", fontsize=28)
pl.xlabel("Frequency [MHz]", fontsize=20)
pl.ylabel("Output Power [dBc]", fontsize=20)
pl.xlim(0, 1000)
pl.ylim(-1.0, -0.3)
pl.legend(fontsize=18)


'''
Baseband Loopback S11 and like responses 
'''
F_S11_BB_LB = "s_data/SN020L_S11_BB_Loopback_4p5GHz.npz"
F_S22_BB_LB = "s_data/SN020L_S22_BB_Loopback_4p5GHz.npz"
# F_S33_BB_LB = "s_data/SN020L_S33_BB_Loopback_4p5GHz.npz" # Didn't save the data
# F_S44_BB_LB = "s_data/SN020L_S44_BB_Loopback_4p5GHz.npz" # Didn't save the data

f_s11_lb = np.load(F_S11_BB_LB)
f_s22_lb = np.load(F_S22_BB_LB)
# f_s33_lb = np.load(F_S33_BB_LB)
# f_s44_lb = np.load(F_S33_BB_LB)

freqs_s11_lb = f_s11_lb["freqs"]
power_s11_lb = f_s11_lb["data"]
freqs_s22_lb = f_s22_lb["freqs"]
power_s22_lb = f_s22_lb["data"]
# freqs_s33 = f_s33_lb["freqs"]
# power_s33 = f_s33_lb["data"]
# freqs_s44 = f_s44_lb["freqs"]
# power_s44 = f_s44_lb["data"]
plot_st_idx = 10
plot_ep_idx = np.absolute(freqs_s31-1e9).argmin()

pl.figure()
pl.plot(freqs_s11_lb[plot_st_idx:plot_ep_idx]/1e6, power_s11_lb[plot_st_idx:plot_ep_idx], label="s11")
pl.plot(freqs_s22_lb[plot_st_idx:plot_ep_idx]/1e6, power_s22_lb[plot_st_idx:plot_ep_idx], label="s22")
# pl.plot(freqs_s33[plot_st_idx:plot_ep_idx]/1e6, power_s33[plot_st_idx:plot_ep_idx])
# pl.plot(freqs_s44[plot_st_idx:plot_ep_idx]/1e6, power_s44[plot_st_idx:plot_ep_idx])
pl.title("Baseband Loopback Matching", fontsize=28)
pl.xlim(0, 1000)
pl.ylim(-31.0, -25.0)
pl.xlabel("Frequency [MHz]", fontsize=20)
pl.ylabel("Output Power [dBc]", fontsize=20)
pl.legend(fontsize=18)


'''
Baseband Loopback S11 and like responses 
'''
F_S11_BB_4p5 = "s_data/SN020L_S11_rf_50ohm_4p5GHz.npz"
F_S22_BB_4p5 = "s_data/SN020L_S22_rf_50ohm_4p5GHz.npz"
f_s11_bb_4p5 = np.load(F_S11_BB_4p5)
f_s22_bb_4p5 = np.load(F_S22_BB_4p5)

freqs_s11_4p5 = f_s11_bb_4p5["freqs"]
power_s11_4p5 = f_s11_bb_4p5["data"]
freqs_s22_4p5 = f_s22_bb_4p5["freqs"]
power_s22_4p5 = f_s22_bb_4p5["data"]
plot_st_idx = 10
plot_ep_idx = np.absolute(freqs_s11_4p5-1e9).argmin()

pl.figure()
pl.plot(freqs_s11_4p5[plot_st_idx:plot_ep_idx]/1e6, power_s11_4p5[plot_st_idx:plot_ep_idx], label="s11")
pl.plot(freqs_s22_4p5[plot_st_idx:plot_ep_idx]/1e6, power_s22_4p5[plot_st_idx:plot_ep_idx], label="s22")
pl.title("Baseband Matching, Up-Mix, RF port 50 OHm terminated", fontsize=28)
pl.xlim(0, 1000)
# pl.ylim(-31.0, -25.0)
pl.xlabel("Frequency [MHz]", fontsize=20)
pl.ylabel("Output Power [dBc]", fontsize=20)
pl.legend(fontsize=18)


'''
RF Snn responses vs F_LO
'''

F_S55_rf_4p5 = "s_data/SN013L_S55_rf_bbterm_4p5GHz.npz"
F_S66_rf_4p5 = "s_data/SN013L_S66_rf_bbterm_4p5GHz.npz"
F_S55_rf_5p5 = "s_data/SN013L_S55_rf_bbterm_5p5GHz.npz"
F_S66_rf_5p5 = "s_data/SN013L_S66_rf_bbterm_5p5GHz.npz"

f_s55_rf_4p5 = np.load(F_S55_rf_4p5)
f_s66_rf_4p5 = np.load(F_S66_rf_4p5)
f_s55_rf_5p5 = np.load(F_S55_rf_5p5)
f_s66_rf_5p5 = np.load(F_S66_rf_5p5)


freqs_s55_4p5 = f_s55_rf_4p5["freqs"]
power_s55_4p5 = f_s55_rf_4p5["data"]
freqs_s66_4p5 = f_s66_rf_4p5["freqs"]
power_s66_4p5 = f_s66_rf_4p5["data"]
freqs_s55_5p5 = f_s55_rf_5p5["freqs"]
power_s55_5p5 = f_s55_rf_5p5["data"]
freqs_s66_5p5 = f_s66_rf_5p5["freqs"]
power_s66_5p5 = f_s66_rf_5p5["data"]

pl.figure()
pl.plot(freqs_s55_4p5/1e6, power_s55_4p5, label="S55_4p5 GHz")
pl.plot(freqs_s66_4p5/1e6, power_s66_4p5, label="S66_4p5 GHz")
pl.title("RF Snn Matching vs F_LO", fontsize=28)
pl.xlim(3200, 5200)
# pl.ylim(-31.0, -25.0)
pl.xlabel("Frequency [MHz]", fontsize=20)
pl.ylabel("Power [dB]", fontsize=20)
pl.legend(fontsize=18)
