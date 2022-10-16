# -*- coding: utf-8 -*-

import pylab as pl
pl.ion()
import numpy as np
import load_cable_atten

F_NATURAL_IMAGE = "s_data/SN0013_Natural_Image_supression_4p5GHz_0p5scale_tone.npz"
F_IF_CALIBRATION = "if_calib/687Colossus/SN0013_4p5GHz/calib.npz"
F_DAC_CAL = "cal_data/dac_cal.npz"
F_CAL_CABLEA = "cal_data/cableA.npz"
F_CAL_CABLEB = "cal_data/cableB.npz"
F_CAL_CABLEC = "cal_data/cableC.npz"

atten_cableA = load_cable_atten.Load_Cable_Atten(F_CAL_CABLEA)
atten_cableB = load_cable_atten.Load_Cable_Atten(F_CAL_CABLEB)
atten_cableC = load_cable_atten.Load_Cable_Atten(F_CAL_CABLEC)

# Lets load up the Abaco calibration
if_calib = np.load(F_IF_CALIBRATION)
calib_freqs = if_calib["calib_freq_hz"]
calib_offset_deg = if_calib["iq_offset_deg"]
calib_power_dBm = if_calib["power_rf"]
calib_image_dBm = if_calib["power_im"]

# Fix center zero freq and set to next
calib_power_dBm[48] = calib_power_dBm[47]
calib_image_dBm[48] = calib_image_dBm[47]

post_calib_power_dBm = np.zeros_like(calib_power_dBm)
post_calib_image_dBm = np.zeros_like(calib_image_dBm)

for idx in range(len(calib_freqs)):
    freq = calib_freqs[idx]
    if(freq == 0):
        freq = 0.5
    post_calib_power_dBm[idx] = calib_power_dBm[idx] - atten_cableA.real_atten_avg(4.5e9 + freq, 10)
    post_calib_image_dBm[idx] = calib_image_dBm[idx] - atten_cableA.real_atten_avg(4.5e9 + freq, 10)



# pl.title("IF Calibration - Imagine Tone Power (RF)")
# pl.xlabel("Frequency [MHz]")
# pl.ylabel("Output Power [dBm]")

'''TODO: Natural Image Tone supression and power on the IF_Calibration plot'''
f_natural = np.load(F_NATURAL_IMAGE)
f_natural_keys = list(f_natural.keys())
nat_freq_start = f_natural["freq_start"]
nat_freq_stop = f_natural["freq_stop"]
nat_npoints = f_natural["npoints"]
nat_lower_sweep = f_natural["data_lower_band"]
nat_upper_sweep = f_natural["data_upper_band"]
# manipulate data
nat_freq_x = np.linspace(nat_freq_start, nat_freq_stop, nat_npoints) - 4.5e9
nat_im_flip = nat_lower_sweep
nat_im_flip[0:500] = np.flip(nat_lower_sweep[501:])
nat_im_flip[501:] = np.flip(nat_upper_sweep[0:500])
# Remove cable attenuation
for idx in range(len(nat_freq_x)):
    freq_MHz = np.absolute(nat_freq_x[idx])
    if(freq_MHz == 0):
        freq_MHz = 0.5
    nat_im_flip[idx] -= atten_cableA.real_atten_avg(freq_MHz*1e6, 4)
# Make the plot
pl.figure()
pl.plot(calib_freqs/1e6, post_calib_power_dBm, label="Tone Power")
pl.plot(nat_freq_x/1e6, nat_im_flip-12.46, label="Natural Image Supression")
pl.plot(calib_freqs/1e6, post_calib_image_dBm, label="Image After Angle Cal")
pl.title("IF Calibration - Power (RF, $f_{LO}$=4.5GHz)")
pl.xlabel("Frequency [MHz]")
pl.ylabel("RF Power [dBm]")
pl.xlim(-480, 480)
pl.legend()

