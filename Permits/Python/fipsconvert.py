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
import json
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

input_file = open('data/Ohio.json' , 'r')
output_file = open('data/test.json' , 'w')

json_decode=json.load(input_file)

result = []

for item in json_decode:
    my_dict={}
    my_dict['title']=item.get('labels').get('en').get('value')
    my_dict['description']=item.get('descriptions').get('en').get('value')
    my_dict['id']=item.get('id')
    print my_dict
back_json=json.dumps(my_dict, output_file)
output_file.write(back_json)
output_file.close()
