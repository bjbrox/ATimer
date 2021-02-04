from ResultatForm_ui import Ui_ResultatForm
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import pandas as pd
from dbsqlite import timedb, kunderdb, getAtimer
from Atimer_calendar import Atimer_calendar
from ResultatPlot import ResultatPlot
import qdarkstyle

class showresultat(qtw.QWidget):
    
    def __init__(self, dbfile, yearinput, mybud, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_ResultatForm()
        #self.setGeometry(1325,100,2533,698) 
        self.ui.setupUi(self)
        
        self.error_unsaved = qtw.QErrorMessage()

        self.db_file = dbfile
        self.year=yearinput
        self.mybud=mybud
        
        '''self.resultatTabel = pd.DataFrame({'mnd': ['Jan','Feb','Mar','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dec','SUM'],
                                        'ant dager': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'ant timer': [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        '% av budsj': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'budsjett': [0.5,0,0,0,0,0,0,0,0,0,0,0,1800000],
                                        'Akk.budsjett': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'Akk.bud 75%': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'Reelt': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'Akk.reelt': [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'Avvik': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        '%Avvik': [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'ant f.timer': [0.5,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'f.grad': [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'f.timer overtid': [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                        'Fakt. u/overtid':[0,0,0,0,0,0,0,0,0,0,0,0,0]
                                        })
        '''
        self.resultatTabel = pd.DataFrame(columns=['mnd','ant dager','ant timer','% av budsj','budsjett','Akk.budsjett','Akk.bud 75%',
                                                'Reelt','Akk.reelt','Avvik','%Avvik','ant f.timer','f.grad','f.timer overtid','Fakt. u/overtid'],
                                                index=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
        self.resultatTabel.at[0,'mnd']='Jan'
        self.resultatTabel.at[1,'mnd']='Feb'
        self.resultatTabel.at[2,'mnd']='Mar'
        self.resultatTabel.at[3,'mnd']='Apr'
        self.resultatTabel.at[4,'mnd']='Mai'
        self.resultatTabel.at[5,'mnd']='Jun'
        self.resultatTabel.at[6,'mnd']='Jul'
        self.resultatTabel.at[7,'mnd']='Aug'
        self.resultatTabel.at[8,'mnd']='Sep'
        self.resultatTabel.at[9,'mnd']='Okt'
        self.resultatTabel.at[10,'mnd']='Nov'
        self.resultatTabel.at[11,'mnd']='Dec'
        self.resultatTabel.at[12,'mnd']='_____________'
        self.resultatTabel.at[13,'mnd']='SUM'

        #print(self.year,' type ', type(self.year))
        #print(self.db_file)

        self.fylltabel(self.resultatTabel)
        #print(self.resultatTabel)
        model = DataFrameModel(self.resultatTabel)
        #self.ui.tableView.setAlternatingRowColors(True)
        #self.ui.tableView.setStyleSheet('gridline-color: rgb(191,191,191)')
        
        self.ui.tableView.setModel(model)
        #self.ui.tableWidget.setModel(model)

        self.ui.Button_Akk.clicked.connect(self.button_Akk_Clicked)
        self.ui.Button_Bud.clicked.connect(self.button_Bud_Clicked)

    def button_Akk_Clicked(self):
        myplot=ResultatPlot(self.db_file, self.mybud, self.year)
        myplot.showPlot("Akkumulert Bud")

    def button_Bud_Clicked(self):
        myplot=ResultatPlot(self.db_file, self.mybud, self.year)
        myplot.showPlot("Bud")

    def fylltabel(self, data):
        sum_dager=0
        sum_timer=0
        sum_bud=0
        sum_prosent_av_bud=0
        akk_bud=0
        sum_kr=0
        sum_kr_mnd=0
        sum_kr_akk_mnd=0
        sum_kr_mnd_u_overtid=0
        tot_timer_overtid=0
        tot_sum_kr_u_overtid=0
        sum_ftimer=0
        sum_avvik=0
        data.at[13,'budsjett']= self.mybud #1800000
        spaceline='_____________'

        for index_mnd in range(12):     # tabell starter på 0=Jan 1=Feb 2=Mar  osv.
            maned=index_mnd+1
            if index_mnd==11:
                data.at[index_mnd+1,'ant dager']=spaceline
                data.at[index_mnd+1,'ant timer']=spaceline
                data.at[index_mnd+1,'% av budsj']=spaceline
                data.at[index_mnd+1,'budsjett']=spaceline
                data.at[index_mnd+1,'Akk.budsjett']=spaceline
                data.at[index_mnd+1,'Akk.bud 75%']=spaceline
                data.at[index_mnd+1,'Reelt']=spaceline
                data.at[index_mnd+1,'Akk.reelt']=spaceline
                data.at[index_mnd+1,'Avvik']=spaceline
                data.at[index_mnd+1,'%Avvik']=spaceline
                data.at[index_mnd+1,'ant f.timer']=spaceline
                data.at[index_mnd+1,'f.grad']=spaceline
                data.at[index_mnd+1,'f.timer overtid']=spaceline
                data.at[index_mnd+1,'Fakt. u/overtid']=spaceline
                

            ant=Atimer_calendar(self.db_file)        
            
            timer, dager =ant.ant_atimer_mnd(maned,int(self.year))
            
            data.at[index_mnd,'ant dager']=dager
            data.at[index_mnd,'ant timer']=timer
            sum_dager=sum_dager+dager
            sum_timer=sum_timer+timer

            sum_kr_mnd, sumtimer_mnd = timedb.getkrfakturert_mnd(self, self.db_file, maned)
            sum_kr_mnd_u_overtid, timer_overtid_mnd = ant.getkrfakturert_u_overtid_mnd(maned)
            sum_ftimer=sum_ftimer+sumtimer_mnd

            if sum_kr_akk_mnd==0:
                sum_kr_akk_mnd = sum_kr_mnd
            else:
                sum_kr_akk_mnd = data.at[index_mnd-1,'Akk.reelt'] + sum_kr_mnd
            
            sum_kr = sum_kr + sum_kr_mnd
            tot_timer_overtid=tot_timer_overtid+timer_overtid_mnd
            tot_sum_kr_u_overtid=tot_sum_kr_u_overtid + sum_kr_mnd_u_overtid
            
            if sum_kr_mnd>0:
                data.at[index_mnd,'Reelt'] = sum_kr_mnd
                data.at[index_mnd,'Akk.reelt'] = sum_kr_akk_mnd
                data.at[index_mnd,'ant f.timer'] = sumtimer_mnd
                data.at[index_mnd,'Fakt. u/overtid'] = sum_kr_mnd_u_overtid
                data.at[index_mnd,'f.timer overtid'] = timer_overtid_mnd
            

            
            
            

        data.at[13,'ant dager']=sum_dager
        data.at[13,'ant timer']=sum_timer
        data.at[13,'Reelt'] = round(sum_kr, 2)
        data.at[13,'ant f.timer'] = sum_ftimer
        data.at[13,'f.timer overtid'] = tot_timer_overtid
        data.at[13,'Fakt. u/overtid'] = tot_sum_kr_u_overtid

        for index_mnd in range(12):
            maned=index_mnd+1
            prosent = data.at[index_mnd,'ant dager'] / sum_dager * 100
            mnd_bud = data.at[13,'budsjett'] * prosent / 100
            if akk_bud == 0:
                akk_bud=mnd_bud
            else:
                akk_bud=mnd_bud + data.at[index_mnd -1,'Akk.budsjett']
            data.at[index_mnd,'% av budsj']=round(prosent,2)
            data.at[index_mnd,'budsjett']=round(mnd_bud,1)
            data.at[index_mnd,'Akk.budsjett']=round(akk_bud,1)
            data.at[index_mnd,'Akk.bud 75%']=round(akk_bud*0.75,1)
            sum_bud=sum_bud + mnd_bud
            sum_prosent_av_bud=sum_prosent_av_bud+ prosent
        data.at[13,'% av budsj']=round(sum_prosent_av_bud,2)
        data.at[13,'budsjett']=round(sum_bud,2)

        for index_mnd in range(12):
            maned=index_mnd+1
            if data.at[index_mnd,'Reelt']>0:
                # Avvik
                data.at[index_mnd,'Avvik']=round(data.at[index_mnd,'Reelt'] - data.at[index_mnd,'budsjett'],2)
                sum_avvik=sum_avvik+data.at[index_mnd,'Avvik']
                # %Avvik
                data.at[index_mnd,'%Avvik']=round(data.at[index_mnd,'Akk.reelt'] / data.at[index_mnd,'Akk.budsjett'] *100, 2)
                # fakturerings grad
                data.at[index_mnd,'f.grad']=round(data.at[index_mnd,'ant f.timer'] / data.at[index_mnd,'ant timer'] *100, 2)

        data.at[13,'Avvik'] = round(sum_avvik,2)
        data.at[13,'f.grad'] = round(data.at[13,'ant f.timer'] * 100 / data.at[13,'ant timer'], 2)
        

        return(data)


class DataFrameModel(qtc.QAbstractTableModel):
    DtypeRole = qtc.Qt.UserRole + 1000
    ValueRole = qtc.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = qtc.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @qtc.pyqtSlot(int, qtc.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: qtc.Qt.Orientation, role: int = qtc.Qt.DisplayRole):
        if role == qtc.Qt.DisplayRole:
            if orientation == qtc.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return qtc.QVariant()

    def rowCount(self, parent=qtc.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=qtc.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=qtc.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return qtc.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == qtc.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return qtc.QVariant()

    def roleNames(self):
        roles = {
            qtc.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles