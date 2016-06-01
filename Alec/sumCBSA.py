'''
Created on May 31, 2016

@author: Alec
'''


import json

cpcFile = open("cpc_xf_with_CBSA_2.json")
data = json.load(cpcFile)

outFile = open("cpcWithCountyAndCBSA.json", "w+")

# cpcData = data["cpcData"]
cbsaList = []
cbsaSumList = []
cbsaNormList = []
listIndex = 0

#populate lists that will contain cbsa sum and normalized data
for county in data: #go line by line through every county
    currentCbsa = county["cbsaID"] 
    currentSum = county["sum"]
    currentNorm = county["normalized"]
    if currentCbsa != 0: #if it equals 0 then it isn't in a cbsa
        if currentCbsa not in cbsaList: #first county encountered in current cbsa
            cbsaList.append(currentCbsa) #add cbsa Id to list
            cbsaSumList.append(currentSum) # add cbsa Sum to list
            cbsaNormList.append(currentNorm) # add cbsa normalized sum to list
        else:
            listIndex = cbsaList.index(currentCbsa) #find index of cbsa ID in id list 
            oldSum = cbsaSumList[listIndex]
            newSum = int(county["sum"])
            cbsaSumList[listIndex] = oldSum+newSum
            oldNorm = cbsaNormList[listIndex]
            newNorm = county["normalized"]
            cbsaNormList[listIndex] = oldNorm + newNorm
            
# add cbsa sum and normalized sum fields to each line in json object
for county in data:
    if county["cbsaID"] != 0: #skip counties not in a cbsa
        listIndex = cbsaList.index(county["cbsaID"])
        county["cbsaSum"] = cbsaSumList[listIndex]
        county["cbsaNormalized"] = cbsaNormList[listIndex]
    
#print each county with new fields  
outFile.write("[\n")  
for county in data:
    outFile.write(json.dumps(county)+"\n,")
outFile.write("]")
    
    
