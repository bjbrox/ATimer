import sqlite3
import calendar
from datetime import date
from ResultatTimer import ResultatTimer

class Atimer_calendar(object):

    def __init__(self,dbfile):

        self.kunder_file = dbfile


    def getkrfakturert_u_overtid_mnd(self, mnd):
        #fakturert=0
        pris=0
        timer=0
        d=str(mnd)
        if len(d)==1:
            d='0'+d
        d='%-' + d +'-%'
        #print(d)
        try:
            sqliteConnection = sqlite3.connect(self.kunder_file)
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite to get MND pris") 

            sql_select_query = """SELECT timer, timepris, overtid FROM timedb WHERE dato LIKE ?;"""
            cursor.execute(sql_select_query, (d,))
            res=cursor.fetchall()
            #print(res)
            for t in res:
                if t[2]=='100%':
                    pris=t[0] * t[1] / 2 + pris
                    timer=timer+t[0]
                elif t[2]=='50%':
                    timepris= t[1] - t[1]*50/100
                    pris=t[0] * timepris + pris
                    timer=timer+t[0]
                else:
                    pris=t[0] * t[1] + pris
                
                
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed mnd ")
                #print(pris)
                return (pris, timer)

    def fri_dager_mnd(self, mnd):
        fd=0
        #dato=dato[:-4]
        #dato=dato[2:]  
        #dato='%' + dato +'%'
        mnd='%-' + mnd +'-%'
        result=[]
        try:
            sqliteConnection = sqlite3.connect("kunderdb.db")
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite fridag ",dato)

            sql_select_query = """SELECT atimer, fridag FROM fridager WHERE fridag LIKE ?"""
            cursor.execute(sql_select_query, (mnd, ))
            fd=cursor.fetchall()
            #print(fd)
            for x in fd:   #fd=fd[0]
                if x[0]==0:
                    result.append(x[1])
            p=0
            for r in result:
                result[p]=int(r[0:2])
                p=p+1

                    
            #print(fd)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")

                return result  # returnerer list av dato dager som er fri dag

    def antall_arbeidsdager_mnd(self, mnd, ar):
        #ar=dato[6:10]  # plukker ut årstall
        #mnd=dato[3:5]  # plukker ut måned
        #print('år ', ar , 'mnd ',mnd)
        weekday_count = 0
        cal = calendar.Calendar()
        fday=self.fri_dager_mnd(mnd)
        #fday=[1, 17, 21, 30, 31]
        ant_fday=len(fday)
        #print('antall fri dager', ant_fday)
        #print('fridager dato dag ',fday)
        #try:
        #    print(fday.index(1))
        #except ValueError:
        #    print('ikke fridag')
            
        for week in cal.monthdayscalendar(int(ar), int(mnd)):
            #print(week)
            for i, day in enumerate(week):
                #print(day)
                # not this month's day or a weekend
                if day == 0 or i >= 5:                # ikke tell om det er helg eller utenfor valgt mnd  
                    # helg dag dato
                    continue
                if ant_fday!=0:     # eksisterer det fridager i måneden ?
                    try:
                        for ant in fday:
                            if fday.index(day)<ant_fday:  # ikke tell om dato ligger i fridager databasen
                                ant #print(day)
                                continue 
                    except ValueError:
                        #print('.')
                        weekday_count += 1
                else:
                    weekday_count += 1
                # or some other control if desired...
                #print(day,i)
                
        #print('---------------------------------    ------------------------- ----------------')
        #print('Antall arbeidsdager ', weekday_count)
        return weekday_count

    def ant_atimer_mnd(self, mnd, ar):
        timer_count = 0
        dager_count = 0
        cal = calendar.Calendar()
        for week in cal.monthdayscalendar(ar, mnd):
            #print(week)
            for i, day in enumerate(week):
                #print(day)
                # not this month's day or a weekend
                if day == 0 or i >= 5:                # ikke tell om det er helg eller utenfor valgt mnd  
                    # helg dag dato
                    continue
                adag=ResultatTimer(self.kunder_file, date(ar,mnd,day))
                arbdag, atimer = adag.isworkday()
                if arbdag == True:     # eksisterer det fridager i måneden ?
                    timer_count=timer_count + atimer
                    #print(day)
                    if atimer == 4:
                        dager_count +=0.5
                    else:
                        dager_count +=1 
                else:
                    continue
                # or some other control if desired...
                #print(day,i)
                
        result= (timer_count, dager_count)     # returnerer antall timer og antall dager i en tuple
        return result

    '''
    def getkrfakturert_mnd(self, mnd):
        fakturert=0
        sumtimer=0
        pris=0
        d=str(mnd)
        if len(d)==1:
            d='0'+d
        d='%-' + d +'-%'
        #print(d)
        try:
            sqliteConnection = sqlite3.connect(self.kunder_file)
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
    '''