LOCAL_FILE_PATH="file:///workspace/html-content-extractor/data/dump.txt"
#LOCAL_FILE_PATH="file:///SAMS/workspace/python/html-content-extractor/data/dump.txt"
#LOCAL_FILE_PATH="file:///./data/dump.txt"
BRAND_DUMP_DELIMETER='|||||'
APP_NAME='RSP1'
MASTER_NODE_MAP={'cluster':'spark://10.0.75.1:7077','local':'local'}
TAG_EXTRACTOR_URL="http://taggenerator:5000/getTags/{brand}"

COSMOS_END_POINT = "https://rspoc.documents.azure.com:443/"
COSMOS_KEY = 'F9FllTJ6Iq5ZzAtihWlajKoBbo3Yk5B5H8pQbfHx3d1SSiMvpT9Q4blbDes3QVZ0iAHrfh0cll4o0Fuyg5rmPg=='
COSMOS_PARTITION_KEY = 'retailer'
COSMOS_DB_NAME= 'RS-Crawl'
COSMOS_CONTAINER_NAME= 'retailers'
COSMOS_FIND_QUERY = "SELECT * FROM retailers r where r.retailer='{retailername}'"
COSMOS_DB_LINK="dbs/" + COSMOS_DB_NAME + "/colls/" + COSMOS_CONTAINER_NAME