import raspi.utility as utility

class InputValidator():
    def __init__(self):
        self.mapping = None
        self.switchSeq = None
        self.transSeq = None
        self.waveSelection = None
        self.waveFile = None
        self.waveType = None
        self.freq = None
        self.pulseWidth = None
        self.numCycles = None
        self.numSamps = None
        self.sampRate = None
        self.valid = True
    
    def isValid(self):
        return self.valid
    
    def checkErrors(self):
        invalidTx = []
        invalidRx = []
        for s in range(0, len(self.switchSeq)):
            seq = self.switchSeq[s]
            if len(seq['txErrors']) != 0:
                invalidTx.append((s, seq['txErrors']))
                self.valid = False
            if len(seq['rxErrors']) != 0:
                invalidRx.append((s, seq['rxErrors']))
                self.valid = False
        return (invalidTx, invalidRx)
        
    def getMapping(self):
        return mapping
    
    def setMapping(self, value):
        mapping = {}
        for r in range(0, len(value)):
            transNum = value[r][0]
            switchId = value[r][1]
            mapping[transNum] = switchId
        self.mapping = mapping
        return self.validateMapping()
        
    def validateMapping(self):
        reverse = {}
        duplicates = {}
        invalidMappings = {}
        for transNum in self.mapping:
            switchId = self.mapping[transNum]
            # check for invalid switch id: board letter must be A,B,C,D and switch number 1-15
            try:
                boardLetter = switchId[0].upper()
                switchNum = int(switchId[1:])
                if ord(boardLetter) < ord('A') or ord(boardLetter) > ord('D') or switchNum < 1 or switchNum > 15:
                    error = "Invalid switch ID: Must contain board letter A-D and transducer number 1-15"
                    invalidMappings[int(transNum)-1] = [error]
            except Exception:
                error = "Invalid switch ID: Must contain board letter A-D and transducer number 1-15"
                invalidMappings[int(transNum)-1] = [error]
                
            # check for invalid mapping: more than one transducer number maps to same switch id
            if switchId in reverse:
                if switchId in duplicates:
                    duplicates[switchId].append(transNum)
                else:
                    # create new dictionary entry containing list of transducer numbers with same switch id for the invalid switch id
                    duplicates[switchId] = [ reverse[switchId], transNum ]
            else:
                reverse[switchId] = transNum
        
        for switchId in duplicates:
            error = "Invalid mapping: Transducer to switch must be a one-to-one mapping\n%s is mapped to %s" %(switchId, ','.join(duplicates[switchId]))
            for transNum in duplicates[switchId]:
                invalidMappings[int(transNum)-1] = [error]
        
        if len(invalidMappings) != 0:
            self.valid = False
            
        indexedInvalid = []
        for index in sorted(invalidMappings):
            errors = invalidMappings[index]
            indexedInvalid.append((index, errors))
        
        return indexedInvalid
        
    def getSwitchSeq(self):
        return self.switchSeq
        
    def setTransSeq(self, value):
        switchSeq = []
        self.transSeq = []
        for n in range(0, len(value)):
            txList = [x.strip() for x in value[n][0].split(',')]
            rxList = [x.strip() for x in value[n][1].split(',')]
            self.transSeq.append((list(txList), list(rxList))) # copy list into transSeq
            
            seq = {}
            seq['txErrors'] = []
            seq['rxErrors'] = []
            
            for t in range(0, len(txList)):
                transNum = txList[t]
                if transNum in self.mapping: # mapping found for transducer number
                    txList[t] = self.mapping[transNum]
                else:
                    error = "Invalid transducer number: Mapping not found for transducer " + transNum
                    seq['txErrors'].append(error)
            seq['tx'] = txList
            
            for r in range(0, len(rxList)):
                transNum = rxList[r]
                if transNum in self.mapping: # mapping found for transducer number
                    rxList[r] = self.mapping[transNum]
                else:
                    error = "Invalid transducer number: Mapping not found for transducer " + transNum
                    seq['rxErrors'].append(error)
            seq['rx'] = rxList

            switchSeq.append(seq)
        self.switchSeq = switchSeq
        self.validateTx()
        self.validateRx()
    
    def getTransSeq(self):
        return self.transSeq
    
    def getNumSeq(self):
        return len(self.transSeq)
    
    def validateTx(self):
        for seq in self.switchSeq:
            txList = seq['tx']
            # only one transmitter allowed
            if (len(txList) != 1):
                error = "Invalid Tx: Only one transmitting transducer allowed"
                seq['txErrors'].append(error)
        
    def validateRx(self):
        NUM_BOARDS = 4
        for seq in self.switchSeq:
            txList = seq['tx']
            rxList = seq['rx']
            
            # 0 - letter not in rxList
            flag = {'A':0, 'B':0, 'C':0, 'D':0}
            for r in rxList:
                boardLetter = r[0]
                if boardLetter.isalpha():
                    # only one transducer can be receiving per board
                    if flag[boardLetter] != 0:
                        # board already has transducer set to rx
                        error = "Invalid Rx: Only one receiving transducer allowed per board"
                        if error not in seq['rxErrors']:
                            seq['rxErrors'].append(error)
                    else:
                        # set flag for board
                        flag[boardLetter] = 1
            
                # rx can't contain same transducer as tx
                if r in txList:
                    error = "Invalid Tx/Rx: Transducer cannot be set to transmit and receive"
                    seq['txErrors'].append(error)
                    seq['rxErrors'].append(error)
        
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
        
    def getPulseWidth(self):
        return self.pulseWidth
        
    def setPulseWidth(self, value):
        self.pulseWidth = value
        
    def getNumSamps(self):
        return self.numSamps
        
    def setNumSamps(self, value):
        self.numSamps = value
        
    def getSampRate(self):
        return self.sampRate
        
    def setSampRate(self, value):
        self.sampRate = value