import numpy as np

class Load_Cable_Atten():
    def __init__(self, f_name:str):
        self.debug = False
        self.fname = f_name
        self.data = np.load(self.fname)
        self.keys = list(self.data.keys())
        self.freqs_Hz = self.data["freqs"]
        self.all_data = self.data["data"]     

    def _nearest_frequency_Hz(self, desired_freqeucy_Hz:float) -> int:
        ''' Returns the freq index that is closest to the desired frequency'''
        diff_array = np.absolute(self.freqs_Hz - desired_freqeucy_Hz)
        idx = diff_array.argmin()
        if(self.debug):
            print("Load_Atten_Cal._nearest_frequency_Hz():{} Hz".format(desired_freqeucy_Hz))
            print("  Found nearest Frequency : {} Hz".format(self.freqs_Hz[idx]))
            print("  IDX : {}".format(idx))
        '''Pretty simple once you think about it but the code is reference and soured from:
        https://www.geeksforgeeks.org/find-the-nearest-value-and-the-index-of-numpy-array/#:~:text=The%20approach%20to%20finding%20the%20nearest%20value%20and,values%20in%20a%20difference%20array%2C%20say%20difference_array%20%5B%5D.
        '''
        return int(idx)
    
    def real_atten(self, desired_freq_Hz:float) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        real_atten_dB = self.all_data[freq_idx]
        return real_atten_dB

    def real_atten_avg(self, desired_freq_Hz:float, avg_width=10) -> float:
        freq_idx = self._nearest_frequency_Hz(desired_freq_Hz)
        real_atten_dB = np.average(self.all_data[freq_idx-avg_width:freq_idx+avg_width+1])
        return real_atten_dB

    def plot_cable_atten(self):
        import pylab as pl
        pl.ion()
        pl.plot(self.freq_Hz/1e6, self.all_data)
        pl.title("Cable Attenuation : {}".format(self.fname))
        pl.xlabel("Frequency [MHz]")
        pl.ylabel("Power [dB]")
    
    