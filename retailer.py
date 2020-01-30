import uuid

class Retailer:

	def __init__(self,retailer,dataExtracted):
		self.id = 'retailer_' + str(uuid.uuid4())
		self.retailer = retailer
		self.dataExtracted = dataExtracted

