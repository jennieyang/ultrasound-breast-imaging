class WaveformGenerator():
    def __init__(self, dlg, waveSelection, wave, freq):
        self.dlg = dlg
        self.waveSelection = waveSelection
        self.wave = wave
        self.freq = freq
        
    def configure(self):
        self.dlg.sendMsg("Configuring waveform generator with parameters:")
        self.dlg.sendMsg("<pre>\tWaveform: %s</pre>" % self.wave)
        self.dlg.sendMsg("<pre>\tFrequency: %s Hz</pre>" % self.freq)
        
        '''call SPI module '''
        
        self.dlg.sendMsg("Waveform generator configuration complete.", "blue")
    
    def sendWaveform(self):
        self.dlg.sendMsg("Triggering waveform generator to transmit waveform")
        
        '''send trigger signal'''
    