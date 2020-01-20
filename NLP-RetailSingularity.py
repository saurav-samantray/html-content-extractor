#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os,json
import numpy as np
import nltk as nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def removePunctuation(words):
    symbols = "!\"#$%&()*+./:;<=>?@[\]^_`{|}~\n"
    for i in symbols:
        words = np.char.replace(words, i, ' ')
    return words



def removeNonString(words):
    listOfWords = []
    for i in filter(str.isalpha, words):
        listOfWords.append(i)
    return listOfWords


def makeAllWordsSmallCaps(words):
    return np.char.lower(words)
    

def removeRetailerName(words,retailerName):
    keywords = []
    retailerName= retailerName.lower()
    retailerName = retailerName.split(' ')
    for i in words:
        if i not in retailerName:
            keywords.append(i)
    return keywords


def removeSingleCharacterWords(words):
    keywords = []
    for i in words:
        if len(i) > 3:
            keywords.append(i)
    return keywords

def removeStopWords(words):
    keywords = []
    stop_words = set(stopwords.words('english')) 
    stop_words.update(["also","founded","included","new","companies","com","including","customers","customer"])
    for i in words:
        if i not in stop_words:
            keywords.append(i)
    return keywords

def getTheRelevantWords(words,documents,nameOfRetailer):
    mapOfWords = dict.fromkeys(words,0)
    words = set(words)
    for i in words:
        for j in documents:
            if i in j:
                mapOfWords[i] += 1   
    processedDict = {k: v for k, v in sorted(mapOfWords.items(), key=lambda item: item[1], reverse= True)}
    return [*processedDict]

path = "output"
tagsForAllRetailers ={}
whereToPickFrom = {'wikipedia':'paragraphdump','crunchbase':'longdescription','yahoo' : 'paragraphdump'}
jsonDocuments = [jsonFile for jsonFile in os.listdir(path)]
for json_file in jsonDocuments:
    json_file_path = os.path.join(path, json_file)
    with open (json_file_path, "r") as f:
        j = json.load(f)
        arrayOfDocuments = []
        allTheWords = []
        for x,z in whereToPickFrom.items():
            if x not in j or z not in j[x]:
                continue
            refinedText = (str)(removePunctuation(j[x][z]))
            arrayOfDocuments.append(refinedText.lower())
            allTheWords += set(refinedText.split(' '))
    bagOfTags = removeNonString(allTheWords)
    bagOfTags = removePunctuation(bagOfTags)
    bagOfTags = makeAllWordsSmallCaps(bagOfTags)
    bagOfTags = removeStopWords(bagOfTags)
    bagOfTags = removeSingleCharacterWords(bagOfTags)
    bagOfTags = removeRetailerName(bagOfTags,json_file.split('.')[0])
    relevantTags = getTheRelevantWords(bagOfTags,arrayOfDocuments,json_file.split('.')[0])
    tagsForAllRetailers[json_file.split('.')[0]] = relevantTags[0:25]

print(json.dumps(tagsForAllRetailers))





