# -*- coding: utf-8 -*-
#from __future__ import print_function
import math
from collections import defaultdict
import collections
import string
import random
import itertools
import sys
import re
import addfips
import csv
from sys import argv
from collections import defaultdict
from collections import Counter

import difflib
from time import time

maxLine = -1
numPerfect = 0
numDifflib = 0
numNotfound = 0

debug = False
fipMap = {}
zipList = {}
fipList = {}
msaList = {}
pop10List = {}
csaList = {}
countyNameList = {}
stateNameMap = {}

cityStateToFip = defaultdict(list)
citiesInState = defaultdict(list)


def multi_dimensions(n, type):
  """ Creates an n-dimension dictionary where the n-th dimension is of type 'type'
  """  
  if n<=1:
    return type()
  return defaultdict(lambda:multi_dimensions(n-1, type))



def findFip(city,state):
   global numPerfect,numDifflib,numNotfound
   foundFip = "00000"
   state2 = state.lower().strip()
   if (len(state2)>2):
      if (len(stateLong2[state2]) > 0):
         if (debug): print " in findFip: ",state2,stateLong2[state2]
         state2 = stateLong2[state2][0]
      else:
         return foundFip
   if (debug): print "findFip state ",state,state2

   citiesList = citiesInState[state2.lower()]
   firstCity = ""
   secondCity = ""
#
# First look for a perfect match
   if (city in citiesList):
      firstCity = city
      numPerfect += 1
#
# Not a perfect match, so use difflib to find the best match
   else:
      citiesSort = sorted(citiesList,key=lambda x:difflib.SequenceMatcher(None,x,city).ratio(),reverse=True)
      if (len(citiesSort)> 0): firstCity = citiesSort[0]
      if (len(citiesSort)> 1): secondCity = citiesSort[1]
      numDifflib += 1
   if (debug): print "looking for ",city,"; found ",firstCity
#
# Now get the fips corresponding to a "good" city name
   fipsList = cityStateToFip[state2.lower()]
   if (len(fipsList) > 0):
   #if (debug): print "state:",state2,fipsList
      if (debug): print "search for city: ",city.lower()
      for fip in fipsList:
         #print fip["city"].lower()
         if firstCity.lower() in fip["city"].lower():
            foundFip = fip["fipC"]
            if (debug): print "FOUND"
            break
   if (foundFip == "000000"): numNotfound += 1
   return foundFip


def afterNum(mystring):
   mo = re.match('.+([0-9])[^0-9]*$', mystring)
   if (mo is not None):
      return mystring[mo.start(1)+1:],mo.start(1)+1
   else:
      return mystring, len(mystring)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def mysplit(s):
   head = s.rstrip('0123456789')
   tail = s[len(head):]
   return head, tail
#
# Get cpc info
cpcSectionHead = defaultdict(list)
cpcSectionClass = defaultdict(list)
fileName = "../cpc_short.tsv" 
f = open(fileName)
for line in f:
   lineParts = line.split("|")
   cpcVal = lineParts[0].strip()
   cpcDesc = lineParts[1].strip().lower().title()
   print "cpcVal: ",cpcVal,"; cpcDesc: ",cpcDesc
   if (len(cpcVal) == 1):
      cpcSectionHead[cpcVal].append(cpcDesc)
   elif (len(cpcVal) == 3):
      cpcSectionClass[cpcVal].append(cpcDesc)
cpcSectionClassLong = defaultdict(list)
fileName = "../cpc.tsv" 
f = open(fileName)
for line in f:
   lineParts = line.split("|")
   cpcVal = lineParts[0].strip()
   cpcDesc = lineParts[1].strip().lower().title()
   print "cpcVal: ",cpcVal,"; cpcDesc: ",cpcDesc
   if (len(cpcVal) == 3):
      cpcSectionClassLong[cpcVal].append(cpcDesc)


#
# Open the state csv file
fc = open("state.csv", 'rb')
# topics loaded in 3-tuples: (topicN, dopicDesc, topicSel)
reader = csv.DictReader(fc, delimiter=',', quotechar="'")
stateNameList = []
state2List = []
stateLong2 = defaultdict(list)
for row in reader:
   stateNameList.append(row["name_long"])
   state2List.append(row["name_short"])
   stateLong2[row["name_long"].lower()].append(row["name_short"].lower())
   print row
print "Number of state: ",len(stateNameList)
print stateNameList


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
   fipC = row["county"].replace('"','')
   csa = row["csa"].replace('"','').strip()
   msa = row["cbsa"].replace('"','').strip()
   stateName = row["stab"]
   countyName = row["zipname"]
   placenm14 = row["placenm14"]
   weight = (row["afact"])
   pop10 = int(row["pop10"])
   city = placenm14.split(",")[0]
   city = city.replace(" city","").lower()
   city = city.replace("boise city","boise").lower()
   city = city.replace(" cdp","").lower()
   city = city.replace(" village","").lower()
   city = city.replace(" borough","").lower()
   #print "adding ",stateName.lower()
   if (len(city)>2):
      if (city.lower() not in citiesInState[stateName.lower()]):
         citiesInState[stateName.lower()].append(city.lower())
         cityStateToFip[stateName.lower()].append({"fipC":fipC,"city":city})
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

print "citiesInState"
#for key,val in citiesInState.iteritems():
#   print "   key: ",key,val

#
# Now get the data from patstat online - in csv files

fileNamePatents = "resulttable_2013-2016.csv" 
fileNamePatents = "resulttable_2011-2012.csv" 
fileNamePatents = "resulttable_2009-2010.csv" 
fileNamePatents = "resulttable_2007-2008.csv" 
fileNamePatents = "resulttable_2005-2006.csv" 
fileNamePatents = "resulttable_all.csv" 
f = open(fileNamePatents)
next(f)
numRead = 0
patentData = defaultdict(list)
patentDataCount = defaultdict(int)
addrCount = defaultdict(int)
for line in f:
   lineParts = line.split(";")
   year = int(lineParts[0])
   docdbId = int(lineParts[1])
   numFamily = int(lineParts[2])
   addr = lineParts[3].strip()[1:-1]
   cpc4 = lineParts[4].strip()[1:-1]
   year_cpc_addr = str(year) + "|" + cpc4[:3] + "|" + addr
   patentDataCount[year_cpc_addr] += 1
   addrCount[addr] += 1
   if (numRead < 100): print "line: ",year,docdbId,numFamily,addr,cpc4,"; year_cpc_addr: ",year_cpc_addr
   numRead += 1
   if (maxLine>0) and (numRead>maxLine): break
f.close()
print "Number of lines read    :",numRead
print "Number of year/cpc/addr :",len(patentDataCount)
print "Number of addr only     :",len(addrCount)

#
# Loop over unique addresses and find city/state and lookup FIPS
numBad1 = 0
numBad1city = 0
numBad3 = 0
cityStateFIPS = defaultdict(list)
numProcessed = 0
print "Number addr to process: ",len(addrCount)
t0 = time()
addrFips = defaultdict(list)
for addr in addrCount:
#
   if (numProcessed%1000 == 0): 
      print "Processed: %d; perf %d, difflib %d; nofound %d; in %0.3fs." % (numProcessed,numPerfect,numDifflib,numNotfound,(time() - t0))
      t0 = time()
   numProcessed += 1
#
# Now split addr into parts
   addrParts = addr.split(",")
   city = ""
   state = ""
   fips = ""
   print addr
   if (len(addrParts) == 2):
      city = addrParts[0]
      state = addrParts[1]
      if (len(state.split()) == 2):
         oldCity = city
         oldState = state
         stateParts = state.split()
         cityParts = city.split()
         lastStateParts = stateParts[-1]
         if (is_int(lastStateParts[-1])):
            state = stateParts[0]
            lastCity = cityParts[-1].lower()
            firstCity = ""
            if (len(cityParts) > 1):
               firstCity = cityParts[-2].lower()
            if ("hills" in lastCity or "park" in lastCity or "york" in lastCity \
                  or "claire" in lastCity or "city" in lastCity or "alto" in lastCity  or "rouge" in lastCity \
                   or "santa" in firstCity  or "san" in firstCity or "los" in firstCity):
               city = cityParts[-2] + " " + cityParts[-1]
            else:
               city = cityParts[-1]
         else:
            state = stateParts[1]
            city = stateParts[0]
         if (debug): print "   2p: ",len(oldCity.split()),len(oldState.split()),"oc: ",oldCity,"; os: ",oldState,"; nc ",city,"; ns ",state
      elif (len(state.split()) > 2):
         stateParts = state.split()
         offset = 0
         if is_int((stateParts[-1])[0]): offset = -1
         state = stateParts[-1+offset]
         city = stateParts[-2+offset]
         if (debug): print "stateparts :",stateParts,"; city ",city,"; state ",state,"; offset ",offset
         if (len(stateParts) > (2-offset)):
            if (debug): print "got here"
            if ("st" in stateParts[-3+offset].lower() or "saint" in stateParts[-3+offset].lower() \
                  or "winter" in stateParts[-3+offset].lower() or "new" in stateParts[-3+offset].lower()):
               city = stateParts[-3+offset] + " " + stateParts[-2+offset]
#         if (
      if (debug): print "   2: ",city,",",state
   elif (len(addrParts) > 2):
#
# Is the last part a number?
      if (debug): print "  len(addrParts) > 2: ",addrParts

      lastP = addrParts[-1]
      if (debug): print "  lastP: ",lastP
      
      if (len(lastP)>0 and is_int(lastP[-1])):
#
# Does the last part have two parts?
         if (debug): print "   zip is last: ",lastP,len(lastP.split())
         if (len(lastP.split()) > 2):
            state = lastP.split()[-2]
            city = " ".join(lastP.split()[:-2])
         elif (len(lastP.split()) == 2):
            state = lastP.split()[0]
            city = addrParts[-2]
         elif (len(lastP.split()) == 1): 
            state = addrParts[-2]
            city = addrParts[-3]
         else:
            state = "errs"
            city = "errc"
      else:
         state = addrParts[-1]
         city = addrParts[-2]
      (cityN,pos) = afterNum(city)
      if (debug): print "   3: ",cityN,",",state
   elif (len(addrParts) == 1):
      if (len(addrParts[0]) > 2): 
         numBad1city += 1
         (cityN,pos) = afterNum(addrParts[0])
         newParts = (addrParts[0])[:pos].split()
         city = ""
         state = ""
         zipCode = newParts[-1]
         offset = 0
         if is_int(zipCode[0]):
            offset = -1
         print "len(newParts),offset ",len(newParts),offset,newParts
         if (len(zipCode) >= 5):
            if (len(newParts) > 2) and \
                     ("south" in newParts[-2+offset].lower() or \
                     "new" in newParts[-2+offset].lower() or \
                     "north" in newParts[-2+offset].lower()) \
                     and (len(newParts) > 2):
               city = newParts[-3+offset]
               state = newParts[-2+offset] + " " + newParts[-1+offset]
            elif (len(newParts) > 1):
               city = newParts[-2+offset]
               state = newParts[-1+offset]
         if (debug): print "  1a: ",addrParts[0],"; res ",city,state
      else:
         p2Parts = addrParts[0].split()
         len2 = len(p2Parts)
         if (debug): print "  1b: ",addrParts[0]
         
         if (debug): print "addr1 2: ",len2,":P ",addrParts[0]
#
# Spelling mistakes:
   if (state == "Alambama"): state = "Alabama"
#
# Now do the fips lookup
   fips = "00000"
   if (city is not "" and state is not ""):
      fips = findFip(city.lower(),state.lower())
   print "Found fips ",fips,"; ,city,state: ",city,state
   addrFips[addr].append(fips)

print "Number of addr   only     :",len(addrCount)
print "Number of addr1  only     :",numBad1
print "Number of addr1  city     :",numBad1city
print "Number of addr>3 only     :",numBad3
    
#
# Now loop over patents file again, and associate fips
patentsByCpcYearFips = multi_dimensions(4, int)

f = open(fileNamePatents)
next(f)
numRead = 0
for line in f:
   lineParts = line.split(";")
   year = int(lineParts[0])
   docdbId = int(lineParts[1])
   numFamily = int(lineParts[2])
   addr = lineParts[3].strip()[1:-1]
   cpc4 = lineParts[4].strip()[1:-1]
   print "cpc4: ",cpc4
   if (len(cpc4) < 1):
      print "No cpc found!: ",year,docdbId,numFamily,addr,cpc4
   else:
      cpc1 = cpc4[0]
      print "cpc1: ",cpc1
      if (cpc1=="A" or cpc1=="B" or cpc1=="C" or cpc1=="D" or cpc1=="E" or cpc1=="F" or cpc1=="G" or cpc1=="H" or cpc1=="Y"):
         cpc3 = cpc4[:-1]
         year_cpc_addr = str(year) + "|" + cpc4[:3] + "|" + addr
         #if (numRead < 100): 
         print "line: ",year,docdbId,numFamily,addr,cpc4,"; year_cpc_addr: ",year_cpc_addr
         numRead += 1
         if (maxLine>0) and (numRead>maxLine): break
#
# Retriiev the fips
         fips = addrFips[addr]
#
# Now add data and count
         print "cpc3,year,fips: ",cpc3,";",year,fips[0]
         cpc1 = cpc4[0]
         patentsByCpcYearFips[cpc1][year][fips[0]] += 1
   
#
# Now loop over summary patent data
firstCpc = True
sumName = "cpc_summary.json"
sumf = open(sumName,'w')
sumf.write('{\n')
for cpc in patentsByCpcYearFips.keys():
   if (not firstCpc): sumf.write(',\n')
   firstCpc = False
   sumf.write('"cpc_' + cpc + '":\n')
   sumf.write('{\n')
   sumf.write('   "name":cpc_"' + cpc + '",\n')
   sumf.write('   "url":"' + cpc + '",\n')
   sumf.write('   "html":"' + cpc + '",\n')
   sumf.write('   "sumDates":{\n' )
   outName = "cpc_" + cpc + "_year_fips.csv"
   outf = open(outName,'w')
   outf.write("{\n")
   line = ""
   first = True
   total = 0
   print "processing cpc:",cpc
   firstYear = True
   for year in patentsByCpcYearFips[cpc].keys():
      print "   processing year:",year
      sumYear = 0
      for fips in patentsByCpcYearFips[cpc][year].keys():
         print "      fips,count:",fips,patentsByCpcYearFips[cpc][year][fips]
         count = patentsByCpcYearFips[cpc][year][fips]
         if (not first): line = ","
         line += '"'+fips+'":{"sum":'+str(count)+', "normalized":'+str(count)+', "year":'+str(year)+'}\n'
         outf.write(line)
         first = False
         sumYear += patentsByCpcYearFips[cpc][year][fips]
      if (not firstYear): sumf.write(',')
      sumf.write('   "' + str(year) + '":' + str(sumYear))
      firstYear = False  
      total += sumYear
   sumf.write('},\n')       
   sumf.write('   "gender":' + str(total) + ',\n')
   sumf.write('   "age":' + str(total) + ',\n')
   sumf.write('   "delta":' + str(total) + ',\n')
   sumf.write('   "party":' + str(total) + ',\n')
   sumf.write('   "total":' + str(total) + '\n}\n')
   outf.write("}\n")
   outf.close()
sumf.write('}\n') 
sumf.close()


#
# Now make a XF json file
#
# Now loop over xummary patent data
firstCpc = True
xumName = "cpc_xf.json"
xumf = open(xumName,'w')
xumf.write('{\n')
xumf.write('"cpcData":[\n')

csvName = "cpc_xf.csv"
csvf = open(csvName,'w')
csvf.write('fips,cpc,sum,normailized\n')

first = True
for cpc in patentsByCpcYearFips.keys():
   print "processing cpc:",cpc
   firstYear = True
   for year in patentsByCpcYearFips[cpc].keys():
      print "   processing year:",year
      xumYear = 0
      for fips in patentsByCpcYearFips[cpc][year].keys():
         print "      fips,count:",fips,patentsByCpcYearFips[cpc][year][fips]
         count = patentsByCpcYearFips[cpc][year][fips]
         line = ""
         if (not first): line = ","
         line += '{"cpc":"'+cpc+'", "fips":"'+fips+'", "sum":'+str(count)+', "normalized":'+str(count)+', "year":'+str(year)+'}\n'
         xumf.write(line)
         cline = fips+','+cpc+','+str(count)+','+str(count)+'\n'
         csvf.write(cline)
         first = False
xumf.write(']\n') 
xumf.write('}\n') 
xumf.close()

csvf.close()

