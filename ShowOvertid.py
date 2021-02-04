from ShowOvertid_ui import Ui_ShowOvertid
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from dbsqlite import timedb
from timeclass import BJtimeclass as bjtime
#from pathlib import Path
import qdarkstyle 
#import yaml

class showovertid(qtw.QWidget):
    
    db_saved = qtc.pyqtSignal(str)

    def __init__(self, dbfile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_ShowOvertid()
        self.setGeometry(1325,100,2533,698) 
        self.ui.setupUi(self)
        #self.ask_unsaved = qtw.QMessageBox.question()
        self.error_unsaved = qtw.QErrorMessage()

        self.x = 0
        self.unsaved = False
        self.edited_row_col_data = []
        
        self.db_file = dbfile

        self.ui.tableWidget.cellDoubleClicked.connect(self.dobbelClickedTable)

        self.visOvertid()

    def dobbelClickedTable(self, idx):
        for idx in self.ui.tableWidget.selectionModel().selectedIndexes():
            row = idx.row()
            column = idx.column()
        #print('row ', str(row), '  column ', str(column))
        data=self.ui.tableWidget.item(row,column).text()
        iddb=self.ui.tableWidget.item(row,0).text()
        #print('data = ', iddb)
        
        if column==11:      # collone registrert
            if data=='0':       # endre til registrert
                data='1'
            else:
                data='0'      # endre til uregistrert
        
            self.ui.tableWidget.setItem(row,column, qtw.QTableWidgetItem(data))
            timedb.updateOvertidRecord(self, self.db_file, iddb, data)              #lagre til Databasen som overtid levert


    def visOvertid(self):
        sqldata= timedb.LoadOvertid(self, self.db_file)
        self.ui.tableWidget.clearContents()

        rows=self.ui.tableWidget.rowCount()
        #columns=self.ui.tableWidget.columnCount()
        if rows>0:
            for r in range(rows):
                self.ui.tableWidget.removeRow(0)
                r
        
        flags = qtc.Qt.ItemFlags()
        flags != qtc.Qt.ItemIsEnabled        
        
        for row_number, row_data in enumerate(sqldata):
            self.ui.tableWidget.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                item = qtw.QTableWidgetItem(str(data))
                if colum_number==0:
                    item.setFlags(flags)
                if colum_number==1:
                    item.setFlags(flags)
                if colum_number==2:
                    item.setFlags(flags)
                if colum_number==3:
                    item.setFlags(flags)
                if colum_number==4:
                    item.setFlags(flags)
                if colum_number==5:
                    item.setFlags(flags)
                if colum_number==6:
                    item.setFlags(flags)
                if colum_number==8:
                    item.setFlags(flags)
                if colum_number==9:
                    item.setFlags(flags)
                if colum_number==10:
                    item.setFlags(flags)
                if colum_number==12:
                    item.setFlags(flags)
                if colum_number==13:
                    item.setFlags(flags)
                self.ui.tableWidget.setItem(row_number,colum_number,item)
