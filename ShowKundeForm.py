from KundeForm import Ui_KundeForm
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from dbsqlite import kunderdb
from pathlib import Path
import qdarkstyle 
import yaml

class ShowKundeForm(qtw.QWidget):

    new_kunde_saved = qtc.pyqtSignal(str)

    def __init__(self, dbname, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_KundeForm()
        self.ui.setupUi(self)

        '''
        self.directory = Path(__file__).absolute().parent        #directory hvor python scriptet og data base ligger
        with open(self.directory / 'config.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.db_file = data['db_name']    
        '''
        self.db_file = dbname
        self.sqlkunder=kunderdb()
        self.viewmode=False
        self.kunder = self.sqlkunder.getkunderdf(self.db_file)
        self.ant_kunder = self.kunder.shape[0]  #len(self.kunder)
        #print(self.ant_kunder)
        #print(self.kunder)
        self.kpeker = 0

        self.ui.Button_save.clicked.connect(self.save_clicked)
        self.ui.Button_left.clicked.connect(self.left_clicked)
        self.ui.Button_right.clicked.connect(self.right_clicked)
        self.ui.Button_cancel.clicked.connect(self.cancel_clicked)
        self.ui.Button_nykunde.clicked.connect(self.nykunde_clicked)

    def show_kunde(self, peker):
        self.ui.lineEdit_kunde.setText(self.kunder.at[peker,'name'])
        self.ui.lineEdit_chief.setText(str(self.kunder.at[peker,'timepris_chief']))
        self.ui.lineEdit_senior.setText(str(self.kunder.at[peker,'timepris_senior']))
        self.ui.lineEdit_consultant.setText(str(self.kunder.at[peker,'timepris_consult']))
        self.ui.lineEdit_avtale.setText(str(self.kunder.at[peker,'timepris_avtale']))
        self.ui.lineEdit_travel.setText(str(self.kunder.at[peker,'timepris_reise']))
        self.ui.lineEdit_rabatt.setText(str(self.kunder.at[peker,'rabatt']))
        self.ui.lineEdit_km.setText(str(self.kunder.at[peker,'km']))
        

    def clear_lineEdit(self):
        self.ui.lineEdit_kunde.clear()
        self.ui.lineEdit_consultant.clear()
        self.ui.lineEdit_senior.clear()
        self.ui.lineEdit_chief.clear()
        self.ui.lineEdit_avtale.clear()
        self.ui.lineEdit_travel.clear()
        self.ui.lineEdit_rabatt.clear()
        self.ui.lineEdit_km.clear()

    def nykunde_clicked(self):
        self.viewmode=False
        self.ui.Button_save.setText('Save')
        self.ui.Button_cancel.setText('Cancel')
        self.ui.Button_nykunde.setEnabled(False)
        self.clear_lineEdit()        

    def save_clicked(self):
        kd=[]
        kd.append(self.ui.lineEdit_kunde.text())
        kd.append(self.ui.lineEdit_chief.text())
        kd.append(self.ui.lineEdit_senior.text())
        kd.append(self.ui.lineEdit_consultant.text())
        kd.append(self.ui.lineEdit_avtale.text())
        kd.append(self.ui.lineEdit_travel.text())
        kd.append(self.ui.lineEdit_rabatt.text())
        kd.append(self.ui.lineEdit_km.text())
        d=tuple(kd)
        if self.viewmode==False:
            self.sqlkunder.addkundeColumn(self.db_file, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])
            self.kunder = self.sqlkunder.getkunderdf(self.db_file)
            self.ant_kunder = self.kunder.shape[0]      # oppdaterer antall kunder i kunde tabell 
            
            #print(self.kunder)
            self.clear_lineEdit()
        else:
            #print(d)
            #print(self.kunder[self.kpeker][0])
            self.sqlkunder.updateKundeRecord(self.db_file,self.kunder.at[self.kpeker,'id'], kd)
            self.kunder = self.sqlkunder.getkunderdf(self.db_file)
            #self.sqlkunder.updatekundeColumn(self.db_file, self.kunder[self.kpeker][0], d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7] )
            self.clear_lineEdit()

        self.new_kunde_saved.emit('new_kunde_saved')

    def cancel_clicked(self):
        if self.viewmode==True:
            idx=self.kunder.at[self.kpeker,'id']
            #print(' ID delete ->',str(idx))
            #print('self.kpeker = ',str(self.kpeker))
            self.sqlkunder.deleteSqliteRecord(self.db_file, idx)
            self.kunder=self.kunder.drop(self.kpeker, axis=0)
            self.kunder=self.kunder.reset_index(drop=True)
            self.clear_lineEdit()
            if self.kpeker>0:
                self.kpeker=self.kpeker-1
            else:
                self.kpeker=0
            self.ant_kunder = self.kunder.shape[0]      # oppdaterer antall kunder i kunde tabell 
            #print(self.kunder)
            self.show_kunde(self.kpeker)
        
    def right_clicked(self):
        if self.ant_kunder>self.kpeker and self.viewmode==True:
            ant=self.ant_kunder - 1
            if self.kpeker==ant:
                self.kpeker=self.ant_kunder-1
            else: 
                self.kpeker=self.kpeker+1
            if self.kpeker< self.ant_kunder:
                self.show_kunde(self.kpeker)

        if self.viewmode==False:
            self.viewmode=True
            self.kpeker=self.ant_kunder - 1
            self.show_kunde(self.kpeker)
            self.ui.Button_save.setText('Update')
            self.ui.Button_cancel.setText('Delete')
            self.ui.Button_nykunde.setEnabled(True)
        #print(self.kpeker)


    def left_clicked(self):
        if self.viewmode==True:
            if self.kpeker>0:
                self.kpeker=self.kpeker-1
                self.clear_lineEdit()
                self.show_kunde(self.kpeker)
        
        if self.viewmode==False:
            self.viewmode=True
            self.kpeker=0
            self.show_kunde(self.kpeker)
            self.ui.Button_save.setText('Update')
            self.ui.Button_cancel.setText('Delete')
            self.ui.Button_nykunde.setEnabled(True)
        #print(self.kpeker)