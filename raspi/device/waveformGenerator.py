class WaveformGenerator():
    def __init__(self, dlg, waveSelection, wave, numCycles, freq, pulseWidth):
        self.dlg = dlg
        self.waveSelection = waveSelection
        self.wave = wave
        self.numCycles = numCycles
        self.freq = freq
        self.pulseWidth = pulseWidth
        
    def configure(self):
        self.dlg.sendMsg("Configuring waveform generator with parameters:")
        self.dlg.sendMsg("<pre>\tWaveform Type: %s</pre>" % self.wave)
        self.dlg.sendMsg("<pre>\tNumber of Cycles: %s</pre>" % self.numCycles)
        self.dlg.sendMsg("<pre>\tPulse Width: %s µs</pre>" % self.pulseWidth)
        self.dlg.sendMsg("<pre>\tFrequency: %s Hz</pre>" % self.freq)
        
        '''call SPI module '''
        
        self.dlg.sendMsg("Waveform generator configuration complete.", "blue")
    
    def sendWaveform(self):
        self.dlg.sendMsg("Triggering waveform generator to transmit waveform")
        
        '''send trigger signal'''
    