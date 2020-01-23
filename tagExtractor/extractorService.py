import os,json,config
import numpy as np
import nltk as nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class TagExtractor:

    def remove_verb_adverb_adjective(self, words):
        verb_container = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'RB', 'RBR', 'RBS', 'RP', 'JJ',
                            'JJR', 'JJS', 'DT','MD', 'WP', 'WDT', 'WP$']
        tagged_words = nltk.pos_tag(words)
        words_list = [w[0] for w in tagged_words if not w[1] in verb_container]
        return words_list

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

    def lemmatization(self, words):
        keywords = []
        lemmatizer = WordNetLemmatizer()
        for i in words:
            if len(i) > 3:
                keywords.append(lemmatizer.lemmatize(i))
        return keywords


    def removeStopWords(self, words):
        keywords = []
        stop_words = set(stopwords.words('english'))
        stop_words.update(
            ["also", "founded", "included", "new", "companies", "com", "including", "customers", "customer","price",
            "retailer"])
        for i in words:
            if i not in stop_words:
                keywords.append(i)
        return keywords

    def get_the_relevant_words(self, words, documents, nameOfRetailer):
        mapOfWords = dict.fromkeys(words, 0)
        wordsfinal = set(words)
        for i in wordsfinal:
            for j in documents:
                if i in j:
                    mapOfWords[i] += 1
        processed_dict = {k: v for k, v in sorted(mapOfWords.items(), key=lambda item: item[1], reverse=True)}
        return [*processed_dict]

    def extractTag(self, brand):
        path = config.FILE_LOCATION
        tagsForAllRetailers = {}
        whereToPickFrom = {'wikipedia': 'paragraphdump', 'crunchbase': 'longdescription', 'yahoo': 'paragraphdump'}
        jsonDocuments = [jsonFile for jsonFile in os.listdir(path)]
        for json_file in jsonDocuments:
            if brand.lower() in json_file.lower():
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
                        allTheWords += nltk.word_tokenize(refinedText)
                bagOfTags = self.removeNonString(allTheWords)
                bagOfTags = self.lemmatization(bagOfTags)
                bagOfTags = self.removeStopWords(bagOfTags)
                bagOfTags = self.remove_verb_adverb_adjective(bagOfTags)
                bagOfTags = self.removePunctuation(bagOfTags)
                bagOfTags = self.makeAllWordsSmallCaps(bagOfTags)
                bagOfTags = self.removeRetailerName(bagOfTags, json_file.split('.')[0])
                relevantTags = self.get_the_relevant_words(bagOfTags, arrayOfDocuments, json_file.split('.')[0])
                tagsForAllRetailers[json_file.split('.')[0]] = relevantTags[0:21]
        return tagsForAllRetailers
