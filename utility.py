import configparser
import io


#Gets the transmitter:receiver sequence from a config txt file
def getTransducerSeq(filepath):
    sequence = []
    with open(filepath) as fp:
        for line in fp:
            line = line.replace('\n','').replace(' ','')
            tx,rx = line.split(':')
            sequence.append( (tx,rx) )
            
    return sequence

def saveTransducerSeq(filepath, sequence):
    with open(filepath, 'w') as fp:
        for s in sequence:
            fp.write("%s : %s\n" % (s[0], s[1]))

def loadTransducerMapping(filepath):
    config = configparser.RawConfigParser()
    config.read(filepath)
    mapping = {}
    with open(filepath, 'r') as fp:
        for transNum in config['MAPPING']:
            switchId = config['MAPPING'][transNum]
            mapping[transNum] = switchId
    return mapping

def saveTransducerMapping(filepath, mapping):
    config = configparser.RawConfigParser()
    config.add_section('MAPPING')
    for m in mapping:
        config['MAPPING'][m[0]] = m[1]
        
    with open(filepath, 'w') as fp:
        config.write(fp)
    
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