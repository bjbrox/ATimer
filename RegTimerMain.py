from RegTimer_ui import Ui_MainWindow
from ShowTimer import showtimer
from ShowKundeForm import ShowKundeForm
from Resultat import showresultat
from ShowOvertid import showovertid
from dbsqlite import timedb, kunderdb, getAtimer, NewDatabase
from timeclass import BJtimeclass as bjtime
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc 
from pathlib import Path
import pandas as pd
import sqlite3
import datetime
import yaml
import qdarkstyle


class AppMainWindow(qtw.QMainWindow):
    calender_endret_signal = qtc.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.directory = Path(__file__).absolute().parent        #directory hvor python scriptet og data base ligger
        with open(self.directory / 'config.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.db_file = data['db_name']
        self.mybud = data['bud']
        self.year = data['year']
        #print(self.db_file)
        db_exists = Path(self.db_file)
        if db_exists.exists():
            print('DB OK')
        else:
            print('no DB making new now !')
            new_db = NewDatabase(self.db_file)
            new_db.make_data_in_tabel(self.db_file,'Ratecard','category','overtidalternativer','fridager','kunder')

        self.viewindex=0
        self.viewtab=[]
        self.viewmode=False

        self.error_tableEmpty = qtw.QErrorMessage()
        #henter kunde database
        self.kundedf=kunderdb.getkunderdf(self,self.db_file)
        self.ui.comboBox_kunde.addItem('velg kunde')
        self.ui.comboBox_kunde.addItems(self.kundedf['name'] )
        
        #henter Workorder
        self.ui.comboBox_ordrenr.addItem('New WorkOrder')
        self.wodf= timedb.getLastWO(self,self.db_file)
        #self.wodf.drop_duplicates(subset ='ordrenr', keep= 'last', inplace = True)
        self.wodf.drop_duplicates(keep= 'last', inplace = True)
        #print(self.wodf)
        #selected_kunde=self.ui.comboBox_kunde.currentText()
        #print(selected_kunde)

        
        

        #henter categorys
        category_df = kunderdb.getcategory(self, self.db_file)
        self.ui.comboBox_category.addItems(category_df['category'])

        #henter ratecards
        ratecard_df = kunderdb.getratecard(self,self.db_file)
        self.ui.comboBox_ratecard.addItems(ratecard_df['ratecard'])

        #henter overtids valg
        overtidvalg_df= kunderdb.getovertidalternativer(self,self.db_file)
        self.ui.comboBox_overtid.addItems(overtidvalg_df['overtid_alt'])

        # Buttons pressed
        self.ui.button_viewOn.clicked.connect(self.viewOn_clicked)
        self.ui.button_viewOff.clicked.connect(self.viewOff_clicked)
        self.ui.button_left.clicked.connect(self.left_clicked)
        self.ui.button_rigth.clicked.connect(self.rigth_clicked)
        self.ui.button_save.clicked.connect(self.save_clicked)
        self.ui.button_delete.clicked.connect(self.delete_clicked)

        
        # Calender endret
        self.calender_endret()
        self.ui.calendarWidget.selectionChanged.connect(self.calender_endret)
        #self.calender_endret_signal.connect(self.show_timer.selectedDay_Changed)

        # comboBox.currentTextChanged.connect
        self.ui.comboBox_kunde.currentTextChanged.connect(self.selected_kunde_changes)
        self.ui.comboBox_category.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_ratecard.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_overtid.currentTextChanged.connect(self.updatetimepris)

        # legge til ny workorder nr
        self.ui.lineEdit_wonr.returnPressed.connect(self.new_wo)

        self.ui.doubleSpinBox_antalltimer.valueChanged.connect(self.doubleSpinBoxAntTimerValueChange)
        self.ui.textEdit_notat.textChanged.connect(self.textEditNotatChanged)

        # checkBox.
        self.ui.checkBox_timerregistrert.stateChanged.connect(self.checkBoxTimerRegistrertChanged)
        self.ui.checkBox_overtid.stateChanged.connect(self.checkBoxOvertidChanged)

        #Menu action .actionShow.triggered.connect(self.menushow_clicked)
        self.ui.actionOpen.triggered.connect(self.menuopen_db_clicked)
        self.ui.actionVis_timer.triggered.connect(self.menu_show_timer_clicked)
        self.ui.actionVis_Legg_til_kunder.triggered.connect(self.menu_Kunder_clicked)
        self.ui.actionVis_resultat.triggered.connect(self.menu_resultat_clicked)
        self.ui.actionHent_overtid_liste.triggered.connect(self.menu_overtid_liste_clicked)
        self.ui.actionNy.triggered.connect(self.menunew_db_clicked)
        self.ui.actionOm_programet.triggered.connect(self.menuOm_clicked)

        self.ui.statusbar.showMessage(f'Velkommen til time registrering program                    DB: {self.db_file}' )   #, 4000)

    @qtc.pyqtSlot(str)
    def ShowTimer_saved_signal(self):                       # når sowtimer tabell endres og lagres kjøres denne 
        #print('tabel in showtime is saved ')
        selected_day = self.ui.calendarWidget.selectedDate()
        datostr = bjtime.formatdato(self,str(selected_day))

        krfakturert_dag = timedb.getkrfakturert_dag(self, self.db_file, datostr)

        atimer=getAtimer(self.db_file, datostr)
        arbeidstimer=atimer.anttimer(self.db_file)
        self.ui.label_arbeids_timer_dag.setText(str(arbeidstimer))
        regtimer=timedb.getregtimer_dag(self, self.db_file, datostr)
        self.update_progressBar(krfakturert_dag[1],arbeidstimer,regtimer)

    @qtc.pyqtSlot(str)
    def ShowKunde_new_signal(self):                         # kjøres når det er blitt lagt inn ny kunde
        self.reload_db()

    def reload_db(self):
        with open('config.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.db_file = data['db_name']

        # comboBox.currentTextChanged.connect
        self.ui.comboBox_kunde.blockSignals(True)
        #self.ui.comboBox_kunde.currentTextChanged.connect(self.donothing)
        self.ui.comboBox_category.blockSignals(True) #.currentTextChanged.connect(self.donothing)
        self.ui.comboBox_ratecard.blockSignals(True) #.currentTextChanged.connect(self.donothing)
        self.ui.comboBox_overtid.blockSignals(True) #.currentTextChanged.connect(self.donothing)        
        self.ui.comboBox_kunde.clear()
        self.ui.comboBox_category.clear()
        self.ui.comboBox_overtid.clear()
        self.ui.comboBox_ratecard.clear()

        #henter kunde database
        self.kundedf=kunderdb.getkunderdf(self,self.db_file)
        
        self.ui.comboBox_kunde.addItem('velg kunde')
        self.ui.comboBox_kunde.addItems(self.kundedf.name )
        
        #henter categorys
        category_df = kunderdb.getcategory(self, self.db_file)
        self.ui.comboBox_category.addItems(category_df['category'])

        #henter ratecards
        ratecard_df = kunderdb.getratecard(self,self.db_file)
        self.ui.comboBox_ratecard.addItems(ratecard_df['ratecard'])

        #henter overtids valg
        overtidvalg_df= kunderdb.getovertidalternativer(self,self.db_file)
        self.ui.comboBox_overtid.addItems(overtidvalg_df['overtid_alt'])
        
        # comboBox.currentTextChanged.connect
        self.ui.comboBox_kunde.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_category.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_ratecard.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_overtid.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)

        #Menu action .actionShow.triggered.connect(self.menushow_clicked)
        #self.ui.actionOpen.triggered.connect(self.menuopen_db_clicked)
        self.calender_endret()
        self.ui.statusbar.showMessage(f'Velkommen til time registrering program                    DB: {self.db_file}' )   #, 4000)
    
    def resetInputBoxes(self):
            self.ui.comboBox_kunde.setCurrentIndex(0)
            self.ui.comboBox_overtid.setCurrentIndex(0)
            self.ui.doubleSpinBox_antalltimer.setValue(0)
            self.ui.textEdit_notat.clear()
            self.ui.checkBox_timerregistrert.setChecked(False)
            self.ui.checkBox_overtid.setChecked(False)
            self.ui.button_save.setEnabled(False)        

    def donothing(self):
        pass

    def selected_kunde_changes(self):
        self.updatetimepris()
        self.ui.comboBox_ordrenr.clear()
        self.ui.comboBox_ordrenr.addItem('New WorkOrder')

        selected_kunde=self.ui.comboBox_kunde.currentText()
        if selected_kunde != 'velg kunde':
            wo=self.wodf[self.wodf.isin([selected_kunde]).any(axis=1)]
            self.ui.comboBox_ordrenr.addItems(wo['ordrenr'])

    def new_wo(self):
        self.ui.comboBox_ordrenr.addItem(self.ui.lineEdit_wonr.text())
        self.ui.comboBox_ordrenr.setCurrentText(self.ui.lineEdit_wonr.text())
        df= pd.DataFrame({'kundename': [self.ui.comboBox_kunde.currentText()], 'ordrenr': [self.ui.lineEdit_wonr.text()] })
        #print(df, '\n')
        self.wodf=self.wodf.append(df, ignore_index = True)
        #print(self.wodf)
        self.ui.lineEdit_wonr.clear()
       

    def updatetimepris(self):
        #if self.viewmode==False:
        pris = self.gettimepris(self.kundedf, self.ui.comboBox_kunde.currentIndex(),self.ui.comboBox_kunde.currentText(), self.ui.comboBox_ratecard.currentText(), self.ui.comboBox_category.currentText(), self.ui.comboBox_overtid.currentText())
        self.ui.lineEdit_timepris.setText(str(pris))
        #print ('updatetimepris run')
        self.ui.button_save.setEnabled(True)
        
    
    def gettimepris(self,df, kunde_index, name, rate_card, category, overtid):
        res=0
        
        if kunde_index<0:
            kunde_index=0
        if kunde_index!=0:
            kunde_index=kunde_index-1
        #print(df._get_value(kunde_index,'timepris_chief'))
        res = df._get_value(kunde_index,'timepris_chief')
        if name!='velg kunde':
            if category!='Agreement Work':
                if rate_card=='Chief Consultant':
                    res = int(df._get_value(kunde_index,'timepris_chief'))
                elif rate_card=='Senior Consultant':
                    res = int(df._get_value(kunde_index,'timepris_senior'))
                elif rate_card=='Consultant':
                    res = int(df._get_value(kunde_index,'timepris_consult'))
                elif rate_card=='Travel':
                    res = int(df._get_value(kunde_index,'timepris_reise'))
                else:
                    res = 0

                if overtid != '0%':
                    if overtid == '100%':
                        res=res * 2
                    if overtid == '50%':
                        halv=res / 2
                        res=int(res + halv)

                    return res
            else:
                try:
                    res = int(df._get_value(kunde_index,'timepris_avtale'))
                    #print(res)
                    
                    if overtid != '0%':
                        if overtid == '100%':
                            res=res * 2
                        if overtid == '50%':
                            halv=res / 2
                            res=int(res + halv)
                    #return res
                except:
                    #print (' ingen avtale pris ')
                    self.error_tableEmpty.showMessage('Ingen avtale pris på denne kunden !')
                    self.ui.comboBox_category.setCurrentIndex(0)
                finally:
                    return res
        else:
            res = 0
        return res

   
    def save_clicked(self):
        sjekk=self.ui.comboBox_kunde.currentText()
        if sjekk != 'velg kunde':
            selected_day = self.ui.calendarWidget.selectedDate()
            datostr = bjtime.formatdato(self,str(selected_day))
            weeknr = bjtime.getweeknr(self,datostr)

            data=[]
            data.append(datostr)                                                                    #  dato             0
            data.append(self.ui.comboBox_kunde.currentText())                                       # kunde             1
            data.append(self.ui.comboBox_ordrenr.currentText())                                     # workorder nr      2
            data.append(self.ui.comboBox_category.currentText())                                    # category          3
            data.append(self.ui.comboBox_ratecard.currentText())                                    # ratecard          4
            data.append(self.ui.comboBox_overtid.currentText())                                     # Overtidvalg       5
            data.append(self.ui.doubleSpinBox_antalltimer.value())                                  # Antal timer       6
            data.append(int(self.ui.lineEdit_timepris.text()))                                      # henter timepris   7
            data.append(self.ui.textEdit_notat.toPlainText())                                       # notater           8
            data.append(self.ui.checkBox_timerregistrert.isChecked())                               # timer registrert? 9  
            data.append(self.ui.checkBox_overtid.isChecked())                               # overtid levert ?  10
            data.append(weeknr) 

            if self.viewmode==True:
                idx=self.viewtab[self.viewindex][0]
                timedb.updateTimeRecord(self, self.db_file, idx, data)
                self.updateViewtab()
                self.ui.button_save.setEnabled(False)
                self.ui.statusbar.showMessage(f'Updated Record {str(idx)} to Database', 4000)
            else:
                timedb.insertTimeRecord(self, self.db_file, data)
                self.calender_endret()
                self.resetInputBoxes()
                self.ui.statusbar.showMessage(f'Saved to DataBase : {self.db_file}', 4000)  
        self.updateTimeRegInfo()

    def delete_clicked(self):
        #print('viewindex ',str(self.viewindex))
        #print('tabel size ',str(len(self.viewtab)))
        index=self.viewindex
        if index>=0 and len(self.viewtab)>0:                                                   # er det poster i tabell
            idx=self.viewtab[self.viewindex][0]
            if self.viewmode==True and index!=0:                                               # sletter post i tabell
                timedb.deleteSqliteRecord(self, self.db_file, idx)
                self.updateViewtab()
                lengdetab=len(self.viewtab)
                if lengdetab>0:
                    index=index-1
                    self.viewindex=index
                #else:
                #    self.error_tableEmpty.showMessage('Ingen flere Record denne dagen !')
                self.viewUpdate()
                self.ui.statusbar.showMessage(f'Deleted Record {str(idx)} in the Database', 4000)      
            elif self.viewmode==True and index==0:                                             # sletter første post i tabell
                timedb.deleteSqliteRecord(self, self.db_file, idx)
                self.updateViewtab()
                if len(self.viewtab)==0:
                    self.error_tableEmpty.showMessage('Ingen flere Record denne dagen')
                    self.viewOff_clicked()    
                self.viewUpdate()
                #self.error_tableEmpty.showMessage('Ingen flere Record denne dagen !')
                self.ui.statusbar.showMessage(f'Deleted Record {str(idx)} in the Database', 4000)
        else:                                                                                           # ingen poster i tabell
            self.error_tableEmpty.showMessage('Ingen flere Record denne dagen')
            self.viewOff_clicked()
        self.updateTimeRegInfo()
        #print(len(self.viewtab))
        #print(self.viewindex)

    def checkBoxTimerRegistrertChanged(self):
        self.ui.button_save.setEnabled(True)

    def checkBoxOvertidChanged(self):
        self.ui.button_save.setEnabled(True)

    def doubleSpinBoxAntTimerValueChange(self):
        self.ui.button_save.setEnabled(True)
    
    def textEditNotatChanged(self):
        self.ui.button_save.setEnabled(True)

    def viewOn_clicked(self):
        self.updateViewtab()
        #print(type(self.kundedf))
        #print(len(self.viewtab))
        #print(self.viewtab)
        if len(self.viewtab)!=0:
            self.viewmode=True
            #self.viewindex=0
            
            
            self.ui.button_viewOn.setEnabled(False)
            self.ui.button_viewOff.setEnabled(True)
            self.ui.button_delete.setEnabled(True)
            #self.ui.button_left.setEnabled(True)
            self.ui.button_rigth.setEnabled(True)

            self.viewUpdate()
            self.ui.statusbar.showMessage('View reg time on selected day', 4000)
        else:
            self.error_tableEmpty.showMessage('Ingen Record denne dagen !')

    def viewOff_clicked(self):
        self.viewmode=False
        self.ui.button_viewOn.setEnabled(True)
        self.ui.button_viewOff.setEnabled(False)
        self.ui.button_delete.setEnabled(False)
        self.ui.button_left.setEnabled(False)
        self.ui.button_rigth.setEnabled(False)

        self.resetInputBoxes()
        #print(self.viewtab)
        self.viewtab=[]
        self.ui.statusbar.showMessage('Input reg time on selected day', 4000)
    
    def left_clicked(self):
        if self.viewindex > 0:
            self.viewindex = self.viewindex -1
            self.ui.button_left.setEnabled(True)
            self.ui.button_rigth.setEnabled(True)
            if self.viewindex == 0:
                self.ui.button_left.setEnabled(False)
        #print('left ', str(self.viewindex), 'length ', len(self.viewtab))
        self.viewUpdate()

    def rigth_clicked(self):
        if self.viewindex < len(self.viewtab) -1:
            self.viewindex = self.viewindex +1
            self.ui.button_rigth.setEnabled(True)
            self.ui.button_left.setEnabled(True)
            if self.viewindex == len(self.viewtab) -1:
                self.ui.button_rigth.setEnabled(False)
        #print('rigth ', str(self.viewindex), 'length ', len(self.viewtab))
        self.viewUpdate()

    def menuopen_db_clicked(self):
        dbfilename=self.open_file()
        data = {'db_name':'database.db'}
        data['db_name'] = dbfilename
        #db= data['db_name']
        #print(db)
        #print(data)
        
        with open('config.yml','w') as f:
            f.write( yaml.dump(data, default_flow_style=False))
        
        self.ui.statusbar.showMessage(f'DataBase : {dbfilename}', 4000)
        self.reload_db()
    
    def menunew_db_clicked(self):
        dbfilename=self.new_file()
        data = {'db_name':'database.db'}
        data['db_name'] = dbfilename
        #print(data)

        with open('config.yml','w') as f:
            f.write( yaml.dump(data, default_flow_style=False))
        
        self.ui.statusbar.showMessage(f'DataBase : {dbfilename}', 4000)
        new_db = NewDatabase(dbfilename)    #Lager ny db file
        new_db.make_data_in_tabel(dbfilename,'Ratecard','category','overtidalternativer','fridager','kunder')    #fyller tabeller fra Excel filer fra /NewDBConfig        
        self.reload_db()

    def menu_show_timer_clicked(self):
        selected_day = self.ui.calendarWidget.selectedDate()
        dato = bjtime.formatdato(self, str(selected_day))
        uke=bjtime.getweeknr(self, dato)
        self.show_timer = showtimer(self.db_file, uke)  
        self.show_timer.ui.spinBox_ukenr.setValue(uke) 
        self.show_timer.ui.dateEdit.setDate(selected_day)
        self.calender_endret_signal.connect(self.show_timer.selectedDay_Changed) 
        self.show_timer.db_saved.connect(self.ShowTimer_saved_signal)               #knytter til Signal fra Showtimer
        self.show_timer.show()
        

    def menu_Kunder_clicked(self):
        self.show_kundeForm = ShowKundeForm(self.db_file)
        self.show_kundeForm.new_kunde_saved.connect(self.ShowKunde_new_signal)
        self.show_kundeForm.show()

    def menu_resultat_clicked(self):
        selected_day = self.ui.calendarWidget.selectedDate()
        year = bjtime.formatdato(self,str(selected_day))
        year = bjtime.get_year(self, year)
        
        self.show_resultat = showresultat(self.db_file, year, self.mybud)
        
        self.show_resultat.show()

    def menu_overtid_liste_clicked(self):
        self.show_overtid_liste = showovertid(self.db_file)
        self.show_overtid_liste.show()

    def menuOm_clicked(self):
        #NewDatabase.make_data_in_tabel(self,self.db_file,'Ratecard','category','overtidalternativer','fridager','kunder')
        #NewDatabase.make_data_in_tabel(self,self.db_file,'category')
        qtw.QMessageBox.about(self, 'ver 2.0',' Dette programmet er designet ved hjelp av PyQt5 \n Lisens under GNU General Public \n \n Utviklet av Brede Jensen email: brede.jensen@atea.no')
        #about.show()


    def updateViewtab(self):
        selected_day = self.ui.calendarWidget.selectedDate()
        datostr = bjtime.formatdato(self,str(selected_day))
        self.viewtab= timedb.LoadTimeDataDag(self, self.db_file ,datostr)
        self.viewindex=0
        #print(self.viewtab)

    
    def viewUpdate(self):

        self.ui.comboBox_kunde.blockSignals(True) #.currentTextChanged.connect(self.donothing)
        self.ui.comboBox_category.blockSignals(True) #.currentTextChanged.connect(self.donothing)
        self.ui.comboBox_ratecard.blockSignals(True) #.currentTextChanged.connect(self.donothing)
        self.ui.comboBox_overtid.blockSignals(True) #.currentTextChanged.connect(self.donothing)
        
        self.ui.textEdit_notat.blockSignals(True)
        self.ui.doubleSpinBox_antalltimer.blockSignals(True)
        self.ui.checkBox_timerregistrert.blockSignals(True)
        self.ui.checkBox_overtid.blockSignals(True)


        peker=self.viewindex
        if len(self.viewtab) > 0:
            #print(self.viewtab[peker][0])

            index=self.ui.comboBox_kunde.findText(self.viewtab[peker][2])
            if index >= 0:
                self.ui.comboBox_kunde.setCurrentIndex(index)

            #print(self.viewtab[peker][2],'->', index)
            self.ui.comboBox_ordrenr.clear()
            selected_kunde=self.ui.comboBox_kunde.currentText()
            if selected_kunde != 'velg kunde':
                wo=self.wodf[self.wodf.isin([selected_kunde]).any(axis=1)]
                self.ui.comboBox_ordrenr.addItems(wo['ordrenr'])
            #self.ui.comboBox_ordrenr.addItems(self.wodf['ordrenr'])
            index=self.ui.comboBox_ordrenr.findText(self.viewtab[peker][3])
            if index >= 0:
                self.ui.comboBox_ordrenr.setCurrentIndex(index) 

            index=self.ui.comboBox_category.findText(self.viewtab[peker][4])
            if index >= 0:    
                self.ui.comboBox_category.setCurrentIndex(index)

            index=self.ui.comboBox_ratecard.findText(self.viewtab[peker][5])     #, qtc.Qt.MatchFixedString)
            if index >= 0:
                self.ui.comboBox_ratecard.setCurrentIndex(index)
            
            #print(self.viewtab[peker][5],'->', index)
            
            index=self.ui.comboBox_overtid.findText(self.viewtab[peker][6])
            if index >= 0:    
                self.ui.comboBox_overtid.setCurrentIndex(index)
            
            self.ui.doubleSpinBox_antalltimer.setValue(self.viewtab[peker][7])
            self.ui.lineEdit_timepris.setText(str(self.viewtab[peker][8]))
            self.ui.textEdit_notat.setText(self.viewtab[peker][9])
            self.ui.checkBox_timerregistrert.setChecked(self.viewtab[peker][10])
            self.ui.checkBox_overtid.setChecked(self.viewtab[peker][11])   

        self.ui.comboBox_kunde.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_category.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_ratecard.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.comboBox_overtid.blockSignals(False) #.currentTextChanged.connect(self.updatetimepris)
        self.ui.textEdit_notat.blockSignals(False)
        self.ui.doubleSpinBox_antalltimer.blockSignals(False)
        self.ui.checkBox_timerregistrert.blockSignals(False)
        self.ui.checkBox_overtid.blockSignals(False)

    def updateTimeRegInfo(self):
        selected_day = self.ui.calendarWidget.selectedDate()
        datostr = bjtime.formatdato(self,str(selected_day))
                
        m = bjtime.get_mnd(self,datostr)
        y = bjtime.get_year(self,datostr)
        
        krfakturert_dag = timedb.getkrfakturert_dag(self, self.db_file, datostr)
        krfakturert_mnd = timedb.getkrfakturert_mnd(self, self.db_file, m)
        krfakturert_year = timedb.getkrfakturert_ar(self, self.db_file, y)

        self.ui.label_sum_dag.setText(str(krfakturert_dag[0]))
        self.ui.label_timer_dag_value.setText(str(krfakturert_dag[1]))
        self.ui.label_sum_mnd.setText(str(krfakturert_mnd[0]))
        self.ui.label_timer_mnd_value.setText(str(krfakturert_mnd[1]))
        self.ui.label_sum_ar.setText(str(krfakturert_year[0]))
        self.ui.label_timer_ar_value.setText(str(krfakturert_year[1]))

        atimer=getAtimer(self.db_file, datostr)
        arbeidstimer=atimer.anttimer(self.db_file)
        self.ui.label_arbeids_timer_dag.setText(str(arbeidstimer))
        regtimer=timedb.getregtimer_dag(self, self.db_file, datostr)
        self.update_progressBar(krfakturert_dag[1],arbeidstimer,regtimer)

        self.calender_endret_signal.emit(datostr)

    def calender_endret(self):

        self.updateTimeRegInfo()

        self.updateViewtab()
        if self.viewmode==True: 
            if len(self.viewtab)>0:
                self.ui.button_viewOn.setEnabled(False)
                self.ui.button_viewOff.setEnabled(True)
                self.ui.button_delete.setEnabled(True)
                self.ui.button_left.setEnabled(True)
                self.ui.button_rigth.setEnabled(True)            
                #self.updateViewtab()
                self.viewUpdate()
                #self.viewOn_clicked()
            else:
                self.viewmode=False
                self.ui.button_viewOn.setEnabled(True)
                self.ui.button_viewOff.setEnabled(False)
                self.ui.button_delete.setEnabled(False)
                self.ui.button_left.setEnabled(False)
                self.ui.button_rigth.setEnabled(False)

                self.resetInputBoxes()
                self.error_tableEmpty.showMessage('Ingen Record denne dagen slår av view modus!')




    def update_progressBar(self,value,atimer,reg):
        
        #self.progressBar.setMaximum(atimer)
        #self.progressBar.setValue(value)
        
        if atimer==0:
            self.ui.progressBar_time_reg.setMaximum(100)
            self.ui.progressBar_time_reg.setValue(100)
        elif value > atimer:
            #self.progressBar.setProperty("value",8)
            self.ui.progressBar_time_reg.setMaximum(atimer)
            self.ui.progressBar_time_reg.setValue(atimer)
        else:
            #self.progressBar.setProperty("value",value)
            self.ui.progressBar_time_reg.setMaximum(atimer)
            if type(value)==float:
                value=int(value)
            self.ui.progressBar_time_reg.setValue(value)
        
        if value==0:
            self.ui.progressBar_regCSMS.setMaximum(100)
            self.ui.progressBar_regCSMS.setValue(0)
        else:
            if type(value)==float:
                value=int(value)
            self.ui.progressBar_regCSMS.setMaximum(value)
            self.ui.progressBar_regCSMS.setValue(reg)  

    def open_file(self):
        #filename, _ = qtw.QFileDialog.setNameFilter(qtw.QFileDialog.getOpenFileName(),"*.db")
        #filename, _ = qtw.QFileDialog.getOpenFileName(None, "Select Database Fil ...", './', filter="*.db")
        filename, _ = qtw.QFileDialog.getOpenFileName(None, "Select Database Fil ...", filter="*.db")
        #print(filename)
        if filename!='':
            #with open(filename, 'r') as handle:
            #    text = handle.read()
            return filename            #str(f'Database {filename}')  
        else:
            filename=self.db_file
            return filename

    def new_file(self):
        filename = qtw.QFileDialog.getSaveFileName(None, "New DAtabase Fil ...", filter="*.db")
        print('new file')
        dbfil=filename[0]
        print(dbfil)
        if dbfil!='':
            NewDatabase(dbfil)
            return dbfil
        else:
            dbfil=self.db_file
            return dbfil
        
        



if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    vindu = AppMainWindow()
    vindu.setGeometry(100,100,1224,414)
    vindu.show()
    
    app.exec_()