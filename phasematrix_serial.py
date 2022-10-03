# -*- coding: utf-8 -*-
'''
Module PhaseMatrix_Serial
=================================
This module is responsible for communicating with NI QuickSyn Synthesizer.
It can be either the Full features on or Lite version. Just note that the Lite
version ignores the RF power parameter and can't do any fancy modulations or
sweeps. Current this class allows basic control for generating a CW sine wave
and there are no error checks. 
'''
# System level imports
import serial

class PhaseMatrix_Serial():
    def __init__(self, port=""):
        if(port == ""):
            raise IOError("There is no default serial com port, user must tell PhaseMatrix_Serial what port to use")
        self.IDN = ""
        self.port = port
        self._term = "\n"
        self.com = None
        self._sent_str = ""
        self._ret_str = ""
        
    def open(self):
        if(self.com):
            self.com.close()
        self.com = serial.Serial(port=self.port, timeout=10)

    def close(self):
        self.com.close()

    def getIdentity(self):
        self.IDN = self.query("*IDN?")
        return(self.IDN)

    def _write(self, cmd):
        self._sent_str = cmd + self._term
        self.com.write(self._sent_str)
        self._ret_str = self.com.read_until()
        return (self._ret_str)

    def _query(self, cmd):
        self._sent_str = cmd + self._term
        self.com.write(self._sent_str)
        self._ret_str = self.serial.readline()
        result = self._ret_str.split("\n")[0]
        return result

    def setFrequencyGHz(self, frequency_GHz):
        ''' Set the microwave frequency in GHz.'''
        freq_mHertz = frequency_GHz * 1e9 * 1e3 # Convert to Hz then mHz
        commandstring = "FREQ " + str(freq_mHertz)
        #QuickSyn units are milli-Hertz
        self._write(commandstring)

    def getFrequencyGHz(self) -> float:
        ''' Get the microwave frequency.'''
        response = self.query("FREQ?")
        # Response is in mHz
        freq_GHz = float(response) / 1e9 / 1e3
        return freq_GHz
    
    def setFrequencyMHz(self, frequency_GHz):
        ''' Set the microwave frequency in GHz.'''
        freq_mHertz = frequency_GHz * 1e6 * 1e3 # Convert to Hz then mHz
        commandstring = "FREQ " + str(freq_mHertz)
        #QuickSyn units are milli-Hertz
        self._write(commandstring)

    def getFrequencyMHz(self) -> float:
        ''' Get the microwave frequency.'''
        response = self.query("FREQ?")
        # Response is in mHz
        freq_GHz = float(response) / 1e6 / 1e3
        return freq_GHz

    def setFrequencyHz(self, frequency_GHz):
        ''' Set the microwave frequency in GHz.'''
        freq_mHertz = frequency_GHz * 1e3 # Convert to Hz then mHz
        commandstring = "FREQ " + str(freq_mHertz)
        #QuickSyn units are milli-Hertz
        self._write(commandstring)

    def getFrequencyHz(self) -> float:
        ''' Get the microwave frequency.'''
        response = self.query("FREQ?")
        # Response is in mHz
        freq_GHz = float(response) / 1e3
        return freq_GHz

    def setPowerdBm(self, power_dBm):
        ''' Set the microwave power in dBm.'''
        self._write("POW {}".format(str(power_dBm)))

    def getPowerdBm(self) -> float:
        ''' Get the microwave power.'''
        ret = self.query("POW?")
        pow = float(ret)
        return pow

    def setRefSourceInternal(self):
        self._write("ROSC:SOUR INT")

    def setRefSourceExternal(self):
        self._write("ROSC:SOUR EXT")

    def getRefSource(self):
        ret = self._query("ROSC:SOUR?")
        return ret

    def setRefOutputOn(self):
        self._write("OUTP:ROSC:STAT ON")

    def setRefOutputOff(self):
        self._write("OUTP:ROSC:STAT OFF")

    def setOutputStatusON(self):
        self._write("OUTP:STAT ON")

    def setOutputStatusOff(self):
        self._write("OUTP:STAT OFF")

    def getOutputStatus(self):
        ret = self._query("OUTP:STAT?")
        return ret

    def setSaveCurrentStateFlash1(self):
        self._write("*SAV 1")

    def setSaveCurrentStateFlash2(self):
        self._write("*SAV 2")

    def setRecalFlashState(self, state:int):
        if(state < 0):
            print("Invalid FlashState, must be 0 to 2")
        if(state > 2):
            print("Invalid FlashState, must be 0 to 2")
        
        if(state == 0):
            print("Recalling Factory Defaults, flash state 0")
            self._write("*RCL 0")
        elif(state == 1):
            print("Recalling User Flash State 1")
            self._write("*RCL 1")
        else:
            print("Recalling User Flash State 2")
            self._write("*RCL 2")
    
    def getStatus(self, print_console=True):
        stat = self._query("STAT?")
        if(print_console):
            print("QuickSyn Status:")
            if(stat & 0x01):
                print("  External Reference")
            else:
                print("  No External Reference")

            if(stat & 0x02):
                print("  RF Unlocked")
            else:
                print("  RF Locked")
            
            if(stat & 0x04):
                print("  Reference Unlocked")
            else:
                print("  Reference Locked")

            if(stat & 0x08):
                print("  RF Output ON")
            else:
                print("  RF Output Off")

            if(stat & 0x10):
                print("  Voltage Error")
            else:
                print("  Voltage Okay")

            if(stat & 0x20):
                print("  Reference Output on")
            else:
                print("  Reference Output Off")

            if(stat & 0x40):
                print("  Blanking On")
            else:
                print("  Blanking Off")

            if(stat & 0x80):
                print("  Lock Recovery Off")
            else:
                print("  Lock recovery On")

        return stat

    def getTemperatureC(self):
        ret = self._query("DIAG:MEAS? 21")
        return float(ret)

    def getTemperatureF(self):
        T_C = self.getTemperatureC
        T_F = T_C * 1.8 + 32
        return T_F

    def resetDevice(self):
        self._write("*RST")
    
