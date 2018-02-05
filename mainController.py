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
        
    def validateInput(self):
        iv = inputValidator.InputValidator()
        self.iv = iv
        self.view.setParams(iv)
        if iv.isValid():
            self.beginAcquisition()
        else:
            # open error dialog
            print("Error: check highlighted input fields")
    
    def beginAcquisition(self):
        self.dialog.clear()
        self.dialog.show()
        
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
        
    def runTest(self):
        self.dialog.clear()
        self.dialog.show()
        self.dialog.sendMsg("Running test...")
        
        '''@TODO: get filepath of cfg file in current dir with sys.os.path'''
        cfg = utility.ConfigFileParser("C:/Users/Jennie/Desktop/Capstone/default.ini")   
        
        sequence = cfg.getTransducerSeq("TEST")
        r=1
        for s in sequence:
            transducers = utility.parse(s[0], s[1])
            self.dialog.sendMsg("<br>Executing sequence %d" % r, 'red')
            raspi.switch.configureSwitch(transducers[0], transducers[1], self.dialog)
            r = r+1
            
            raspi.waveformGenerator.sendWaveform(self.dialog)
        self.dialog.sendMsg("<br>Test complete", "red")