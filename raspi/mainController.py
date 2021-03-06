import PyQt5
from PyQt5.QtWidgets import *
import raspi.device.switch
import raspi.device.waveformGenerator
import raspi.device.fpga
import raspi.utility
import raspi.inputValidator

class MainController():
    def setup(self, dialog, view):
        self.dialog = dialog
        self.view = view
        self.errorDialog = None
        self.iv = None
        
    def validateAcqInput(self):
        iv = raspi.inputValidator.InputValidator()
        self.iv = iv
        self.view.setParams(iv)
        
        if iv.isValid():
            self.dialog.clear()
            self.dialog.show()
            self.dialog.sendMsg("Running Acquisition", "red")
            self.beginAcquisition()
        else:
            # open error dialog
            self.errorDialog = QMessageBox.critical(None,'Error',"Invalid input: check highlighted fields", QMessageBox.Ok)
        
    def validateTestInput(self):
        iv = raspi.inputValidator.InputValidator()
        self.iv = iv
        '''@TODO: remove hard-coded file path'''
        cfg = raspi.utility.ConfigFileParser("C:/Users/Jennie/Desktop/Capstone/default.ini")
        iv.setTransSeq(cfg.getTransducerSeq("TEST"))
        iv.setWaveSelection(0)
        iv.setWaveType("Sinusoid")
        iv.setFreq(1000000)
        iv.setNumSamps(100)
        iv.setSampRate(50)
        
        if iv.isValid():
            self.dialog.clear()
            self.dialog.show()
            self.dialog.sendMsg("Running Test", "red")
            self.beginAcquisition()
        else:
            print("Error: check test input values")
    
    def beginAcquisition(self):
        self.dialog.sendMsg("Executing initialization sequence", "red")
        # initialize waveform generator
        wg = raspi.device.waveformGenerator.WaveformGenerator(self.dialog, self.iv.getWaveSelection(), self.iv.getWave(), self.iv.getNumCycles(), self.iv.getFreq(), self.iv.pulseWidth)
        wg.configure()
        # initialize fpga
        fpga = raspi.device.fpga.FPGA(self.dialog, self.iv.getNumSamps(), self.iv.getSampRate())
        fpga.configure()
        # initialize switch
        switch = raspi.device.switch.Switch(self.dialog)
        
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
        
        self.dialog.sendMsg("<br>Finished running %d sequences." % numSequences, "blue")
        '''@TODO: get acquisition folder from config file'''
        fpga.receiveData("C:/Users/Jennie/Desktop/Acquisitions")
        self.dialog.sendMsg("<br>Acquisition complete.", "blue")