import sqlite3
import yaml
import datetime
from datetime import date



class ResultatTimer:
    def __init__(self, dbfile, datoin):
        
        dt=self.formatdato(str(datoin))
        self.dato = dt
        #self.kunder_file = "kunderdb.db"
        #with open('config.yml') as f:
        #    data = yaml.load(f, Loader=yaml.FullLoader)
        #self.kunder_file = data['db_name']
        self.kunder_file = dbfile
    
    def formatdato(self, d):
        dt = datetime.datetime.strptime(d, '%Y-%m-%d')
        dato=dt.strftime('%d-%m-%Y')
        return dato

    def getOvertid_mnd(self, mnd):
        fd=0
        d=str(mnd)
        if len(d)==1:
            d='0'+d
        d='%-' + d +'-%'     #klargjør sql spørring med måned '-mnd-'        
        try:
            sqliteConnection = sqlite3.connect(self.kunder_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite fridag")
            
            sql_select_query = """SELECT dato, kundename, rate_card, overtid, timer, overtidlevert FROM timedb WHERE dato LIKE ? AND overtid !='0%';"""
            cursor.execute(sql_select_query, (d, ))
            
            fd=cursor.fetchall()
            #fd=fd[0]
            #print(fd)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return fd


    def dag_in_fri_db(self):
        fd=0
        try:
            sqliteConnection = sqlite3.connect(self.kunder_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite fridag")
            
            sql_select_query = """SELECT id, atimer FROM fridager WHERE fridag = ?"""
            cursor.execute(sql_select_query, (self.dato, ))
            #print(self.dato)
            fd=cursor.fetchone()
            #fd=fd[0]
            #print(fd)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return fd


    def isworkday(self):    #__repr__
        dag=self.getukedag()
        fdag=self.dag_in_fri_db()
        #print(fdag)
        if fdag != None:
            atimer=fdag[1]                    #hent atimer fra sqlite tabel 'fridager'
        elif dag == 'Lørdag':
            atimer=0
        elif dag == 'Søndag':
            atimer=0
        else:
            atimer=8

        if atimer==0:
            arbeidsdag=False
        else:
            arbeidsdag=True
        #print(atimer, arbeidsdag)
        result=(arbeidsdag, atimer)
        return result

    def weekday(self, i):
        switcher={
                7:'Søndag',
                1:'Mandag',
                2:'Tirsdag',
                3:'Onsdag',
                4:'Torsdag',
                5:'Fredag',
                6:'Lørdag'
             }
        return switcher.get(i,"invalid day")


    def getukedag(self):
        dt = datetime.datetime.strptime(self.dato, '%d-%m-%Y')
        ukedag = dt.isocalendar()[2]
        dagstr = self.weekday(ukedag)
        return dagstr

    def getuke(self):
        dt = datetime.datetime.strptime(self.dato, '%d-%m-%Y')
        uke = dt.isocalendar()[1]
        return uke

    '''def get_antOvertid(self, mnd):              #0=dato 1=k.name 2=category 3=overtid 4=timer 5=levert
        ant100=0
        ant50=0
        overtid=ResultatTimer(date(2021,4,1))
        result=overtid.getOvertid_mnd(mnd)
        for teller in result:
            #print(teller)
            if teller[3]=='100%':
                ant100=ant100 + teller[4]
            elif teller[3]=='50%':
                ant50=ant50 + teller[4]
            else:
                #print(teller[3])
                print('error ingen overtid reg !')
        return (ant100, ant50)
    '''

