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


sel = u'''select letters, state, permits from state_totals'''





print sel


cur_fetch.execute(sel)

print "Rows returned: ",cur_fetch.rowcount
numWrites = 0
i = 0

rows = cur_fetch.fetchall()



for row in rows:
   letters = row['letters']
   state = row['state']
   permits = row['permits']

   print letters, state, permits

   f = open('stateTotals.txt','a')
   f.write(',{"State ID":"')
   f.write(letters)
   f.write('", "State":"')
   f.write(state)
   f.write('", "Permits":')
   f.write(permits)
   f.write('}')

   f.write("\n")

   i = i + 1

   f.close()
