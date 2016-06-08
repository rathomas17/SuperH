# -*- coding: utf-8 -*-
#from __future__ import print_function

from time import time
import MySQLdb as mdb
import csv
from sys import argv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#
# Connect to DB
con = mdb.connect(read_default_file=u'./genUser.cnf', db=u'State_Permits', charset=u'utf8')
con2 = mdb.connect(read_default_file=u'./genUser.cnf', db=u'State_Permits', charset=u'utf8')
#
# grab a "cursor"
cur_fetch = con.cursor(mdb.cursors.DictCursor)
cur_fetch2 = con2.cursor(mdb.cursors.DictCursor)

sel = u'''select FacilityName,County from Ohio'''
sel2 = u'''select name,fips from Counties'''

f = open('myfile.txt','w')


print sel


cur_fetch.execute(sel)
cur_fetch2.execute(sel2)
print "Rows returned: ",cur_fetch.rowcount
numWrites = 0
i = 0

rows = cur_fetch.fetchall()
fipsrows = cur_fetch2.fetchall()


for row in rows:
   FacilityName = row['FacilityName']
   County = row['County']

   #print 'Row data: FacilityName ',FacilityName,'; County ',County


   i = i + 1
   for row2 in fipsrows:

       fips = row2['fips']
       name = row2['name']




       if i < 10 and County == name:
            print fips, i

            #{"cpc":"A", "fips":"39001", "sum":100, "normalized":100, "year":2015}

            f = open('myfile.txt','a')
            f.write('"lol"')
            f.write("\n")
            f.close()
