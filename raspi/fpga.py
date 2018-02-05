class FPGA():
    def __init__(self, dlg, numSamps, sampRate):
        self.dlg = dlg
        self.numSamps = numSamps
        self.sampRate = sampRate
        
    def configure(self):
        self.dlg.sendMsg("<br>Configuring FPGA with parameters:")
        self.dlg.sendMsg("<pre>\tNumber of Samples: %s samples</pre>" % self.numSamps)
        self.dlg.sendMsg("<pre>\tSampling Rate: %s MHz</pre>" % self.sampRate)
        '''call write SPI module'''
        self.dlg.sendMsg("FPGA configuration complete.", "blue")
    
    def startCapture(self):
        self.dlg.sendMsg("Triggering FPGA to begin capture")
        '''send start capture signal'''
    
    def receiveData(self, filePath):
        self.dlg.sendMsg("<br>Writing data to %s" % filePath)
        '''call read SPI module'''
        '''write data to file'''