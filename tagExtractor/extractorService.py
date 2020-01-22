import os,json,config
import numpy as np
import nltk as nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


class TagExtractor:

    def removePunctuation(self, words):
        symbols = "!\"#$%&()*+./:;<=>?@[\]^_`{|}~\n"
        for i in symbols:
            wordsfinal = np.char.replace(words, i, ' ')
        return wordsfinal

    def removeNonString(self, words):
        listOfWords = []
        for i in filter(str.isalpha, words):
            listOfWords.append(i)
        return listOfWords

    def makeAllWordsSmallCaps(self, words):
        return np.char.lower(words)

    def removeRetailerName(self, words, retailerName):
        keywords = []
        retailerName = retailerName.lower()
        retailerName = retailerName.split(' ')
        for i in words:
            if i not in retailerName:
                keywords.append(i)
        return keywords

    def removeSingleCharacterWords(self, words):
        keywords = []
        for i in words:
            if len(i) > 3:
                keywords.append(i)
        return keywords

    def removeStopWords(self, words):
        keywords = []
        stop_words = set(stopwords.words('english'))
        stop_words.update(
            ["also", "founded", "included", "new", "companies", "com", "including", "customers", "customer"])
        for i in words:
            if i not in stop_words:
                keywords.append(i)
        return keywords

    def getTheRelevantWords(self, words, documents, nameOfRetailer):
        mapOfWords = dict.fromkeys(words, 0)
        wordsfinal = set(words)
        for i in wordsfinal:
            for j in documents:
                if i in j:
                    mapOfWords[i] += 1
        processeddict = {k: v for k, v in sorted(mapOfWords.items(), key=lambda item: item[1], reverse=True)}
        return [*processeddict]

    def extractTag(self):
        path = config.FILE_LOCATION
        tagsForAllRetailers = {}
        whereToPickFrom = {'wikipedia': 'paragraphdump', 'crunchbase': 'longdescription', 'yahoo': 'paragraphdump'}
        jsonDocuments = [jsonFile for jsonFile in os.listdir(path)]
        for json_file in jsonDocuments:
            json_file_path = os.path.join(path, json_file)
            with open(json_file_path, "r") as f:
                j = json.load(f)
                arrayOfDocuments = []
                allTheWords = []
                for x, z in whereToPickFrom.items():
                    if x not in j or z not in j[x]:
                        continue
                    refinedText = (str)(self.removePunctuation(j[x][z]))
                    arrayOfDocuments.append(refinedText.lower())
                    allTheWords += set(refinedText.split(' '))
            bagOfTags = self.removeNonString(allTheWords)
            bagOfTags = self.removePunctuation(bagOfTags)
            bagOfTags = self.makeAllWordsSmallCaps(bagOfTags)
            bagOfTags = self.removeStopWords(bagOfTags)
            bagOfTags = self.removeSingleCharacterWords(bagOfTags)
            bagOfTags = self.removeRetailerName(bagOfTags, json_file.split('.')[0])
            relevantTags = self.getTheRelevantWords(bagOfTags, arrayOfDocuments, json_file.split('.')[0])
            tagsForAllRetailers[json_file.split('.')[0]] = relevantTags[0:25]
        return json.dumps(tagsForAllRetailers)
