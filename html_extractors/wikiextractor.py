import re

class WikiExtractor:

	def getparagraphdump(self,soup):
		content = soup.find('div',attrs={'id':'mw-content-text'})
		if content is not None:
			paras_el = content.find_all('p')
			paras = [re.sub(" ?\[[(0-9)]+\]"," ",i.get_text(strip=False)) for i in paras_el]
			return '. '.join(paras)

	def populatetabledata(self,soup,wikidict):
		table = soup.find_all('table',attrs={"class":"infobox vcard"})
		if table is not None and len(table) != 0:
			for row in table[0].find_all("tr"):
				thcolumns = row.find_all('th')
				headValue = ""
				for column in thcolumns:
					headValue = column.text
					tdcolumns = row.find_all('td')
					for column in tdcolumns:
						#print(headValue+" - " + column.text)
						wikidict[headValue] = column.get_text(strip=True)

	def extract(self, soup):
		#intialize the wikipedia dictonary
		wikidict = {}

		#get body dump
		paragraphdump = self.getparagraphdump(soup)
		wikidict['paragraphdump'] = str(paragraphdump.encode("ascii", "ignore"),'utf-8')

		#populate the wiki info table content
		self.populatetabledata(soup,wikidict)
		return wikidict


