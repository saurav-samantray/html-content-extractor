import json
import collections
import time
import sys

import requests
import html2text
from pyspark import SparkConf, SparkContext
from bs4 import BeautifulSoup
from retailer import Retailer
import cosmos



def runtask(retailers,master):
	try:
		conf = SparkConf()\
		.setMaster(master)\
		.setAppName("RSP1")\
		.set("spark.cores.max","2")\
		.set("spark.executor.memory","1g")
		
		sc = SparkContext(conf = conf)
		sc.setLogLevel("WARN")
		sc.addFile("config.py")
		sc.addFile("main.py")
		sc.addFile("html_extractors/baseextractor.py")
		sc.addFile("html_extractors/crunchextractor.py")
		sc.addFile("html_extractors/wikiextractor.py")
		sc.addFile("html_extractors/yahooextractor.py")

		#Initializing the log4J logger from spark context
		log4jLogger = sc._jvm.org.apache.log4j
		LOGGER = log4jLogger.LogManager.getLogger(__name__)
		LOGGER.info("pyspark script logger initialized")

		import config
		

		stime = time.time()
		jobid = sc._jsc.sc().applicationId()
		filepath = config.LOCAL_FILE_PATH
		print("Created job : {jobid}".format(jobid=jobid))
		print("Reading file : {filepath} ".format(filepath=filepath))
		print("Current encoding : "+sys.getdefaultencoding())
		
		#read the source content	
		lines = sc.textFile(filepath)

		result = {}
		#print("lines : ",type(lines))

		if retailers is None or len(retailers) == 0:
			LOGGER.info("No list provided, processing the complete dump of available names")
			result = lines\
			.map(extractkeys)\
			.reduceByKey(merge_two_dicts)\
			.map(update_item)\
			.collect()

		else:
			print("Processing records for : {retailers}".format(retailers=retailers))
			result = lines\
			.filter(lambda x : x.split(config.BRAND_DUMP_DELIMETER)[0] in retailers)\
			.map(extractkeys)\
			.reduceByKey(merge_two_dicts)\
			.map(update_item)\
			.collect()

		etime = time.time()
		
		print(jobid+" complete")
		sc.stop()
		print("Total time taken = {time} seconds".format(time=(etime-stime)))
		#return dict(result)
	except Exception as e:
		LOGGER.error(e)
		response = {"success":False,"error":"some error occured"}
		return response

def merge_two_dicts(x, y):
    # from https://stackoverflow.com/a/26853961/5858851
    # works for python 2 and 3
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def extractkeys(row):
	import config
	import crunchextractor as crunchextract
	import wikiextractor as wikiextract
	import yahooextractor as yahooextract

	retailer = row.split(config.BRAND_DUMP_DELIMETER)[0]
	source = row.split(config.BRAND_DUMP_DELIMETER)[1]
	html = row.split(config.BRAND_DUMP_DELIMETER)[2]
	#print(f"extraction for {source}")
	#print(i)
	#print("\t Source : "+source)
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
	elif source in ['yahoonews', 'yahoofinance']:
		yahoo = yahooextract.YahooExtractor()
		yahoodict = yahoo.extract(soup)
		retailerdict['yahoo']=yahoodict
		#print(crunchdict)
	#print(retailerdict)
	'''
	with open('output/'+key+'.json', 'w') as fp:
		json.dump(retailerdict, fp,indent=4)
	'''
	return (retailer, retailerdict)

def update_item(item):
	import config
	
	retailerDoc = Retailer(item[0],item[1])
	#print(retailerDoc.__dict__)
	cosmos.create_item(retailerDoc.__dict__)
	'''
	try:
		response = requests.get(config.TAG_EXTRACTOR_URL.format(brand=item[0]))
		#print(json.loads(response.text))
		if response.text is not None and len(item)>1:
			item[1]['tags']= json.loads(response.text).get(item[0])
			#pass
	except Exception:
		print("Error occured while fetching tags. Skipping step")
	'''
	return item
	

if __name__ == '__main__':
	print("Initiating spark job in local mode")
	print(runtask(None,'local'))