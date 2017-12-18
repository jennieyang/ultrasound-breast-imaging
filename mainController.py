import PyQt5
from PyQt5.QtWidgets import *
import raspi.switch
import raspi.transmission
import raspi.acquisition
import utility

class MainController():
    def setup(self, form, dialog, view):
        self.form = form
        self.dialog = dialog
        self.view = view
    
    def beginAcquisition(self):
        self.dialog.clear()
        self.dialog.show()
        self.dialog.sendMsg("Beginning acquisition...")
        self.dialog.sendMsg("Total sequences: %d" % self.form.tableWidget_transConfig.rowCount())
        
        '''@TODO: remove form dependency & convert transducer configs to model data'''
        for r in range(0,self.form.tableWidget_transConfig.rowCount()):
            txList = self.form.tableWidget_transConfig.item(r,0).text()
            rxList = self.form.tableWidget_transConfig.item(r,1).text()
            transducers = utility.parse(txList,rxList) # parse string entry and order values
            
            self.dialog.sendMsg("<br>Executing sequence %d" % (r+1), 'red')
            raspi.switch.configureSwitch(transducers[0], transducers[1], self.dialog)
            
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
        
        '''@TODO: get filepath from cmd line arguments with argparser & pass from main'''
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

    def browseWaveFile(self):
        self.view.browseWaveFile(['Text Files (*.txt)', 'All Files (*.*)'])
        
    def browseTransFile(self):
        filepath = self.view.browseTransFile(['INI Files (*.ini)', 'All Files (*.*)'])
        self.updateTable(filepath)
        
    def selectWaveform(self):
        self.view.en_selectWave()
        
    def loadWaveFile(self):
        self.view.en_loadWaveFile()
        
    def updateTable(self, filepath):
        # read selected config file
        cfg = utility.ConfigFileParser(filepath)
        sequence = cfg.getTransducerSeq("RUN")
        for s in sequence:
            self.view.addTableItem(s[0], s[1])
            
    def addEmptyRow(self):
        self.view.addTableItem("","")