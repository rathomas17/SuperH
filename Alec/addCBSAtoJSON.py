import json

#Remember to delete the extra brackets and names at the beginning of the cpc_xf.json file

cpcFile = open("cpc_xf.json")
convertFile = open("crosswalk.json")
cpcData = json.load(cpcFile)
convertData = json.load(convertFile)
outFile = open("cpc_xf_with_CBSA_2.json", "w")


cpcFile.close()

outFile.write("[\n")


for line in cpcData:
    cbsaID = 0
    cbsaName = "null"
    fips = line["fips"]
    #print(fips)
    for county in convertData:
        if county["fipscounty"]-int(fips)==0:
            cbsaID = county["cbsa"]
            cbsaName = county["cbsaname"]
            #print(line)
            #with open('testOut.json', 'r+') as out:
            #   d = json.     
            line["cbsaname"] = cbsaName
            line["cbsaID"] = cbsaID
            outFile.write(","+json.dumps(line))
            outFile.write("\n")
            
outFile.write("]\n")
            
            


#for county in convertData:

    
    
    
    #if len(str(county["fipscounty"])) == 4:
     #   print(4)

 
# with open("testOut.json", "w") as outFile:
 #   json.dump(cpcData, outFile)

#for x in range(0,numCBSA)