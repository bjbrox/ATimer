import datetime

class BJtimeclass(object):
    
    def getweeknr(self,dato):
        dt= datetime.datetime.strptime(dato, '%d-%m-%Y')
        weeknr= dt.isocalendar()[1]
        return weeknr
        
    def formatdato(self,d):
        d=d.strip('PyQt5.QtCore.QDate(')
        d=d.strip(')')
        d=d.replace(', ','-')
        self.contents=d
        #print(self.contents)
        dt = datetime.datetime.strptime(d, '%Y-%m-%d')
        dato=dt.strftime('%d-%m-%Y')
        self.contents=dato
        return self.contents

    def get_day(self,d):
        dt = datetime.datetime.strptime(d, '%d-%m-%Y')
        mnd=dt.strftime('%d')
        self.contents=mnd
        return self.contents

    def get_mnd(self,d):
        dt = datetime.datetime.strptime(d, '%d-%m-%Y')
        mnd=dt.strftime('%m')
        self.contents=mnd
        return self.contents

    def get_year(self,d):
        dt = datetime.datetime.strptime(d, '%d-%m-%Y')
        mnd=dt.strftime('%Y')
        self.contents=mnd
        return self.contents
