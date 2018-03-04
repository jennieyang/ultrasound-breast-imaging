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