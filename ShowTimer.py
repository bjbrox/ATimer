from ShowTimer_ui import Ui_showtimer
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from dbsqlite import timedb
from timeclass import BJtimeclass as bjtime
#from pathlib import Path
import qdarkstyle 
#import yaml

class showtimer(qtw.QWidget):
    
    db_saved = qtc.pyqtSignal(str)

    def __init__(self, dbfile, ukenr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arg= ukenr
        self.ui = Ui_showtimer()
        self.setGeometry(1325,100,2533,698) 
        self.ui.setupUi(self)
        #self.ask_unsaved = qtw.QMessageBox.question()
        self.error_unsaved = qtw.QErrorMessage()

        self.x = 0
        self.unsaved = False
        self.edited_row_col_data = []
        '''
        self.directory = Path(__file__).absolute().parent        #directory hvor python scriptet og data base ligger
        with open(self.directory / 'config.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.db_file = data['db_name']
        '''
        self.db_file = dbfile
        
        self.ui.spinBox_ukenr.valueChanged.connect(self.spinBox_ukenr_change)
        
        #self.ui.tableWidget.cellChanged.connect(self.tabell_endret)
        self.ui.pushButton_save.clicked.connect(self.savebutton_clicked)
        self.ui.pushButton_cancel.clicked.connect(self.cancelbutton_clicked)
        self.ui.tableWidget.clicked.connect(self.valuetablechange)
        self.ui.tableWidget.cellDoubleClicked.connect(self.dobbelClickedTable)
        #self.move(1225,414)  
          

        self.fylltebel(self.arg)

    @qtc.pyqtSlot(str)
    def selectedDay_Changed(self,datostr):
        #print(datostr)
        ukenr=bjtime.getweeknr(self, datostr)
        self.ui.spinBox_ukenr.setValue(ukenr)
        #self.oppdatertabel(ukenr)

    def donothing(self):
        print('do nothing' + str(self.x))
        self.x = self.x + 1

    def savebutton_clicked(self):
        self.ui.tableWidget.blockSignals(False)
        self.unsaved=False
        self.ui.spinBox_ukenr.setEnabled(True)
        self.ui.pushButton_save.setEnabled(False)
        self.ui.pushButton_cancel.setEnabled(False)

        #print(self.edited_row_col_data)  
        timedb.save_edited_row_col(self, self.db_file, self.edited_row_col_data)
        self.db_saved.emit('db_saved')                                              #send signal to main 
        self.edited_row_col_data=[]

    def cancelbutton_clicked(self):
        self.ui.tableWidget.blockSignals(False)
        self.unsaved=False
        self.ui.spinBox_ukenr.setEnabled(True)
        self.ui.pushButton_save.setEnabled(False)
        self.ui.pushButton_cancel.setEnabled(False)         
        self.oppdatertabel(self.ui.spinBox_ukenr.value())
        self.edited_row_col_data= []        

    def dobbelClickedTable(self, idx):
        for idx in self.ui.tableWidget.selectionModel().selectedIndexes():
            row = idx.row()
            column = idx.column()
        #print('row ', str(row), '  column ', str(column))
        data=self.ui.tableWidget.item(row,column).text()
        #print('data = ', data)
        
        if column==10:      # collone registrert
            if data=='0':       # endre til registrert
                data='1'
            else:
                data='0'      # endre til uregistrert
        
            self.ui.tableWidget.setItem(row,column, qtw.QTableWidgetItem(data))

    def valuetablechange(self):
        self.ui.tableWidget.cellChanged.connect(self.tabell_endret)
    def tabell_endret(self):
        #---------------------
        for idx in self.ui.tableWidget.selectionModel().selectedIndexes():
            row = idx.row()
            column = idx.column()
        #print('row ', str(row), '  column ', str(column))
        data=self.ui.tableWidget.item(row,column).text()
        dbidstr=self.ui.tableWidget.item(row,0).text()
        dbid=int(dbidstr)
        #print('data = ', data)

        ifexist = (row,column,dbid,data)
        if ifexist not in self.edited_row_col_data:
            self.edited_row_col_data.append((row,column,dbid,data))
             
        #-------------------------        
        self.ui.pushButton_save.setEnabled(True)
        self.ui.pushButton_cancel.setEnabled(True)
        self.unsaved=True
        self.ui.spinBox_ukenr.setEnabled(False)

    def spinBox_ukenr_change(self):
        l_ukenr=self.ui.spinBox_ukenr.value()
        if self.unsaved:
            self.save_dialog()
            l_ukenr=l_ukenr -1
            self.oppdatertabel(l_ukenr)

        else:
            self.oppdatertabel(l_ukenr)
    
    def save_dialog(self):
        msg=qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Question)
        msg.setText('Do you want to save')
        msg.setWindowTitle("UnSaved data")
        msg.setStandardButtons(qtw.QMessageBox.Save | qtw.QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()
        print('value of pressed message box button:', retval)

    def msgbtn(self,i):
        print ('saved knapp = ', i.text())
        if i.text()=='Save':
            self.button_clicked()
            
        else:
            s_ukenr=self.ui.spinBox_ukenr.value()
            #s_ukenr=s_ukenr-1
            print('ukenr spin = ', str(s_ukenr))
            #self.ui.spinBox_ukenr.setValue= s_ukenr
            

    
    def oppdatertabel(self, ukenr):
        self.ui.tableWidget.blockSignals(True)
        self.fylltebel(ukenr)
        self.ui.tableWidget.blockSignals(False)


        

        

    def fylltebel(self, ukenr):
              
        ukestr=str(ukenr)
        #print(ukestr)
        
        sqldata=timedb.LoadTimeDataUkenr(self, self.db_file, ukestr)
        
        #print(sqldata)
        self.ui.tableWidget.clearContents()
        ##self.tableWidget.clear()

        #Fjerne gamle linjer i tabellen hvis eksisterer
        
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
                if colum_number==11:
                    item.setFlags(flags)
                if colum_number==12:
                    item.setFlags(flags)
                if colum_number==13:
                    item.setFlags(flags)
                self.ui.tableWidget.setItem(row_number,colum_number,item)
        