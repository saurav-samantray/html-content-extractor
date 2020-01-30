import azure.cosmos.cosmos_client as cosmos_client
import os, json
import config

from retailer import Retailer


def create_item(retailer):
	# Initialize the Cosmos client
	endpoint = config.COSMOS_END_POINT
	key = config.COSMOS_KEY
	client = cosmos_client.CosmosClient(config.COSMOS_END_POINT, {'masterKey': config.COSMOS_KEY})

	query = config.COSMOS_FIND_QUERY

	#sample_retailer = Retailer('dummyretailer',{'crunchbase':{'from':'crunchbase'}}).__dict__

	items = list(client.QueryItems(\
			 config.COSMOS_DB_LINK,query.format(retailername=retailer['retailer']),\
			 options=None, partition_key=config.COSMOS_PARTITION_KEY))


	if len(items) == 0:	
		client.CreateItem(config.COSMOS_DB_LINK,retailer, {'enableCrossPartitionQuery': True})
		print("Item created entry for : "+retailer['retailer'])
	elif len(items) == 1:
		doc_link = items[0]['_self']
		client.ReplaceItem(doc_link,retailer)
		print("Document already exists for retailer : "\
			  +retailer['retailer'] + " with id : "+items[0]['id']\
			  +" replacing with new document : "+retailer['id'])
	else:
		doc_link = items[0]['_self']
		client.ReplaceItem(doc_link,retailer)
		print("Multiple documents exists for retailer : "\
			  +retailer['retailer'] + ", replaced id : "+items[0]['id']\
			  +" with id : "+retailer['id'])