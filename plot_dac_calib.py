# -*- coding: utf-8 -*-

import pylab as pl
pl.ion()
import numpy as np
import load_cable_atten
import db_math


F_IF_CALIBRATION = "if_calib/687Colossus/SN0013_4p5GHz/calib.npz"
F_DAC_CAL = "cal_data/dac_cal.npz"
F_CAL_CABLEA = "cal_data/cableA.npz"
F_CAL_CABLEB = "cal_data/cableB.npz"
F_CAL_CABLEC = "cal_data/cableC.npz"

atten_cableA = load_cable_atten.Load_Cable_Atten(F_CAL_CABLEA)
atten_cableB = load_cable_atten.Load_Cable_Atten(F_CAL_CABLEB)
atten_cableC = load_cable_atten.Load_Cable_Atten(F_CAL_CABLEC)

dac_cal = np.load(F_DAC_CAL)
dac0 = dac_cal["data_dac0"]
dac1 = dac_cal["data_dac1"]
dac_freqs = np.linspace(dac_cal["freq_start"], dac_cal["freq_stop"], dac_cal["npoints"]+1)[1:]
dac_plot_start = 4

# Subtract out the frequency dependent cable attenuation
for x in range(len(dac_freqs)):
    dac0[x] -= atten_cableA.real_atten_avg(dac_freqs[x], 4)
    dac1[x] -= atten_cableA.real_atten_avg(dac_freqs[x], 4)

# Make a plot of this data
fig1 = pl.figure(1)
frame1 = fig1.add_axes((0.1, 0.3, 0.8, 0.6))
pl.plot(dac_freqs[dac_plot_start:]/1e6, dac0[dac_plot_start:], label="DAC0")
pl.plot(dac_freqs[dac_plot_start:]/1e6, dac1[dac_plot_start:], label="DAC1")
pl.title("DAC Responses vs Freq (Half Scale)", fontsize=28)
# xlabel on frame2
pl.ylabel("Output Power [dBm]", fontsize=20)
pl.xlim(6, 490)
pl.ylim(-10, 0)
pl.legend(fontsize=18)

# pl.grid()
frame2 = fig1.add_axes((0.1, 0.1, 0.8, 0.2))
dac_diff = 10*np.log10(db_math.dBm_mW(dac1[dac_plot_start:]) / db_math.dBm_mW(dac0[dac_plot_start:]))
pl.plot(dac_freqs[dac_plot_start:]/1e6, dac_diff)
pl.xlim(6, 490)
pl.ylim(-0.1, -0.025)
pl.xlabel("Frequency [MHz]", fontsize=20)
pl.ylabel("Output Power [dBc]", fontsize=20)
pl.grid()
