def connect (uri):
	from pymongo import MongoClient

	client = MongoClient(uri)

	return client