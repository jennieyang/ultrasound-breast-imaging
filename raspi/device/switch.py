class Switch():
    def __init__(self, dlg):
        self.dlg = dlg
        
    def configure(self, txList, rxList):
        self.dlg.sendMsg("Configuring switch with parameters:")
        self.dlg.sendMsg("<pre>\tTx: %s</pre>" % " ".join(str(x) for x in txList))
        self.dlg.sendMsg("<pre>\tRx: %s</pre>" % " ".join(str(x) for x in rxList))
        ''' setupFrame() '''
        ''' send output enable signal '''
        self.dlg.sendMsg("Switch configuration complete.", "blue")
    
    def setupFrame(self):
        # i2c frame for writing to i/o expanders:
        # [slave address][command register][data0][data1][data2][data3][data4]
        # with auto-increment, all 5 output ports can be written to sequentially
        
        # NUM_IO_EXPANDERS frames will have to be sent out to write to each i/o expander
        # there are 5 ports to be written per i/o expander
        # format: data[device number][register number]
        '''TODO: get NUM_IO_EXPANDERS from constants file'''
        NUM_IO_EXPANDERS = 4
        data = [[0]*4 for i in range(NUM_IO_EXPANDERS)]
        
        #for i in range(0, NUM_IO_EXPANDERS):
        
        
        # need to left shift device address because bit 0 indicates R/nW
        # left shift again because we are using A2 and A1