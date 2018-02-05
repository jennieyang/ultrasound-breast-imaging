class InputValidator():
    def __init__(self, controller):
        self.controller = controller
        self.transSeq = None
        self.waveFile = None
        self.waveType = None
        self.amp = None
        self.freq = None
        self.numSamps = None
        self.sampRate = None
    
    def validate(self):
        self.controller.beginAcquisition()
    
    def getTransSeq(self):
        return self.transSeq
        
    def setTransSeq(self, value):
        self.transSeq = value
    
    def getWaveFile(self):
        return self.waveFile
		
    def setWaveFile(self, value):
        self.waveFile = value
        
    def getWaveType(self):
        return self.waveType
		
    def setWaveType(self, value):
        self.waveType = value
    
    def getAmp(self):
        return self.amp
        
    def setAmp(self, value):
        self.amp = value
        
    def getFreq(self):
        return self.freq
        
    def setFreq(self, value):
        self.freq = value
        
    def getNumSamps(self):
        return self.numSamps
        
    def setNumSamps(self, value):
        self.numSamps = value
        
    def getSampRate(self):
        return self.sampRate
        
    def setSampRate(self, value):
        self.sampRate = value