from pyspark import SparkConf, SparkContext
import collections, time, html2text, sys

#from lxml import html
#from lxml.html.clean import Cleaner

from bs4 import BeautifulSoup
import json



def runtask():
	conf = SparkConf().setMaster("spark://10.0.75.1:7077").setAppName("RSP1").set("spark.cores.max", "1")
	sc = SparkContext(conf = conf)
	sc.setLogLevel("WARN")
	sc.addFile("mainconfig.py")
	sc.addFile("main.py")
	sc.addFile("templates2/base.py")
	sc.addFile("templates2/crunchextractor.py")
	sc.addFile("templates2/crunchconfig.py")
	sc.addFile("templates2/wikiextractor.py")
	sc.addFile("templates2/wikiconfig.py")
	sc.addFile("templates2/yahooextractor.py")
	sc.addFile("templates2/yahooconfig.py")

	import mainconfig as config
	import crunchextractor as crunchextract
	import wikiextractor as wikiextract
	import yahooextractor as yahooextract

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
		#article = lines.filter(lambda x : x.split(config.BRAND_DUMP_DELIMETER)[0]==key).map(lambda x: (x.split(config.BRAND_DUMP_DELIMETER)[1],x.split(config.BRAND_DUMP_DELIMETER)[2]))
		article = lines.filter(lambda x : x.split(config.BRAND_DUMP_DELIMETER)[0]==key).map(extract).reduceByKey(lambda p,q: p+q)
		#print(article)
		result = article.collect()
		print(result)
		articleCount = 1
		retailerdict = {}
	etime = time.time()
	jobid = sc._jsc.sc().applicationId()
	print(jobid+" ------")
	sc.stop()
	print("Total time taken = {time} seconds".format(time=(etime-stime)))
	return jobid

def extract(row):
	import mainconfig as config
	import crunchextractor as crunchextract
	import wikiextractor as wikiextract
	import yahooextractor as yahooextract
	source = row.split(config.BRAND_DUMP_DELIMETER)[1]
	html = row.split(config.BRAND_DUMP_DELIMETER)[2]
	#print(f"extraction for {source}")
	#print(i)
	print("\t Source : "+source)
	soup = BeautifulSoup(html,'lxml')
	soup.encode("utf-8")

	# remove all javascript and stylesheet code
	for script in soup(["script", "style"]): 
		script.extract()

	h1 = soup.find('h1').text

	retailerdict = {}

	if source == 'wikipedia':
		wiki = wikiextract.WikiExtractor()
		wikidict = wiki.extract(soup)
		retailerdict['wikipedia']=wikidict
	#print(wikidict)
	elif source == 'crunchbase':
		crunchbase = crunchextract.CrunchbaseExtractor()
		crunchdict = crunchbase.extract(soup)
		retailerdict['crunchbase']=crunchdict
	elif source in ['yahoonews1', 'yahoofinance1']:
		yahoo = yahooextract.YahooExtractor()
		yahoodict = yahoo.extract(soup)
		retailerdict['yahoo']=yahoodict
		#print(crunchdict)
	#print(retailerdict)
	'''
	with open('output/'+key+'.json', 'w') as fp:
		json.dump(retailerdict, fp,indent=4)
	'''
	return source, retailerdict