'''
https://www.geeksforgeeks.org/find-the-nearest-value-and-the-index-of-numpy-array/#:~:text=The%20approach%20to%20finding%20the%20nearest%20value%20and,values%20in%20a%20difference%20array%2C%20say%20difference_array%20%5B%5D.

The link above seems to work when given a desired frequency and trying to determine the attnuation from the dark blue cable
or the real attenuation for the digital attenuator. 
'''

'''
Step Zero:
Figure out the optimal power for the inout of the PXA believed to be between -30dBm to -40dBm. Now the question is should we add attenuation
achieve this power level or change the digital attenuator to achieve this. I think add an attenuator to achieve this.

Assumed uMux_IF conversion loss is -5dB, digital attenuator insertion loss is -7dB, Blue cable -1.2, braided cable (TBD) -1.0
which yields about -14.2 attenuation between stimulus and PXA, this means will will need a bit of added (calibrated) attenuation
between the uMux_IF out and PXA. When doing the Down Mix there is a gain of about 10dB versus a loss of -5dB which means more will 
need to be added between the IF and PXA.

'''

'''
Step one:
Record the quality of the applied stimulus signal and IMD3 peaks. The IMD3 powers will need to be subtracted from the final results.
Same applies to the IMD2 component as well (2F_0 is all we care about). 
'''

'''
Step two:
Connect the IF_Board to the output of the attenuator and connect the desired port (I/Q labeld 1 or 2) to the attenuator with the 
braided cable. Then connect the dark blue cable to between the attenuator output and the PXA. For accurate results we will need 
to subtract out both the dark blue cable and braided cable losses. Will also haec to apply the mapping between attenuator setting 
real attenuation. 
'''

'''
Step three:
Start with stimulus channel of the Digital attenuator at a reasonable value (-50dB) and the other channel at zero dB setting (Intertion loss)
For each itteration grab the key values that we care about. IMD3 and IMD2. Then adjust the stimulus channel up by 0.25 dB and PXA measurement
channel down by 0.25dB. The idea here is to maintain the same incident power on the PXA.
'''

'''
Step four:
post calculations to compensate for the cable losses and Insertion losses of the sigital attenuators. We need the 
actuall incident power on the IF board and the actuall output power from the IF board. Final step is to subtract the stimulus products
from the measured results. This wont make a difference at hgiher powers but "should" clean up the lower power data and have it 
not look so funky and bad. I will have to work in the lab to actually determine if this is possible. Maybe will need to the data to be
post digital attenuator and have the attenuator at the highest desired attenuation level.
'''
