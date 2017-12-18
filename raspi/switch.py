    
def configureSwitch(txList, rxList, dialog):
    dialog.sendMsg("Configuring switch with parameters:")
    dialog.sendMsg("<pre>\tTx: %s</pre>" % " ".join(str(x) for x in txList))
    dialog.sendMsg("<pre>\tRx: %s</pre>" % " ".join(str(x) for x in rxList))
    
    dialog.sendMsg("Switch configured.")