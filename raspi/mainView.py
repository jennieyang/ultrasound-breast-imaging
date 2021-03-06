import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import raspi.utility

class MainView():
    def __init__(self, form):
        self.form = form
        self.createTransTable()
        self.createMappingTable()
        self.freqEntered = False
        self.pwEntered = False
        self.numCycEntered = False
        self.errorDialog = None
    
    def setParams(self, iv):
        invalidMappings = iv.setMapping(self.getTableItems(self.form.tableWidget_transMapping))
        self.setCellHighlight(self.form.tableWidget_transMapping, invalidMappings, 1)
        
        iv.setTransSeq(self.getTableItems(self.form.tableWidget_transConfig))
        invalidTrans = iv.checkErrors()
        # invalid tx input
        self.setCellHighlight(self.form.tableWidget_transConfig, invalidTrans[0], 0)
        # invalid rx input
        self.setCellHighlight(self.form.tableWidget_transConfig, invalidTrans[1], 1)
        
        iv.setWaveSelection(self.getWaveSelection())
        iv.setWaveFile(self.form.lineEdit_waveFileName.text())
        iv.setWaveType(self.form.comboBox_waveform.currentText())
        iv.setFreq(self.form.lineEdit_freq.text())
        iv.setNumCycles(self.form.lineEdit_numCycles.text())
        iv.setPulseWidth(self.form.lineEdit_pulseWidth.text())
        iv.setNumSamps(self.form.lineEdit_numSamps.text())
        iv.setSampRate(self.form.lineEdit_sampRate.text())
    
    def setCellHighlight(self, table, list, col):
        indexes = [item[0] for item in list]
        errors = [item[1] for item in list]
        i = 0
        for row in range(0, table.rowCount()):
            if row in indexes:
                table.item(row, col).setBackground(QColor(255,100,100))
                table.item(row, col).setToolTip("\n".join(errors[i]))
                i = i + 1
            else:
                # reset highlight
                table.item(row, col).setBackground(QColor(255,255,255))
                table.item(row, col).setToolTip("")
    
    def getTableItems(self, table):
        items = []
        for r in range(0,table.rowCount()):
            col0 = table.item(table.verticalHeader().logicalIndex(r),0).text()
            col1 = table.item(table.verticalHeader().logicalIndex(r),1).text()
            if col0 != '' and col1 != '': # don't add incomplete entries
                items.append([col0, col1])
        return items
    
    def getWaveSelection(self):
        if self.form.widget_selectWaveform.isEnabled() is True:
            waveSelection = 0 # Defined wave
        else: # selectWave enabled
            waveSelection = 1 # Arbitrary wave
        return waveSelection
    
    def getFile(self, lineEditWidget, nameFilters):
        dlg = QFileDialog()
        dlg.setNameFilters(nameFilters)
        if dlg.exec_():
            filePath = dlg.selectedFiles()[0]
            lineEditWidget.setText(filePath)

    def saveTransFile(self):
        filepath = self.saveFile('Text File (*.txt)')
        if filepath != '':
            sequence = self.getTableItems(self.form.tableWidget_transConfig)
            raspi.utility.saveTransducerSeq(filepath, sequence)
    
    def saveMappingFile(self):
        filepath = self.saveFile('INI File (*.ini)')
        if filepath != '':
            mapping = self.getTableItems(self.form.tableWidget_transMapping)
            raspi.utility.saveTransducerMapping(filepath, mapping)
    
    def saveFile(self, saveType):
        dlg = QFileDialog()
        filepath = QFileDialog.getSaveFileName(dlg, 'Save As', 'C:/Users/Jennie/Desktop', saveType)
        return filepath[0]
    
    def browseWaveFile(self):
        self.getFile(self.form.lineEdit_waveFileName, ['Text Files (*.txt)', 'All Files (*.*)'])
        
    def browseTransFile(self):
        self.getFile(self.form.lineEdit_transFileName, ['Text Files (*.txt)', 'All Files (*.*)'])
    
    def browseMappingFile(self):
        self.getFile(self.form.lineEdit_mappingFileName, ['INI Files (*.ini)', 'All Files (*.*)'])
    
    def en_selectWave(self):
        self.form.widget_loadWaveFile.setEnabled(False)
        self.form.widget_selectWaveform.setEnabled(True)

    def en_loadWaveFile(self):
        self.form.widget_loadWaveFile.setEnabled(True)
        self.form.widget_selectWaveform.setEnabled(False)

    def createMappingTable(self):
        self.form.tableWidget_transMapping.setHorizontalHeaderLabels(["Transducer Number", "Switch ID"])
        
        # set column widths
        self.form.tableWidget_transMapping.horizontalHeader().setStretchLastSection(True)
        self.form.tableWidget_transMapping.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
        
        rows = self.form.tableWidget_transMapping.rowCount()
        for r in range(rows):
            transNumItem = QTableWidgetItem('%s' % (r+1))
            transNumItem.setFlags( Qt.ItemIsEnabled ) # make cells uneditable
            self.form.tableWidget_transMapping.setItem(r, 0, transNumItem)
            self.form.tableWidget_transMapping.setItem(r, 1, QTableWidgetItem(''))
            
    def setMapping(self, mapping):
        for transNum in mapping.keys():
            rowIndex = int(transNum)-1
            switchId = mapping[transNum]
            self.form.tableWidget_transMapping.setItem( rowIndex, 1, QTableWidgetItem(switchId) )
    
    def createTransTable(self):
        self.form.tableWidget_transConfig.setColumnCount(2)
        self.form.tableWidget_transConfig.setHorizontalHeaderLabels(["Tx", "Rx"])
        
        # set column widths
        self.form.tableWidget_transConfig.horizontalHeader().setStretchLastSection(True)
        #self.form.tableWidget_transConfig.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
        
        self.form.tableWidget_transConfig.verticalHeader().setSectionsMovable(True)

    def addTableItem(self, txList, rxList):
        # insert row at last position
        rowPosition = self.form.tableWidget_transConfig.rowCount()
        self.form.tableWidget_transConfig.insertRow(rowPosition)
        
        # set row with tx and rx
        self.form.tableWidget_transConfig.setItem(rowPosition,0,QTableWidgetItem(txList))
        self.form.tableWidget_transConfig.setItem(rowPosition,1,QTableWidgetItem(rxList))
        
    def addEmptyRow(self):
        self.addTableItem("","")
        
    def updateTransTable(self, filepath):
        # read selected config file
        try:
            sequence = raspi.utility.getTransducerSeq(filepath)
            for s in sequence:
                self.addTableItem(s[0], s[1])
        except:
            self.errorDialog = QMessageBox.critical(None,'Error',"There was an error parsing selected transducer file " + filepath, QMessageBox.Ok)
        
    def updateMappingTable(self, filepath):
        # read selected config file
        try:
            mapping = raspi.utility.loadTransducerMapping(filepath)
            self.setMapping(mapping)
        except:
            self.errorDialog = QMessageBox.critical(None,'Error',"There was an error parsing selected mapping file " + filepath, QMessageBox.Ok)

    def freqInputHandler(self):
        freq = self.form.lineEdit_freq.text()
        numCycles = self.form.lineEdit_numCycles.text()
        if freq == '':
            self.freqEntered = False
            if self.numCycEntered == True:
                self.form.lineEdit_pulseWidth.clear()
        else:
            self.freqEntered = True
            self.pwEntered = False
            self.form.lineEdit_pulseWidth.clear()
            if self.numCycEntered == True:
                try:
                    self.form.lineEdit_pulseWidth.setText(raspi.utility.freqToPW(freq, numCycles))
                except Exception:
                    pass
    
    def pwInputHandler(self):
        pw = self.form.lineEdit_pulseWidth.text()
        numCycles = self.form.lineEdit_numCycles.text()
        if pw == '':
            self.pwEntered = False
            if self.numCycEntered == True:
                self.form.lineEdit_freq.clear()
        else:
            self.pwEntered = True
            self.freqEntered = False
            self.form.lineEdit_freq.clear()
            if self.numCycEntered == True:
                try:
                    self.form.lineEdit_freq.setText(raspi.utility.PWToFreq(pw, numCycles))
                except Exception:
                    pass
    
    def numCycInputHandler(self):
        freq = self.form.lineEdit_freq.text()
        pw = self.form.lineEdit_pulseWidth.text()
        numCycles = self.form.lineEdit_numCycles.text()
        if numCycles == '':
            self.numCycEntered = False
            if self.freqEntered:
                self.form.lineEdit_pulseWidth.clear()
            if self.pwEntered:
                self.form.lineEdit_freq.clear()
        else:
            self.numCycEntered = True
            if self.freqEntered:
                try:
                    self.form.lineEdit_pulseWidth.setText(raspi.utility.freqToPW(freq, numCycles))
                except Exception:
                    pass
            if self.pwEntered:
                try:
                    self.form.lineEdit_freq.setText(raspi.utility.PWToFreq(pw, numCycles))
                except Exception:
                    pass