from pymongo import MongoClient
from Logger import Logger
import json

#class for analize emails.
class MongoDBAccess():

	db = None;
	_client = None;

	def __init__(self,fileName,levelLog):
		self.logger = Logger(self.__class__.__name__,levelLog).get()
		self.logger.setLevel('INFO')
		configText = open(fileName,"r").read()
		config = json.loads(configText)

		try:
  			self.logger.debug(config["url"])
  			self._client = MongoClient(config["url"])
  			self.db = self._client[config["nameDB"]]
			self.logger.info("-- INFO -- DATA BASE CONECT OK")
  		except:
  			self.logger.error("DATA BASE STOP")
 
	def status (self):
		try:
	 		self.logger.debug(self._client.server_info())
	 		return True
	 	except:
 			self.logger.error("DATA BASE STOP")
 	 		return False
 

	def find_one(self,collection,query):
		if self.status():
			self.logger.info("Access to collection: {0}, query {1}".format(collection,query))
			return self.db[collection].find_one(query)
		else:
			self.logger.error("Database Not INIT Find_one")
			return None

	def find(self,collection,query,sort=None):
		if self.status():
			self.logger.info("Access to collection Multi: {0}, query {1}, sort: {2}"\
				.format(collection,query,sort))
			return self.db[collection].find(query,sort)
		else:
			self.logger.error("Database Not INIT Find")
			return None

	def update_one(self,collection,query,change, set="set"):
		if self.status():
			self.logger.info("Modify collection: {0}, query {1}, modify: {2}, set: {3}"\
				.format(collection,query, change,set))
			setdollar = "$"+set
			return self.db[collection].update_one(query,{setdollar:change})
		else:
			self.logger.error("Database Not INIT Update_one")
			return None

	def update_many(self,collection,query,change, set="set"):
		if self.status():
			self.logger.info("Modify Many collection: {0}, query {1}, modify: {2}, set: {3}"\
				.format(collection,query, change,set))
			setdollar = "$"+set
			return self.db[collection].update_many(query,{setdollar:change})
		else:
			self.logger.error("Database Not INIT Update_one")
			return None

	def insert(self,collection,element):
		if self.status():
			self.logger.debug("Insert collection: {0}, data {1}".format(collection,element))
			return self.db[collection].insert(element)
		else:
			self.logger.error("Database Not INIT Find")
			return None

	def delete_one(self,collection,element):
		if self.status():
			self.logger.info("Remove collection: {0}, data {1}".format(collection,element))
			return self.db[collection].delete_one(element)
		else:
			self.logger.error("Database Not INIT Find")
			return None

	def delete_many(self,collection,element):
		if self.status():
			self.logger.info("Remove collection: {0}, data {1}".format(collection,element))
			return self.db[collection].delete_many(element)
		else:
			self.logger.error("Database Not INIT Find")
			return None

	def drop(self,collection):
		if self.status():
			self.logger.info("Drop collection: {0}".format(collection))
			return self.db[collection].drop()
		else:
			self.logger.error("Database Not INIT Find")
			return None
