from base import BaseExtractor
import crunchconfig

class CrunchbaseExtractor(BaseExtractor):

	def extract(self, soup):
			crunchdict = {}
			#Initialize the keys and values list
			values = []
			keys = []

			#ranking extraction
			cbrows = soup.find_all('div',attrs={"class":["flex-100","flex-gt-sm-50","bigValueItem","layout-column"]})
			for cbrow in cbrows:
				if cbrow.find('span',attrs={"class":"wrappable-label-with-info ng-star-inserted"}) is not None and cbrow.find('span',attrs={"class":"wrappable-label-with-info ng-star-inserted"}) is not None:
					cbkey = cbrow.find('span',attrs={"class":"wrappable-label-with-info ng-star-inserted"}).get_text(strip=True)
					cbvalue = cbrow.find('field-formatter',attrs={"contexttype":"profile"}).get_text(strip=True)
					#print(cbkey,cbvalue)
					values.append(cbvalue)
					keys.append(cbkey)
			#print(dict(zip(keys, values)))
			bigpaneldict = dict(zip(keys, values))
			crunchdict.update(bigpaneldict)

			#Extracting the tablular information first
			values = []
			keys = []
			fieldscards = soup.find_all('fields-card',attrs={"class":"ng-star-inserted"})
			if fieldscards is not None:
				for fieldcard in fieldscards:
					keys_el = fieldcard.find_all('span',attrs={"class":"wrappable-label-with-info ng-star-inserted"})
					values_el = fieldcard.find_all('field-formatter',attrs={"contexttype":"profile"})
					values = values + [i.get_text(strip=True) for i in values_el]
					keys = keys + [i.get_text(strip=True) for i in keys_el]
				#print(dict(zip(keys, values)))
				tablepaneldict = dict(zip(keys, values))
				crunchdict.update(tablepaneldict)

			# description extraction
			descriptiondict = {}
			smalldescription = soup.find('span',attrs={"class":"component--field-formatter field-type-text_long ng-star-inserted"})
			if smalldescription is not None:
				#descriptiondict['smalldescription'] = smalldescription.get_text(strip=True)
				descriptiondict['smalldescription'] = str(smalldescription.get_text(strip=True).encode("ascii", "ignore"),"utf-8")
				
				#print(smalldescription.get_text(strip=True))

			longdescription = soup.find('description-card')
			if longdescription is not None:
				#descriptiondict['longdescription'] = longdescription.get_text(strip=True)
				descriptiondict['longdescription'] = str(longdescription.get_text(strip=True).encode("ascii", "ignore"),'utf-8')
				#print(longdescription.get_text(strip=True))
			crunchdict.update(descriptiondict)

			crunchdict.update(self.getinsights(soup))

			return crunchdict

	def getinsights(self,soup):
		insightdict = {}
		#ranking extraction
		insightphrases = [str(i.text.encode("ascii", "ignore"),'utf-8') for i in soup.find_all('phrase-list-card')]
		insightdict['insights'] = insightphrases
		return insightdict
