#encoding:utf-8

import datetime, time
def str2datetime(timestr):
    #~ return datetime.datetime(*time.strptime("16/6/1981", "%d/%m/%Y")[0:5])
    return datetime.datetime(*time.strptime(timestr, "%Y-%m-%d")[0:5])