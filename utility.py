import configparser
import io

class ConfigFileParser():
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = configparser.RawConfigParser()
        self.config.read(self.configFile)
        
    #Gets the transmitter:receiver sequence from a config file in INI format
    def getTransducerSeq(self, section):
        sequence = []
        
        for tx in self.config.options(section):
            rx = self.config.get(section,tx)
            sequence.append( (tx,rx) )
        
        return sequence

def parse(txList, rxList):
    txVals = 0
    rxVals = 0
    try:
        txVals = [int(x) for x in txList.split(',')]
        rxVals = [int(x) for x in rxList.split(',')]
    except:
        print("There was an error parsing values")
    
    txVals.sort()
    rxVals.sort()
    return (txVals, rxVals)