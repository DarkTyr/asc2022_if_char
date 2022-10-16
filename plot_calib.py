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
pl.title("DAC Response vs Freq (@Half Scale)")
pl.xlabel("Frequency [MHz]")
pl.ylabel("Output Power [dBm]")
pl.xlim(6, 490)
pl.ylim(-10, 0)
pl.legend()

pl.grid()
frame2 = fig1.add_axes((0.1, 0.1, 0.8, 0.2))
dac_diff1 = dac0[dac_plot_start:] - dac1[dac_plot_start:]
dac_diff2 = db_math.mW_dBm(db_math.dBm_mW(dac0[dac_plot_start:]) - db_math.dBm_mW(dac1[dac_plot_start:]))
# pl.plot(dac_freqs[dac_plot_start:]/1e6, dac_diff1)
pl.plot(dac_freqs[dac_plot_start:]/1e6, dac_diff2)
pl.xlim(6, 490)
pl.ylim(-30, -10)
pl.grid()

# Lets load up the Abaco calibration
if_calib = np.load(F_IF_CALIBRATION)
calib_freqs = if_calib["calib_freq_hz"]
calib_offset_deg = if_calib["iq_offset_deg"]
calib_power_dBm = if_calib["power_rf"]
calib_image_dBm = if_calib["power_im"]

# Fix center zero freq and set to next
# calib_power_dBm[48] = calib_power_dBm[47]
# calib_image_dBm[48] = calib_image_dBm[47]

post_calib_power_dBm = np.zeros_like(calib_power_dBm)
post_calib_image_dBm = np.zeros_like(calib_image_dBm)

for idx in range(len(calib_freqs)):
    freq = calib_freqs[idx]
    dac_idx = np.absolute(dac_freqs - freq).argmin()
    post_calib_power_dBm[idx] = calib_power_dBm[idx] - atten_cableA.real_atten_avg(4.5e9 + freq, 10)
    post_calib_image_dBm[idx] = calib_image_dBm[idx] - atten_cableA.real_atten_avg(4.5e9 + freq, 10)

pl.figure()
pl.plot(calib_freqs/1e6, post_calib_power_dBm, label="Tone")
pl.plot(calib_freqs/1e6, post_calib_image_dBm, label="Image")
pl.title("IF Calibration - Power (RF)")
pl.xlabel("Frequency [MHz]")
pl.ylabel("RF Power [dBm]")
pl.xlim(-480, 480)
pl.legend()

# pl.title("IF Calibration - Imagine Tone Power (RF)")
# pl.xlabel("Frequency [MHz]")
# pl.ylabel("Output Power [dBm]")

