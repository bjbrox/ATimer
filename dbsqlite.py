import sqlite3
import yaml
import datetime
import pandas as pd
from pathlib import Path

class timedb(object):
    def __init__(self):
        #self.kunder_file = "kunderdb.db"
        '''
        init
        '''

    def getLastWO(self, db_file):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            #print("Connected to SQLite")
            df = pd.read_sql_query("SELECT kundename, ordrenr FROM timedb ORDER BY id DESC LIMIT 200", sqliteConnection)

            #cursor.close()
            sqliteConnection.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed ")
                #print(pris)
                return (df)

    
    def getkrfakturert_dag(self, db_file, d):
        #fakturert=0
        sumtimer=0
        pris=0
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite") 

            sql_select_query = """SELECT timer, timepris FROM timedb WHERE dato=?;"""
            res=cursor.execute(sql_select_query, (d,))
            #self.kunder=cursor.fetchall()
            for t in res:
                pris=t[1]*t[0]+pris
                sumtimer=sumtimer + t[0]
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return (pris, sumtimer)

    def getkrfakturert_mnd(self, db_file, mnd):
        #fakturert=0
        sumtimer=0
        pris=0
        d=str(mnd)
        if len(d)==1:
            d='0'+d
        d='%-' + d +'-%'
        #print(d)
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite to get MND pris") 

            sql_select_query = """SELECT timer, timepris FROM timedb WHERE dato LIKE ?;"""
            cursor.execute(sql_select_query, (d,))
            res=cursor.fetchall()
            #print(res)
            for t in res:
                pris=t[1]*t[0]+pris
                if t[1]!=0:                         # ikke tell med HR timer der timespris = 0
                    sumtimer=sumtimer + t[0]
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed mnd ")
                #print(pris)
                return (pris, sumtimer)    # kr fakturert i mnd + sum timer fakturert

    def getkrfakturert_ar(self, db_file, d):
        #fakturert=0
        sumtimer=0
        pris=0
        length = len(d)
        d=d[length - 4:]
        d='%' + d      # tekst som inneholder årstallet spørring
        #print(d)
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite to get AR pris") 

            sql_select_query = """SELECT timer, timepris FROM timedb WHERE dato LIKE ?;"""
            cursor.execute(sql_select_query, (d,))
            res=cursor.fetchall()
            #print(res)
            for t in res:
                pris=t[1]*t[0]+pris
                sumtimer=sumtimer + t[0]
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table ar", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed ar ")
                #print(pris)
                return (pris, sumtimer)
    
    def getregtimer_dag(self, db_file, d):
        
        sumtimer=0
        
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite") 

            sql_select_query = """SELECT timer FROM timedb WHERE dato=? AND registrert=1;"""
            res=cursor.execute(sql_select_query, (d,))
            
            for t in res:
                sumtimer=sumtimer + t[0]
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return sumtimer

    def updateMultipleColumns(self, db_file, id, dato, kunde, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, weeknr):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            sqlite_update_query = """Update timedb set dato = ?, kundename = ?, ordrenr = ?, category = ?, rate_card = ?, overtid = ?, timer = ?, timepris = ?, notes = ?, registrert = ?, overtidlevert = ?, weeknr = ? where id = ?"""
            columnValues = (dato, kunde, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, weeknr, id)
            cursor.execute(sqlite_update_query, columnValues)
            sqliteConnection.commit()
            #print("Multiple columns in timedb updated successfully")
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update multiple columns of sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("sqlite connection is closed")

    def save_edited_row_col(self, db_file, row_col_data):
        #print(row_col_data)
        #dbid=row_col_data[0][2]
        #registrert=row_col_data[0][3]
        #print('id -> ',str(dbid), ' data -> ', str(registrert))
        
        for tab in row_col_data:
            #print(tab)
            dbid=tab[2]
            registrert=tab[3]
            col=tab[1]
            #print('id -> ',str(dbid), ' registert -> ', str(registrert))
            if col==10:                                                             # col 10 = registrert feltet
                try:
                    sqliteConnection = sqlite3.connect(db_file)
                    cursor = sqliteConnection.cursor()
                    #print("Connected to SQLite")

                    sqlite_update_query = """Update timedb set registrert = ? where id = ?"""
                    columnValues = (registrert, dbid)
                    cursor.execute(sqlite_update_query, columnValues)
                    sqliteConnection.commit()
                    #print("Multiple columns in timedb updated successfully")
                    sqliteConnection.commit()
                    cursor.close()

                except sqlite3.Error as error:
                    print("Failed to update multiple columns of sqlite table", error)
                finally:
                    if (sqliteConnection):
                        sqliteConnection.close()
                        #print("sqlite connection is closed")
            
    def insertTimeRecord(self, db_file, data):
        indata=tuple(data)
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            sqlite_insert_query = """INSERT INTO timedb (dato, kundename, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, ukenr) VALUES {};""".format(indata)
            #columnValues = (dato, kunde, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, weeknr)
            cursor.execute(sqlite_insert_query)
            #print("Multiple columns in timedb updated successfully")
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update multiple columns of sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("sqlite connection is closed")
                 
    def updateTimeRecord(self, db_file, idx, data):
        data.append(idx)
        #indata=tuple(data)
        #print(indata)
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            #sqlite_update_query = """Update timedb set (dato, kundename, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, ukenr) WHERE id = ?;""".format(indata)
            sqlite_update_query = """Update timedb set dato = ?, kundename = ?, ordrenr = ?, category = ?, rate_card = ?, overtid = ?, timer = ?, timepris = ?, notes = ?, registrert = ?, overtidlevert = ?, ukenr = ? where id = ?"""
            #columnValues = (dato, kunde, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, weeknr)
            cursor.execute(sqlite_update_query, data)
            #print("Multiple columns in timedb updated successfully")
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update multiple columns of sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("sqlite connection is closed")
                #                  
    def updateOvertidRecord(self, db_file, idx, data):
        data=[data, idx]
        #indata=tuple(data)
        #print(indata)
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            #sqlite_update_query = """Update timedb set (dato, kundename, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, ukenr) WHERE id = ?;""".format(indata)
            sqlite_update_query = """Update timedb set overtidlevert = ? where id = ?"""
            #columnValues = (dato, kunde, ordrenr, category, rate_card, overtid, timer, timepris, notes, registrert, overtidlevert, weeknr)
            cursor.execute(sqlite_update_query, data)
            #print("Multiple columns in timedb updated successfully")
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update multiple columns of sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("sqlite connection is closed")
                #               
    def deleteSqliteRecord(self, db_file, id):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            sql_update_query = """DELETE FROM timedb WHERE id = ?"""
            cursor.execute(sql_update_query, (id, ))
            sqliteConnection.commit()
            #print("Record deleted successfully")

            cursor.close()
        except sqlite3.Error as error:
            print("Failed to delete reocord from a sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("sqlite connection is closed")
                #     

    def LoadTimeDataUkenr(self, db_file, where):
        where='%'+where+'%'
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            sql_select_query = """SELECT * FROM timedb WHERE ukenr LIKE ?;"""
            cursor.execute(sql_select_query, (where,))
            result=cursor.fetchall()
            #print(result)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return result

    def LoadOvertid(self, db_file):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            sql_select_query = """SELECT * FROM timedb 
                                WHERE overtid = "100%" 
                                AND overtidlevert = "0" OR overtid = "50%" 
                                AND overtidlevert = "0" ORDER BY date(dato);"""
            cursor.execute(sql_select_query)
            result=cursor.fetchall()
            #print(result)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return result    
    
    def LoadTimeDataDag(self, db_file, where):
        #where='%'+where+'%'
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            sql_select_query = """SELECT * FROM timedb WHERE dato LIKE ?;"""
            cursor.execute(sql_select_query, (where,))
            result=cursor.fetchall()
            #print(result)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
                return result

class kunderdb(object):
    #def __init__(self):
        #self.kunder_file = "kunderdb.db"
        #with open('config.yml') as f:
        #    data = yaml.load(f, Loader=yaml.FullLoader)
        #self.db_file = data['db_name']



    def getkunderdf(self,db_file):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            #print("Connected to SQLite")
            df = pd.read_sql_query("SELECT id, name, timepris_chief, timepris_senior, timepris_consult, timepris_avtale, timepris_reise, rabatt, km  FROM kunder", sqliteConnection)

            #cursor.close()
            sqliteConnection.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed ")
                #print(pris)
                return (df)

    #  -------------     legge til og fjerne kunder i basen

    def addkundeColumn(self, db_file, name, tpchief, tpsenior, tpconsult, tpavtale, tptravel, rabatt, km):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_insert_query = """INSERT INTO kunder 
                                (name, 
                                timepris_chief, 
                                timepris_senior, 
                                timepris_consult, 
                                timepris_avtale,
                                timepris_reise,
                                rabatt,
                                km)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
            columnValues = (name, tpchief, tpsenior, tpconsult, tpavtale, tptravel, rabatt, km)
            cursor.execute(sqlite_insert_query, columnValues)
            sqliteConnection.commit()
            print("columns added successfully")
            sqliteConnection.commit()
            cursor.close()
            ##################################################   self.clear_lineEdit()

        except sqlite3.Error as error:
            print("Failed to add columns of sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("sqlite connection is closed")

    def updateKundeRecord(self, db_file, idx, data):
        idx=int(idx)
        data.append(idx)
        indata=tuple(data)
        print(indata)
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")
            sqlite_update_query = """UPDATE kunder SET name = ?,
                                timepris_chief = ?, 
                                timepris_senior = ?, 
                                timepris_consult = ?,
                                timepris_avtale = ?, 
                                timepris_reise = ?, 
                                rabatt = ?,
                                km = ? 
                                WHERE id = ?;"""
            cursor.execute(sqlite_update_query, indata)

            sqliteConnection.commit()
            print('comit to DB')
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to update multiple columns of sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("sqlite connection is closed")

    def deleteSqliteRecord(self, db_file, id):
        id=int(id)
        print(type(id))
        try:
            sqliteConnection = sqlite3.connect(db_file)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite file ->",str(db_file))

            sql_delete_query = """DELETE FROM kunder WHERE id = ?"""
            cursor.execute(sql_delete_query, (id, ))
            sqliteConnection.commit()
            print(f"Record {str(id)} deleted successfully")

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete reocord from a sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("sqlite connection is closed")


    # -----------------------------   Kunder slutt -----------------------------                            

    def getcategory(self,db_file):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            df = pd.read_sql_query("SELECT id, category FROM category",sqliteConnection)
            sqliteConnection.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table",error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed ")
                #print(pris)
                return (df)


    def getratecard(self,db_file):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            df = pd.read_sql_query("SELECT id, ratecard FROM Ratecard",sqliteConnection)
            sqliteConnection.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table",error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed ")
                #print(pris)
                return (df)

    def getovertidalternativer(self,db_file):
        try:
            sqliteConnection = sqlite3.connect(db_file)
            df = pd.read_sql_query("SELECT id, overtid_alt FROM overtidalternativer",sqliteConnection)
            sqliteConnection.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table",error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed ")
                #print(pris)
                return (df)

            
class getAtimer:
    def __init__(self, db_file, datoin):
        self.dato = datoin
        '''
        self.directory = Path(__file__).absolute().parent        #directory hvor python scriptet og data base ligger
        #self.kunder_file = "kunderdb.db"
        with open(self.directory / 'config.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.db_file = data['db_name']
        '''

    def dag_in_fri_db(self, db_file):
        fd=0
        try:
            sqliteConnection = sqlite3.connect(db_file)
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


    def anttimer(self, db_file):    #__repr__
        dag=self.getukedag()
        fdag=self.dag_in_fri_db(db_file)
        #print(type(fdag))
        if fdag != None:
            atimer=fdag[1]                    #hent atimer fra sqlite tabel 'fridager'
        elif dag == 'Lørdag':
            atimer=0
        elif dag == 'Søndag':
            atimer=0
        else:
            atimer=8        
        return atimer

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

class NewDatabase:
    def __init__(self, db_file):
        self.directory = Path(__file__).absolute().parent        #directory hvor python scriptet og data base ligger
        
        sql_create_timedb_table = """CREATE TABLE IF NOT EXISTS timedb (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        dato DATE NOT NULL,
                                        kundename TEXT,
                                        ordrenr STRING,
                                        category STRING NOT NULL,
                                        rate_card STRING NOT NULL,
                                        overtid STRING,
                                        timer NUMERIC(23, 5) NOT NULL,
                                        timepris INTEGER,
                                        notes TEXT NOT NULL,
                                        registrert BOOLEAN,
                                        overtidlevert BOOLEAN,
                                        ukenr INTEGER
                                     );"""
        sql_create_Ratecard_table = """CREATE TABLE IF NOT EXISTS Ratecard (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ratecard STRING NOT NULL UNIQUE
                                    );"""
        sql_create_category_table = """CREATE TABLE IF NOT EXISTS category (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        category STRING NOT NULL UNIQUE
                                    );"""
        sql_create_overtidalternativer_table = """CREATE TABLE IF NOT EXISTS overtidalternativer (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        overtid_alt STRING
                                    );"""
        sql_create_fridager_table = """CREATE TABLE IF NOT EXISTS fridager (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                                        fridag TEXT NOT NULL UNIQUE,
                                        atimer INTEGER,
                                        beskrivelse TEXT
                                    );"""
        sql_create_kunder_table = """CREATE TABLE IF NOT EXISTS kunder (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL UNIQUE,
                                        timepris_chief INT,
                                        timepris_senior INT,
                                        timepris_consult INT,
                                        timepris_avtale INTEGER,
                                        timepris_reise INT,
                                        rabatt NUMERIC,
                                        km INT
                                    );"""
                            

        conn=self.create_connection(db_file)

        if conn is not None:
            self.create_tables(conn, sql_create_timedb_table)
            self.create_tables(conn, sql_create_Ratecard_table)
            self.create_tables(conn, sql_create_category_table)
            self.create_tables(conn, sql_create_overtidalternativer_table)
            self.create_tables(conn, sql_create_fridager_table)
            self.create_tables(conn, sql_create_kunder_table)
            conn.close()



    def create_connection(self,db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except conn.Error as e:
            print(e)
        #finally:
        #    if conn:
        #        conn.close()
        return conn

    def create_tables(self, conn, create_table_sql):
        try:
            c=conn.cursor()
            c.execute(create_table_sql)
            c.close()
        except c.Error as e:
            print(e)
        finally:
            if (c):
                c.close()

    def make_data_in_tabel(self, db_file, *arg, **kwargs):
        #ratecard_df= pd.read_excel('ratecard.xlsx')
        try:
            conn = sqlite3.connect(db_file)
            #print(arg)
            for tabel in arg:
                #print(tabel)
                if tabel=='Ratecard':
                    ratecard_df= pd.read_excel(self.directory / 'NewDBConfig/ratecard.xlsx')
                    ratecard_df.to_sql('Ratecard',conn, if_exists='append', index=False)
                elif tabel=='category':
                    category_df= pd.read_excel(self.directory / 'NewDBConfig/category.xlsx')
                    category_df.to_sql('category',conn, if_exists='append', index=False)
                    #print(category_df)
                elif tabel=='overtidalternativer':
                    overtidalt_df= pd.read_excel(self.directory / 'NewDBConfig/overtidalternativer.xlsx')
                    overtidalt_df.to_sql('overtidalternativer',conn, if_exists='append', index=False)
                    #print(overtidalt_df)                    
                elif tabel=='fridager':
                    overtidalt_df= pd.read_excel(self.directory / 'NewDBConfig/fridager.xlsx')
                    overtidalt_df.to_sql('fridager',conn, if_exists='append', index=False)    
                elif tabel=='kunder':
                    overtidalt_df= pd.read_excel(self.directory / 'NewDBConfig/kunder.xlsx')
                    overtidalt_df.to_sql('kunder',conn, if_exists='append', index=False)               
                else:
                    print(tabel)

        except conn.Error as e:
            print(e)
        finally:
            if (conn):
                conn.close()



