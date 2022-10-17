# -*- coding: utf-8 -*-

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
pl.title("Baseband Loopback Pass Response")
pl.xlabel("Frequency [MHz]")
pl.ylabel("Output Power [dBc]")
pl.xlim(0, 1000)
pl.ylim(-1.0, -0.3)
pl.legend()


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

freqs_s11 = f_s11_lb["freqs"]
power_s11 = f_s11_lb["data"]
freqs_s22 = f_s22_lb["freqs"]
power_s22 = f_s22_lb["data"]
# freqs_s33 = f_s33_lb["freqs"]
# power_s33 = f_s33_lb["data"]
# freqs_s44 = f_s44_lb["freqs"]
# power_s44 = f_s44_lb["data"]
plot_st_idx = 10
plot_ep_idx = np.absolute(freqs_s31-1e9).argmin()

pl.figure()
pl.plot(freqs_s11[plot_st_idx:plot_ep_idx]/1e6, power_s11[plot_st_idx:plot_ep_idx], label="s11")
pl.plot(freqs_s22[plot_st_idx:plot_ep_idx]/1e6, power_s22[plot_st_idx:plot_ep_idx], label="s22")
# pl.plot(freqs_s33[plot_st_idx:plot_ep_idx]/1e6, power_s33[plot_st_idx:plot_ep_idx])
# pl.plot(freqs_s44[plot_st_idx:plot_ep_idx]/1e6, power_s44[plot_st_idx:plot_ep_idx])
pl.title("Baseband Loopback Matching")
pl.xlim(0, 1000)
pl.ylim(-31.0, -25.0)
pl.xlabel("Frequency [MHz]")
pl.ylabel("Output Power [dBc]")
pl.legend()

