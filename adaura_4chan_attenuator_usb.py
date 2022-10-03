# -*- coding: utf-8 -*-
'''
Module Adaura_4Chan_Attenuator_USB
=================================
This module is responsible for communicating the Adaura 4 Channel USB Attenuator. 
As of this writing there is no way to ask what the current attenuation value is
set to. 
'''
# System level imports
import serial
import time

# local imports

class Adaura_4Chan_Attenuator_USB:
    def __init__(self, port=''):
        if(port == ''):
            raise IOError("There is no default serial com port, user must tell Base_Board_Rev3 what port to use")
        self.port = port    # Serial port we are supposed to communicate with
        self.com = serial.Serial(port=self.port, timeout=6, write_timeout=6) # PySerial object
        self.debug = True
        self._sent_str = ''
        self._ret_str = ''
        self._read_delay_s = 0.001
        self.device_info = ''
        self._attenuation_resolution = 0.25
        
    def _write(self, str_in: str):
        if(self.debug):
            print("Adaura_4Chan_Attenuator_USB._write()")
        self._sent_str = str_in
        if(self.debug):
            print("  Sent CMD : {}".format(self._sent_str))
        self.com.write(self._sent_str.encode())
        time.sleep(self._read_delay_s)
        self._ret_str = self.com.read_all().decode("utf-8")
        if(self.debug):
            print("  Response : {}".format(self._ret_str))
        
    def _read(self) -> str:
        return " "
    
    def open(self):
        '''Open the serial port'''
        self.com.open()

    def close(self):
        '''Close the serial port'''
        self.com.close()

    def info(self, print_out=False):
        self._write("info")
        self.device_info = self._ret_str
        if(print_out):
            print(self.device_info)

    def set_atten(self, chan, atten_dB):
        if(chan < 1):
            print("Invalid channel number, must be 1, 2, 3, 4")
            return
        if(chan > 4):
            print("Invalid channel number, must be 1, 2, 3, 4")
            return
        
        if((atten_dB % self._attenuation_resolution) != 0.0):
            print("Requested attenuation must be modulo {}".format(str(self._attenuation_resolution)))

        self._write("SET {} {}".format(chan, atten_dB))
        #TODO: Parse Return string and see if the command was valid
        return

    def set_all_atten(self, atten_dB):
        if((atten_dB % self._attenuation_resolution) != 0.0):
            print("Requested attenuation must be modulo {}".format(str(self._attenuation_resolution)))

        self._write("SAA {}".format(atten_dB))
        #TODO: Parse Return string and see if the command was valid
        return

    def get_atten(self, chan) -> float:
        raise IOError("Currently Can't ask for the current attenuation value")
        return

    