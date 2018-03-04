import utility

class InputValidator():
    def __init__(self):
        self.transSeq = None
        self.waveSelection = None
        self.waveFile = None
        self.waveType = None
        self.freq = None
        self.numCycles = None
        self.numSamps = None
        self.sampRate = None
        self.valid = True
    
    def isValid(self):
        return self.valid
    
    def getTransSeq(self):
        return self.transSeq
        
    def setTransSeq(self, value):
        seq = []
        for r in range(0, len(value)):
            txList = value[r][0]
            rxList = value[r][1]
            trans = utility.parse(txList,rxList) # parse string entry and order values
            seq.append(trans)
        self.transSeq = seq
        return (self.validateTx(), self.validateRx())
    
    def getNumSeq(self):
        return len(self.transSeq)
    
    def validateTx(self):
        invalidRows = []
        for row in range(0, len(self.transSeq)):
            txList = self.transSeq[row][0]
            # only one transmitter allowed
            # must be between 1 and 60 (inclusive)
            if (len(txList) != 1) or (txList[0] < 1) or (txList[0] > 60):
                invalidRows.append(row)
                self.valid = False
            row = row + 1
        return invalidRows
    
    def validateRx(self):
        NUM_BOARDS = 4
        invalidRows = []
        for row in range(0, len(self.transSeq)):
            txNum = self.transSeq[row][0][0]
            rxList = self.transSeq[row][1]
            valid = True
            flag = [0] * NUM_BOARDS
            # only one transducer can be transmitting per board
            # can't contain same transducer as Tx
            # must be between 1 and 60 (inclusive)
            for rxNum in rxList:
                boardNum = rxNum % NUM_BOARDS
                if (flag[boardNum] != 0) or (rxNum == txNum) or (rxNum < 1) or (rxNum > 60): 
                    valid = False
                    self.valid = False
                else:
                # valid & no transducers selected from boardNum yet
                    flag[boardNum] = 1
            if not valid:
                invalidRows.append(row)
        return invalidRows
    
    def getWave(self):
        if (self.waveSelection == 0):
            # defined waveform
            wave = self.waveType
        else:
            # arbitrary waveform
            wave = self.waveFile
        return wave
    
    def getWaveSelection(self):
        return self.waveSelection
        
    def setWaveSelection(self, value):
        self.waveSelection = value
		
    def setWaveFile(self, value):
        self.waveFile = value
        
    def setWaveType(self, value):
        self.waveType = value
    
    def getNumCycles(self):
        return self.numCycles
        
    def setNumCycles(self, value):
        self.numCycles = value
        
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