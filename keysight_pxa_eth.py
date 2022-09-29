# -*- coding: utf-8 -*-
'''
Module Keysight_PXA_Eth
=================================
This module is responsible for communicating with the Keysight PXA Signal Analyzer over
Ethernet using the pyvisa infrastructure. 
'''
# System level imports
import pyvisa

# local imports


class Keysight_PXA_Eth:
    def __init__(self, visa_resource_manager:pyvisa.ResourceManager, resource_name="TCPIP::K-N9030A-10275.local::5025::SOCKET"):
        self.resource_name = resource_name    # VISA Device ID
        self.rm = visa_resource_manager
        self._sent_str = ''
        self._ret_str = ''
        self._ret_data = ''
        self.IDN = ''
        self._termination = '\n'
    def _write(self, str_in: str):
        pass
        
    def _read(self) -> str:
        return " "
    
    def open(self):
        self.pxa = self.open_resource(self.resource_name)
        self.pxa.write_termination = self._termination
        self.pxa.read_termination = self._termination
        self.pxa.write("*CLS")
        self.IDN = self.pxa.query("*IDN?")

    def close(self):
        self.pxa.close()

    def info(self, print_out=False):
        if(print_out):
            print(self.IDN)
            return ""
        else:
            return self.IDN
    
    def getCenterFrequency_Hz(self) -> float:
        self._ret_str = self.pxa.query(":SENS1:FREQ:CENT?")
        return (float(self._ret_str))

    def getCenterFrequency_MHz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:CENT?")
        return (float(self._ret_str)/1e6)

    def getCenterFreqneucy_GHz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:CENT?")
        return (float(self._ret_str)/1e9)

    def setCenterFrequency_Hz(self, center_Hz):
        self.pxa.write(":SENS1:FREQ:CENT {}".format(str(center_Hz)))

    def setCenterFrequency_MHz(self, center_MHz):
        self.pxa.write(":SENS1:FREQ:CENT {}".format(str(center_MHz*1e6)))

    def setCenterFreqneucy_GHz(self, center_GHz):
        self.pxa.write(":SENS1:FREQ:CENT {}".format(str(center_GHz*1e9)))

    def getSpanFrequency_Hz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:SPAN?")
        return (float(self._ret_str))
    
    def getSpanFrequency_MHz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:SPAN?")
        return (float(self._ret_str)/1e6)

    def getSpanFrequency_GHz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:SPAN?")
        return (float(self._ret_str)/1e9)

    def setSpanFrequency_Hz(self, Span_Hz):
        self.pxa.write(":SENS1:FREQ:SPAN {}".format(str(Span_Hz)))

    def setSpanFrequency_MHz(self, Span_MHz):
        self.pxa.write(":SENS1:FREQ:SPAN {}".format(str(Span_MHz*1e6)))

    def setSpanFrequency_GHz(self, Span_GHz):
        self.pxa.write(":SENS1:FREQ:SPAN {}".format(str(Span_GHz*1e9)))

    def getStartFrequency_Hz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:STAR?")
        return (float(self._ret_str))
    
    def setStartFrequnecy_Hz(self, start_Hz):
        self.pxa.write(":SENS1:FREQ:START {}".format(str(start_Hz)))

    def getStopFrequency_Hz(self):
        self._ret_str = self.pxa.query(":SENS1:FREQ:STOP?")
        return(float(self._ret_str))

    def setStopFrequency_Hz(self, stop_Hz):
        self.pxa.write(":SENS1:FREQ:STOP {}".format(str(stop_Hz)))
        
    def getNumberPoints(self):
        self._ret_str = self.pxa.write(":SENS:SWE:POIN?")

    def setNumberPoints(self, nPoints):
        self.pxa.write(":SENS:SWE:POIN {}".format(str(nPoints)))

    def getData(self, trace):
        self.pxa.write("CALC{}:DATA? SDATA".format(str(trace)))
        self._ret_data = self.pxa.read()
        return self._ret_data

    def triggerSweep(self):
        '''Trigger a sweep, this is a blocking command'''
        self.pxa.query("SENS:SWE:MODE SING; *OPC?")

    def setPresetInstrument(self):
        ''' Set the instrument to the power on preset'''
        self.pxa.query("SYST:PRES; *OPC?") 

    def setAverageOn(self):
        # :SENS1:AVER ON'
        pass

    def setAverageOff(self):
        # :SENS1:AVER OFF'
        pass

    def setNumberAverages(self, num_averages):
        # :SENS1:AVER:COUN {}.format(int())
        pass

    def getNumberAverages(self):
        pass

    def setIFBandwidth(self, bandwidth_Hz):
        pass

    def getIFBandwidth(self):
        pass

    ''' Marker Control Methods'''
    def setMarkerOn(self, N):
        self.pxa.write(':CALC1:MARK%d ON' % (N))

    def setMarkOff(self, N):
        self.pxa.write(':CALC1:MARK%d OFF' % (N))

    def setMarkFreq_Hz(self, N, marker_Hz):
        pass

    def getMarkFreq_Hz(self, N):
        pass

    def getMarkPower(self, N):
        pass

    def setCalibrateInstrument(self):
        '''Should block until done'''
        pass

    def getCalibrationInstrument(self):
        ''' Does the instrument need to be calibrated?'''
        pass