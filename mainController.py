import PyQt5
from PyQt5.QtWidgets import *
import raspi.switch
import raspi.transmission
import raspi.acquisition
import utility
import inputValidator

class MainController():
    def setup(self, form, dialog, view):
        self.form = form
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
            print("error")
            
    def beginAcquisition(self):
        self.dialog.clear()
        self.dialog.show()
        self.dialog.sendMsg(self.iv.getWaveType())
        self.dialog.sendMsg(self.iv.getAmp())
        self.dialog.sendMsg(self.iv.getFreq())
        self.dialog.sendMsg(self.iv.getNumSamps())
        self.dialog.sendMsg(self.iv.getSampRate())
        
        self.dialog.sendMsg("Beginning acquisition...")
        self.dialog.sendMsg("Total sequences: %d" % self.form.tableWidget_transConfig.rowCount())
        
        for r in range(0,self.form.tableWidget_transConfig.rowCount()):
            txList = self.iv.getTransSeq()[r][0]
            rxList = self.iv.getTransSeq()[r][1]
            
            self.dialog.sendMsg("<br>Executing sequence %d" % (r+1), 'red')
            raspi.switch.configureSwitch(txList, rxList, self.dialog)
            
            # transmit waveform
            raspi.transmission.sendWaveform(self.dialog)
            
        # receive data
        '''@TODO: get acquisition folder from config file'''
        raspi.acquisition.receiveData("C:/Users/Jennie/Desktop/Acquisitions", self.dialog)    
        self.dialog.sendMsg("<br>Acquisition complete", "red")
        
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
            
            raspi.transmission.sendWaveform(self.dialog)
        self.dialog.sendMsg("<br>Test complete", "red")

        
    def updateTable(self, filepath):
        # read selected config file
        cfg = utility.ConfigFileParser(filepath)
        try:
            sequence = cfg.getTransducerSeq("RUN")
            for s in sequence:
                self.view.addTableItem(s[0], s[1])
        except:
            print("There was an error parsing selected transducer file " + filepath)
    