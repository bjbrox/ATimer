import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import yaml
from Atimer_calendar import Atimer_calendar

class ResultatPlot(object):
    def __init__(self, dbfile, mybud, year):

        #self.kunder_file = "kunderdb.db"
        #with open('config.yml') as f:
        #    data = yaml.load(f, Loader=yaml.FullLoader)
        #self.kunder_file = data['db_name']
        #self.df=pd.read_sql_query("SELECT dato, timer, timepris FROM timedb WHERE dato LIKE ?;", con)
        self.kunder_file = dbfile
        self.mybud = mybud
        self.year = year

    '''def getdata2plot_year(self, ar):
        year=str(ar)
        year='%' + year 
        df=0
        try:
            sqliteConnection = sqlite3.connect(self.kunder_file)
            print("Connected to SQLite")
            df = pd.read_sql_query("SELECT dato, timer, timepris FROM timedb WHERE dato LIKE '%-04-%'", sqliteConnection)
            #cursor = sqliteConnection.cursor()
            
            #sql_select_query = """SELECT dato, timer, timepris FROM timedb WHERE dato LIKE ?;"""
            #cursor.execute(sql_select_query, (year,))
            #res=cursor.fetchall()
            #print(df)
            #for t in res:
            #    pris=t[1]*t[2]+pris
                
            #cursor.close()
            sqliteConnection.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed ")
                #print(pris)
                return (df)            
    '''

    def getdata2plot_mnd(self, mnd):
        month=str(mnd)
        if len(month)==1:
            month='0'+month
        month='%-' + month +'-%'
       
        #print('parameter = ',month)
        
        df=0
        try:
            sqliteConnection = sqlite3.connect(self.kunder_file)
            #print("Connected to SQLite")
            df = pd.read_sql_query("SELECT dato, timer, timepris FROM timedb WHERE dato LIKE :valg", sqliteConnection,params={'valg': month})
            #cursor = sqliteConnection.cursor()
            
            #sql_select_query = """SELECT dato, timer, timepris FROM timedb WHERE dato LIKE ?;"""
            #cursor.execute(sql_select_query, (year,))
            #res=cursor.fetchall()
            #print(res)
            #for t in res:
            #    pris=t[1]*t[2]+pris
                
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

    def showPlot(self, p):

        plot=ResultatPlot(self.kunder_file, self.mybud, self.year)
        ant=Atimer_calendar(self.kunder_file)
        sum_dager=0
        sum_timer=0
        mal_bud= self.mybud #1800000
        mnd_bud=[]
        print(type(self.year))
        print(self.year)

        for alle_mnd in range(12):
            m=alle_mnd+1
            timer, dager =ant.ant_atimer_mnd(m,int(self.year))
            sum_dager=sum_dager+dager
            sum_timer=sum_timer+timer

        #print(sum_dager)

        for alle_mnd in range(12):
            m=alle_mnd+1
            timer, dager =ant.ant_atimer_mnd(m,int(self.year))
            prosent = dager / sum_dager * 100
            bud=mal_bud * prosent / 100
            mnd_bud.append(round(bud, 2))
            #print('timer ', str(timer), 'dager ', str(dager), 'bud ', str(bud))     
            


        for t in range(12):
            m=t+1
            maned=plot.getdata2plot_mnd(m)
            if m==1:
                jan=maned
                sumjan=jan['timer'] * jan['timepris']
                #print(type(sumjan))
                jan['sum_kr'] = sumjan
                
            elif m==2:
                feb=maned
                sumfeb=feb['timer'] * feb['timepris']
                feb['sum_kr'] = sumfeb
                
            elif m==3:
                mar=maned
                summar=mar['timer'] * mar['timepris']
                mar['sum_kr'] = summar
                
            elif m==4:
                apr=maned
                sumapr=apr['timer'] * apr['timepris']
                apr['sum_kr'] = sumapr
                
            elif m==5:
                mai=maned
                summai=mai['timer'] * mai['timepris']
                mai['sum_kr'] = summai
                
            elif m==6:
                jun=maned
                sumjun=jun['timer'] * jun['timepris']
                jun['sum_kr'] = sumjun
                
            elif m==7:
                jul=maned
                sumjul=jul['timer'] * jul['timepris']
                jul['sum_kr'] = sumjul
                
            elif m==8:
                aug=maned
                sumaug=aug['timer'] * aug['timepris']
                aug['sum_kr'] = sumaug
                
            elif m==9:
                sep=maned
                sumsep=sep['timer'] * sep['timepris']
                sep['sum_kr'] = sumsep
                
            elif m==10:
                okt=maned
                sumokt=okt['timer'] * okt['timepris']
                okt['sum_kr'] = sumokt
                
            elif m==11:
                nov=maned
                sumnov=nov['timer'] * nov['timepris']
                nov['sum_kr'] = sumnov
                
            elif m==12:
                des=maned
                sumdes=des['timer'] * des['timepris']
                des['sum_kr'] = sumdes
                

        data = {'mnd':['jan','feb','mar','apr','mai','jun','jul','aug','sep','okt','nov','des'], 
                        'sum_kr':[  jan['sum_kr'].sum(), 
                                    feb['sum_kr'].sum(),
                                    mar['sum_kr'].sum(),
                                    apr['sum_kr'].sum(),
                                    mai['sum_kr'].sum(),
                                    jun['sum_kr'].sum(),
                                    jul['sum_kr'].sum(),
                                    aug['sum_kr'].sum(),
                                    sep['sum_kr'].sum(),
                                    okt['sum_kr'].sum(),
                                    nov['sum_kr'].sum(),
                                    des['sum_kr'].sum() ],
                        'bud_kr':[mnd_bud[0], mnd_bud[1], mnd_bud[2], mnd_bud[3], mnd_bud[4], mnd_bud[5], 
                                mnd_bud[6], mnd_bud[7], mnd_bud[8], mnd_bud[9], mnd_bud[10], mnd_bud[11]]   
                }

        jan_mnd=jan['sum_kr'].sum()
        feb_mnd=jan_mnd+feb['sum_kr'].sum()
        mar_mnd=feb_mnd+mar['sum_kr'].sum()
        apr_mnd=mar_mnd+apr['sum_kr'].sum()
        mai_mnd=apr_mnd+mai['sum_kr'].sum()
        jun_mnd=mai_mnd+jun['sum_kr'].sum()
        jul_mnd=jun_mnd+jul['sum_kr'].sum()
        aug_mnd=jul_mnd+aug['sum_kr'].sum()
        sep_mnd=aug_mnd+sep['sum_kr'].sum()
        okt_mnd=sep_mnd+okt['sum_kr'].sum()
        nov_mnd=okt_mnd+nov['sum_kr'].sum()
        des_mnd=nov_mnd+des['sum_kr'].sum()

        jan_bud=mnd_bud[0]
        feb_bud=jan_bud+mnd_bud[1]
        mar_bud=feb_bud+mnd_bud[2]
        apr_bud=mar_bud+mnd_bud[3]
        mai_bud=apr_bud+mnd_bud[4]
        jun_bud=mai_bud+mnd_bud[5]
        jul_bud=jun_bud+mnd_bud[6]
        aug_bud=jul_bud+mnd_bud[7]
        sep_bud=aug_bud+mnd_bud[8]
        okt_bud=sep_bud+mnd_bud[9]
        nov_bud=okt_bud+mnd_bud[10]
        des_bud=nov_bud+mnd_bud[11]

        data_akk = {'mnd':['jan','feb','mar','apr','mai','jun','jul','aug','sep','okt','nov','des'], 
                        'sum_kr':[  jan_mnd, 
                                    feb_mnd,
                                    mar_mnd,
                                    apr_mnd,
                                    mai_mnd,
                                    jun_mnd,
                                    jul_mnd,
                                    aug_mnd,
                                    sep_mnd,
                                    okt_mnd,
                                    nov_mnd,
                                    des_mnd ],
                        'bud_kr':[  jan_bud, 
                                    feb_bud,
                                    mar_bud,
                                    apr_bud,
                                    mai_bud,
                                    jun_bud,
                                    jul_bud,
                                    aug_bud,
                                    sep_bud,
                                    okt_bud,
                                    nov_bud,
                                    des_bud ]            
                    }


        df= pd.DataFrame(data)
        dfakk= pd.DataFrame(data_akk)
        #print(df)
        #print('')
        #print(dfakk)
        if p=="Akkumulert Bud":
            ax= dfakk.plot.bar(x='mnd', y=['bud_kr','sum_kr'], rot=0)
            ax
        else:
            ax= df.plot.bar(x='mnd', y=['bud_kr','sum_kr'], rot=0)
        plt.show()

'''
if __name__ == "__main__":
    import sys
    myplot=ResultatPlot()
    myplot.showPlot('')
    sys.exit(app.exec_())
'''
