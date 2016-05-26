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

#
# grab a "cursor"
cur_fetch = con.cursor(mdb.cursors.DictCursor)


sel = u'''select fips, count from ohio_counties'''





print sel


cur_fetch.execute(sel)

print "Rows returned: ",cur_fetch.rowcount
numWrites = 0
i = 0

rows = cur_fetch.fetchall()

if i < 10:

    for row in rows:
       fips = row['fips']
       count = row['count']

       print fips, count

       f = open('myfile.txt','a')
       f.write(',{"cpc":"A", "fips":"')
       f.write(fips)
       f.write('", "sum":')
       f.write(count)
       f.write(', "normalized":')
       f.write(count)
       f.write(', "year":2015}')

       f.write("\n")

       i = i + 1

       f.close()
