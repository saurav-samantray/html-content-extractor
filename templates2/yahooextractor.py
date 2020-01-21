from base import BaseExtractor
import yahooconfig

class YahooExtractor(BaseExtractor):

	def getparagraphdump(self,soup):
		content = soup.find('article')
		if content is not None:
			paras_el = content.find_all('p')
			paras = [i.get_text(strip=False) for i in paras_el]
			return '. '.join(paras)


	def extract(self, soup):
		#intialize the yahoo dictonary
		yahoodict = {}

		#get body dump
		paragraphdump = self.getparagraphdump(soup)
		#print()
		yahoodict['paragraphdump'] = str(paragraphdump.encode("ascii", "ignore"),'utf-8')

		return yahoodict


