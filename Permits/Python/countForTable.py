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


sel = u'''select fips, count, name from california_counties'''





print sel


cur_fetch.execute(sel)

print "Rows returned: ",cur_fetch.rowcount
numWrites = 0
i = 0

rows = cur_fetch.fetchall()



for row in rows:
   fips = row['fips']
   count = row['count']
   name = row['name']

   print fips, count

   f = open('new_california.txt','a')
   f.write(',{"Type":"Title V", "County":"')
   f.write(name)
   f.write('", "Sum":')
   f.write(count)
   f.write(', "Fips ID":')
   f.write(fips)
   f.write(', "Year":2015}')

   f.write("\n")

   i = i + 1

   f.close()
