#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Rohan Damodar"

import json
from demjson import decode
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def cleanJson(filename):
    print "Your file will be saved as 'newFile.json' in current directory!"
    
    with open(filename) as f:
        contents = f.readlines()
     
    with open('newFile.json', 'a') as outfile:  
        for line in contents:
            dic = decode(line) # convert line from JSON to Python dictionary
            json_obj = json.dumps(dic) # convert dic to a string representing a json object
            outfile.write(json_obj) # write to outfile
            outfile.write("\n")

def sentiments(column):
    lis = []
    analyser = SentimentIntensityAnalyzer()
    for i in column:
        sent = analyser.polarity_scores(i)
        lis.append(sent['compound'])
    return map(lambda i: 'positive' if 0<=i else 'negative', lis)