from pyspark import SparkConf, SparkContext
import collections, time, html2text, sys, config
#from lxml import html
#from lxml.html.clean import Cleaner

from bs4 import BeautifulSoup
import json

from templates.crunchbase import extractor as crunchextract
from templates.wikipedia import extractor as wikiextract


conf = SparkConf().setMaster("local").setAppName(config.APP_NAME)
sc = SparkContext(conf = conf)

stime = time.time()
print("Current encoding : "+sys.getdefaultencoding())


lines = sc.textFile(config.LOCAL_FILE_PATH)
#brands = lines.map(lambda x: getBrand(x.split('|||||')[0],x.split('|||||')[1]))
brands = lines.map(lambda x: x.split(config.BRAND_DUMP_DELIMETER)[0])
brandResult = brands.countByValue()

sortedResults = collections.OrderedDict(sorted(brandResult.items()))
#print("Brand\t\t\t| No. of articles")
print("-----------------------------------------------")
for key, value in sortedResults.items():
	print("%s \t\t-\t\t %i" % (key, value))
	article = lines.filter(lambda x : x.split(config.BRAND_DUMP_DELIMETER)[0]==key).map(lambda x: (x.split(config.BRAND_DUMP_DELIMETER)[1],x.split(config.BRAND_DUMP_DELIMETER)[2]))
	#print(article)
	result = article.collect()
	#print(result)
	articleCount = 1
	retailerdict = {}
	for (source,i) in result:
		#print(i)
		print("\t Source : "+source)
		soup = BeautifulSoup(i,'lxml')
		soup.encode("utf-8")
		
		# remove all javascript and stylesheet code
		for script in soup(["script", "style"]): 
			script.extract()
		
		h1 = soup.find('h1').text

		if source == 'wikipedia':
			wiki = wikiextract.WikiExtractor()
			wikidict = wiki.extract(soup)
			retailerdict['wikipedia']=wikidict
			#print(wikidict)
		elif source == 'crunchbase':
			crunchbase = crunchextract.CrunchbaseExtractor()
			crunchdict = crunchbase.extract(soup)
			retailerdict['crunchbase']=crunchdict
			#print(crunchdict)
	with open('output/'+key+'.json', 'w') as fp:
		json.dump(retailerdict, fp,indent=4)

etime = time.time()


print("Total time taken = {time} seconds".format(time=(etime-stime)))