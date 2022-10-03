# -*- coding: utf-8 -*-
'''
Module Keysight_ENA_Eth
=================================
This module is responsible for communicating with the Keysight ena Signal Analyzer over
Ethernet using the pyvisa infrastructure. 
'''
# System level imports
import pyvisa
import numpy as np

# local imports


class Keysight_ENA_Eth:
    def __init__(self, visa_resource_manager:pyvisa.ResourceManager, resource_name="TCPIP::K-E5080A-01140.local::inst0::INSTR"):
        self.resource_name = resource_name    # VISA Device ID
        self.rm = visa_resource_manager
        self._sent_str = ''
        self._ret_str = ''
        self._ret_data = ''
        self.IDN = ''
        self._termination = '\n'
        self.debug = False

    def _write(self, str_in: str):
        self._sent_str = str_in
        if(self.debug):
            print("Keysight_ENA_Eth._write(): {}".format(self._sent_str))
        self.ena.write(self._sent_str)
        
    def _read(self) -> str:
        self._ret_str = self.ena.read()
        if(self.debug):
            print("Keysight_ENA_Eth._read(): {}".format(self._sent_str))
        return self._ret_str

    def _query(self, str_in:str) -> str:
        self._sent_str = str_in
        if(self.debug):
            print("Keysight_ENA_Eth._query():")
            print("  {}".format(str(self._sent_str)))
        self._ret_str = self.ena.query(self._sent_str)
        if(self.debug):
            print("  {}".format(str(self._ret_str)))
    
    def open(self):
        self.ena = self.rm.open_resource(self.resource_name)
        self.ena.write_termination = self._termination
        self.ena.read_termination = self._termination
        self.ena.write("*CLS")
        self.IDN = self._query("*IDN?")

    def close(self):
        self.ena.close()

    def info(self, print_out=False):
        if(print_out):
            print(self.IDN)
            return ""
        else:
            return self.IDN

    def getXValues_Hz(self) -> np.array(float):
        self._query(":CALCulate:MEASure:X:ValUES?")
        data = np.array(self._ret_str.split(",")).astype(float)
        return data

    def getCenterFrequency_Hz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:CENT?")
        return (float(self._ret_str))

    def getCenterFrequency_MHz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:CENT?")
        return (float(self._ret_str)/1e6)

    def getCenterFreqneucy_GHz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:CENT?")
        return (float(self._ret_str)/1e9)

    def setCenterFrequency_Hz(self, center_Hz):
        self._write(":SENS:FREQ:CENT {}".format(str(center_Hz)))

    def setCenterFrequency_MHz(self, center_MHz):
        self._write(":SENS:FREQ:CENT {}".format(str(center_MHz*1e6)))

    def setCenterFreqneucy_GHz(self, center_GHz):
        self._write(":SENS:FREQ:CENT {}".format(str(center_GHz*1e9)))

    def getSpanFrequency_Hz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:SPAN?")
        return (float(self._ret_str))
    
    def getSpanFrequency_MHz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:SPAN?")
        return (float(self._ret_str)/1e6)

    def getSpanFrequency_GHz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:SPAN?")
        return (float(self._ret_str)/1e9)

    def setSpanFrequency_Hz(self, Span_Hz):
        self._write(":SENS:FREQ:SPAN {}".format(str(Span_Hz)))

    def setSpanFrequency_MHz(self, Span_MHz):
        self._write(":SENS:FREQ:SPAN {}".format(str(Span_MHz*1e6)))

    def setSpanFrequency_GHz(self, Span_GHz):
        self._write(":SENS:FREQ:SPAN {}".format(str(Span_GHz*1e9)))

    def getStartFrequency_Hz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:STAR?")
        return (float(self._ret_str))
    
    def setStartFrequnecy_Hz(self, start_Hz):
        self._write(":SENS:FREQ:START {}".format(str(start_Hz)))

    def getStopFrequency_Hz(self) -> float:
        self._ret_str = self._query(":SENS:FREQ:STOP?")
        return(float(self._ret_str))

    def setStopFrequency_Hz(self, stop_Hz):
        self._write(":SENS:FREQ:STOP {}".format(str(stop_Hz)))
        
    def getNumberPoints(self) -> int:
        self._ret_str = self._query(":SENS:SWE:POINTS?")
        return int(self._ret_str)

    def setNumberPoints(self, nPoints:int):
        self._write(":SENS:SWE:POINTS {}".format(str(nPoints)))

    def getData(self, trace):
        '''This will return the raw data in Real + Imaginary'''
        self._write("CALC:MEAS{}:DATA:SDATA?".format(int(trace)))
        self._ret_data = self._read()
        raw_data = np.array(self._ret_data.split(',')).astype(float)
        data = np.zeros(int(raw_data.shape[0]/2), dtype=complex)
        for i in range(int(raw_data.shape[0]/2)):
            data[i] = complex(raw_data[0 + i*2], raw_data[1 + i*2])
        return data

    def getFormattedData(self, trace):
        '''This will return dBm as measured on the instrument'''
        self._write("CALC:MEAS{}:DATA:FDATA?".format(int(trace)))
        self._ret_data = self._read()
        data = np.array(self._ret_data.split(',')).astype(float)
        return data

    def triggerSweep(self):
        '''Trigger a sweep, this is a blocking command'''
        self._query("SENS:SWE:MODE SING; *OPC?")

    def triggerSweepAverage(self):
        '''This reads back the number of averages set and then single triggers that many times'''
        num_avg = self.getNumberAverages()
        for i in range(num_avg):
            self.triggerSweep()

    def setPresetInstrument(self):
        ''' Set the instrument to the power on preset'''
        self._query("SYST:PRES; *OPC?") 

    def setAverageReset(self):
        self._write(":SENS1:AVER:CLE")

    def setAverageOn(self):
        self._write(":SENS1:AVER ON")
        pass

    def setAverageOff(self):
        self._write(":SENS1:AVER OFF")
        pass

    def setNumberAverages(self, num_averages:int):
        self._write(":SENS1:AVER:COUN {}".format(int(num_averages)))
        pass

    def getNumberAverages(self) -> int:
        self._ret_str = self._query(":SENS1:AVER:COUN?")
        return int(self._ret_str)
        
    def setIFBandwidth(self, bandwidth_Hz):
        pass

    def getIFBandwidth(self) -> float:
        pass

    ''' Marker Control Methods'''
    def setMarkerOn(self, N):
        self._write(":CALCulate:MARKer{}:MODE POS".format(int(N)))

    def setMarkOff(self, N):
        self._write(":CALCulate:MARKer{}:MODE OFF".format(int(N)))

    def setMarkFreq_Hz(self, N, marker_Hz):
        self._write("CALCulate:MARKer{}:X {}".format(int(N), str(marker_Hz)))

    def getMarkFreq_Hz(self, N) -> float:
        self._ret_str = self._query("CALCulate:MARKer{}:X?".format(int(N)))
        return float(self._ret_str)

    def getMarkPower(self, N) -> float:
        self._ret_str = self._query(":CALCulate:MARKer{}:Y?".format(int(N)))
        return float(self._ret_str)

    def setMarkMax(self, mark_num):
        self._write(":CALC:MARK{}:MAX".format(int(mark_num)))

    def setMarkNextMax(self, mark_num):
        self._write(":CALC:MARK{}:MAX:NEXT".format(int(mark_num)))

    def setPower(self, pwr_dBm):
        pass