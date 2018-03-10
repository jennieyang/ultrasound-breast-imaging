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

def freqToPW(freq, numCycles):
    pw = 1 / float(freq) * int(numCycles)
    return '{:.2f}'.format(pw)

def PWToFreq(pw, numCycles):
    freq = 1 / ( float(pw) / int(numCycles) )
    return '{:0f}'.format(freq)