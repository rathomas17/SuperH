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

sel = u'''select FacilityName,County from Ohio'''
print sel
cur_fetch.execute(sel)
print "Rows returned: ",cur_fetch.rowcount
numWrites = 0
#for i in range(cur_fetch.rowcount):
#   row = cur_fetch.fetchone()
rows = cur_fetch.fetchall()
for row in rows:
   FacilityName = row['FacilityName']
   County = row['County']
   print 'Row data: FacilityName ',FacilityName,'; County ',County
