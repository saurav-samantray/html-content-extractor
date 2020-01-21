from pyspark import SparkConf, SparkContext
import collections, time, html2text, sys

#from lxml import html
#from lxml.html.clean import Cleaner

from bs4 import BeautifulSoup
import json

import config
from templates.crunchbase import extractor as crunchextract
from templates.wikipedia import extractor as wikiextract
from templates.yahoo import extractor as yahooextract



def runtask(retailers,sourcepath):
	try:
		conf = SparkConf().setMaster("local").setAppName("RSP1")
		sc = SparkContext(conf = conf)
		sc.setLogLevel("WARN")

		stime = time.time()
		jobid = sc._jsc.sc().applicationId()
		filepath = sourcepath if sourcepath is not None else config.LOCAL_FILE_PATH
		print(f"Created job : {jobid}")
		print("Current encoding : "+sys.getdefaultencoding())
		
		#read the source content	
		lines = sc.textFile(filepath)

		result = None
		print("lines : ",type(lines))
		if not lines.isEmpty():
			if retailers is None or len(retailers) == 0:
				print("No list provided, processing the complete dump of available names")
				result = lines\
				.map(extract)\
				.reduceByKey(merge_two_dicts)\
				.collect()

			else:
				print(f"Processing records for : {retailers}")
				result = lines\
				.filter(lambda x : x.split(config.BRAND_DUMP_DELIMETER)[0] in retailers)\
				.map(extract)\
				.reduceByKey(merge_two_dicts)\
				.collect()

		
		etime = time.time()
		
		print(jobid+" complete")
		sc.stop()
		print("Total time taken = {time} seconds".format(time=(etime-stime)))
		return dict(result)
	except Exception as e:
		print(e)
		response = {"success":False,"error":"some error occured"}
		return response

def merge_two_dicts(x, y):
    # from https://stackoverflow.com/a/26853961/5858851
    # works for python 2 and 3
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def extract(row):
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

if __name__ == '__main__':
	print("Executing Spark Job in local mode")
	runtask()