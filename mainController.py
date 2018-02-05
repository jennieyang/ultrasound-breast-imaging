import PyQt5
from PyQt5.QtWidgets import *
import raspi.switch
import raspi.waveformGenerator
import raspi.fpga
import utility
import inputValidator

class MainController():
    def setup(self, dialog, view):
        self.dialog = dialog
        self.view = view
        self.iv = None
        
    def validateAcqInput(self):
        iv = inputValidator.InputValidator()
        self.iv = iv
        self.view.setParams(iv)
        
        self.dialog.clear()
        self.dialog.show()
        self.dialog.sendMsg("Running Acquisition", "red")
        if iv.isValid():
            self.beginAcquisition()
        else:
            # open error dialog
            print("Error: check highlighted input fields")
        
    def validateTestInput(self):
        iv = inputValidator.InputValidator()
        self.iv = iv
        '''@TODO: remove hard-coded file path'''
        cfg = utility.ConfigFileParser("C:/Users/Jennie/Desktop/Capstone/default.ini")
        iv.setTransSeq(cfg.getTransducerSeq("TEST"))
        iv.setWaveSelection(0)
        iv.setWaveType("Sinusoid")
        iv.setAmp(5)
        iv.setFreq(1000000)
        iv.setNumSamps(100)
        iv.setSampRate(50)
        
        self.dialog.clear()
        self.dialog.show()
        self.dialog.sendMsg("Running Test", "red")
        if iv.isValid():
            self.beginAcquisition()
        else:
            print("Error: check test input values")
    
    def beginAcquisition(self):
        self.dialog.sendMsg("Executing initialization sequence", "red")
        # initialize waveform generator
        wg = raspi.waveformGenerator.WaveformGenerator(self.dialog, self.iv.getWaveSelection(), self.iv.getWave(), self.iv.getFreq(), self.iv.getAmp())
        wg.configure()
        # initialize fpga
        fpga = raspi.fpga.FPGA(self.dialog, self.iv.getNumSamps(), self.iv.getSampRate())
        fpga.configure()
        # initialize switch
        switch = raspi.switch.Switch(self.dialog)
        
        # execute sequences
        numSequences = self.iv.getNumSeq()
        for r in range(0, numSequences):
            self.dialog.sendMsg("<br>Executing sequence %d" % (r+1), "red")
            
            # configure switch
            txList = self.iv.getTransSeq()[r][0]
            rxList = self.iv.getTransSeq()[r][1]
            switch.configure(txList, rxList)
            
            # transmit waveform
            wg.sendWaveform()
            fpga.startCapture()
            
        # receive data
        '''@TODO: get acquisition folder from config file'''
        fpga.receiveData("C:/Users/Jennie/Desktop/Acquisitions")
        self.dialog.sendMsg("<br>Acquisition complete.", "blue")