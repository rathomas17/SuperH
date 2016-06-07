# -*- coding: utf-8 -*-
#from __future__ import print_function

from time import time
import MySQLdb as mdb
import csv
from sys import argv
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')

script,indexS = argv
index = int(indexS)
fipMap = {}
zipList = {}
fipList = {}
msaList = {}
pop10List = {}
csaList = {}
countyNameList = {}
stateNameMap = {}


def ensure_unicode(s):
   if isinstance(s, str):
      return unicode(s, u'utf-8')
   if isinstance(s, unicode):
      return s
   if isinstance(s, list):
      newList = []
      for element in s:
         newList.append(ensure_unicode(element))
      return newList
   if isinstance(s, tuple):
      newList = []
      for element in s:
         newList.append(ensure_unicode(element))
      return tuple(newList)
   if isinstance(s, dict):
      newDict = {}
      for key, value in s.iteritems():
         newDict[ensure_unicode(key)] = ensure_unicode(value)
      return newDict
   #this might be a bad idea; doing this might hide bugs
   if s == None:
      return u''

def ensure_str(s):
   if isinstance(s, str):
      return s
   if isinstance(s, unicode):
      return s.encode(u'utf-8')
   if isinstance(s, list):
      newList = []
      for element in s:
         newList.append(ensure_str(element))
      return newList
   if isinstance(s, tuple):
      newList = []
      for element in s:
         newList.append(ensure_str(element))
      return tuple(newList)
   #this might be a bad idea; doing this might hide bugs
   if s == None:
      return ''



def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        print "not an int: ",s
        return False

def findFip(zipCode):
   izip = zipCode
   if (izip in fipMap):
      return fipMap[izip],msaList[izip],csaList[izip],countyNameList[izip],stateNameMap[izip],pop10List[izip]
   else:
      closestFip = fipMap.get(izip, fipMap[min(fipMap.keys(), key=lambda k: abs(int(k)-int(izip)))])
      closestZip = 0
      for thiszip, thisfip in fipMap.iteritems():
         if thisfip == closestFip:
            closestZip = thiszip
            break
      print "zipCode not in DB: ",izip,closestZip
      print "fipmap ",fipMap[closestZip]
      return closestFip,msaList[closestZip],csaList[closestZip],countyNameList[closestZip],stateNameMap[closestZip],pop10List[closestZip]

# Add the documents
#args = get_stdin_args()
#print args

#project_name = args[0]

#print 'project_name = ', project_name

#
# Open the state csv file
fc = open("state.csv", 'rb')
# topics loaded in 3-tuples: (topicN, dopicDesc, topicSel)
reader = csv.DictReader(fc, delimiter=',', quotechar="'")
stateNameList = []
state2List = []
for row in reader:
   stateNameList.append(row["name_long"])
   state2List.append(row["name_short"])
   print row
print "Number of state: ",len(stateNameList)
print stateNameList

state = stateNameList[index]
state2 = state2List[index]
print "Processing index ",index,state
statec = ", " + state
state2c = ", " + state2
filename = state + "_cpcdata.csv"
#target = open(filename, 'w')
target = codecs.open(filename, 'w',encoding='utf-8')
#
# Open the zip to fip file
#fc = open("zipFip2014.csv", 'rb')
fc = open("geocorr14new.csv", 'rb')
# topics loaded in 3-tuples: (topicN, dopicDesc, topicSel)
reader = csv.DictReader(fc, delimiter=',', quotechar='"')
lastZip = 0
maxFip = 0
maxMsa = 0
maxCsa = 0
maxCounty = 0
maxState = 0
maxPop10 = 0
maxWeight = 0
numZips = 0
for row in reader:
   #print row["zcta5"],row["county"],row["afact"]
   zipC = row["zcta5"].replace('"','').strip()
   fipC = row["county"].replace('"','').strip()
   csa = row["csa"].replace('"','').strip()
   msa = row["cbsa"].replace('"','').strip()
   stateName = row["stab"]
   countyName = row["zipname"]
   weight = (row["afact"])
   pop10 = int(row["pop10"])
   if (zipC == lastZip):
      if (weight > maxWeight):
         maxFip = fipC
         maxCsa = csa
         maxMsa = msa
         maxPop10 = pop10
         maxState = stateName
         maxCounty = countyName
         maxWeight = weight
   else:
      if (numZips > 0):
         #print lastZip, maxFip
         zipList[lastZip] = lastZip
         fipList[lastZip] = maxFip
         pop10List[lastZip] = maxPop10
         msaList[lastZip] = maxMsa
         csaList[lastZip] = maxCsa
         countyNameList[lastZip] = maxCounty
         stateNameMap[lastZip] = maxState
         fipMap[lastZip] = maxFip
      maxFip = fipC
      maxWeight = weight
      maxCsa = csa
      maxMsa = msa
      maxPop10 = pop10
      maxState = stateName
      maxCounty = countyName
      lastZip = zipC

   numZips += 1
   #print row
#print lastZip, maxFip
zipList[lastZip] = lastZip
fipList[lastZip] = maxFip
pop10List[lastZip] = maxPop10
msaList[lastZip] = maxMsa
csaList[lastZip] = maxCsa
countyNameList[lastZip] = maxCounty
stateNameMap[lastZip] = maxState
fipMap[lastZip] = maxFip
print "Number of zip/fip: ",len(zipList)
print numZips


con = mdb.connect(read_default_file=u'/nfs/15/com0596/mysql_configs/superH_genUser.cnf', db=u'superH', charset=u'utf8')
cur_fetch = con.cursor(mdb.cursors.DictCursor)

sel = u'''select docdb_family_id,cpc,appln_addresses,appln_countries,appln_auth,''' + \
          u'''substring_index(appln_filing_year,"|",1) as year ''' + \
          u''' from patstatSummary_au15 ''' + \
               u''' where appln_auth like "%US%" and appln_countries like "%US%" ''' + \
               u''' and (substring_index(appln_filing_year,"|",1)>1989) ''' + \
               u''' and (appln_addresses like "%''' + state + u'''%"''' + \
               u''' or appln_addresses like "% ''' + state2 + u''' %"''' + \
               u''' or appln_addresses like "% ''' + state2 + u'''|%"''' + \
               u''' or appln_addresses like "%,''' + state2 + u''' %"''' + \
               u''' )'''
#sel = u'''select cpc,appln_addresses,appln_countries,appln_auth,numPatents,appln_filing_year from patstatSummaryReprocess_au15
#               where appln_auth like "%US%" and substring_index(appln_filing_year,"|",1) >1989
#               and (appln_addresses like "%''' + statec + \
#               u''' %" or appln_addresses like "%''' + state2c +  u''' %") limit 200'''
print sel
cur_fetch.execute(sel)
print "Rows returned: ",cur_fetch.rowcount
numWrites = 0
for i in range(cur_fetch.rowcount):
   row = cur_fetch.fetchone()
   cpcs = row['cpc'].split("|")
   addrs = row['appln_addresses'].split("|")
   countries = row['appln_countries'].split("|")
   auths = row['appln_auth'].split(",")
   numPatents = len(auths)
   year = row['year']
   docdb_family_id = row['docdb_family_id']
#
# Get first year
#   year = years[0]
#
# Count US patents
   numPatentsUS = 0
   for auth in auths:
      if (auth.strip() == "US"): numPatentsUS += 1
#
# Find unique cpc codes for this patent
   cpcSectionList = []
   for cpc in cpcs:
      cpcSection = cpc.split(" ",1)[0]
#
# Ceck that cpc is not too long
      if (len(cpcSection)>4):
         cpcSectionLower = cpcSection.lower()
         pos = 1
         foundPos = 1
         foundEnd = False
         for c in cpcSectionLower:
            if (not foundEnd) and (pos > 1) and (c in 'abcdefghijklmnopqrstuvwxyz'):
               foundPos = pos
               foundEnd = True
            pos += 1
         if (foundEnd): cpcSection = cpcSection[0:foundPos]
         #print "long",foundPos,cpcSection
#
      if (cpcSection not in cpcSectionList) and (cpcSection != 'NULL') and (len(cpcSection)>1):
         cpcSectionList.append(cpcSection)
#
# Now add all of the sections and other info
   for cpcSection in cpcSectionList:
#
# For each CPC, find all of the addresses that are like the state we want
      cityList = []
      foundState = False
      for n in range(len(addrs)):
         country = countries[n]
         addr = addrs[n]
         if (country == "US"):
#
# Use this form to write out all addresses for this state
#            if (statec in addr) or (state2c in addr):
#
# Use this form to write out first address of this state
            if (not foundState) and ((statec in addr) or (state2c in addr)):
               zipCode = addr.split(" ")[-1]
               zipCode = zipCode[0:5]
               city = addr.split(",")[-2]
               if ("San Jos" in city):
                  print "san jose found"
                  city = "San Jose"
                  print city
               if (city not in cityList):
                  cityList.append(city)
                  if (RepresentsInt(zipCode)):
                     fip,msa,csa,county,stateName,pop10 = findFip(zipCode)
                  else:
                     fip = 0
                     msa = 0
                     csa = 0
                     county = "none"
                     stateName = "none"
                     pop10 = 0
#
# Only write out good results
                  if (fip > 0):
                     foundState = True
                     #print cpcSection,"|",docdb_family_id,"|",year,"|",\
                     #   numPatents,"|",numPatentsUS,"|",city,"|",\
                     #   zipCode,"|",fip,"|",state2
                     line = cpcSection + " | " + str(docdb_family_id) + " | " + str(year) + " | " + \
                        str(numPatents) + " | " + str(numPatentsUS) + " | " + city + " | " + \
                        zipCode + " | " + str(fip) + " | " + state2 + \
                        " | " + msa + " | " + csa + " | " + county + " | " + stateName + " | " + str(pop10) + \
                        "\n"
                     #line = ensure_unicode(line)
                     #print line
                     if (state2 == stateName):
                        target.write(line)
                        numWrites += 1
                     else:
                        print "STATE MISMATCH: ",line
print "Total number written records: ",numWrites
target.close()
