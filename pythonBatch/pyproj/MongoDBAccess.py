from pymongo import MongoClient
from Logger import Logger
import json

#class for analize emails.
class MongoDBAccess():

	status = False;
	db = None;

	def __init__(self,fileName):
		self.logger = Logger(self.__class__.__name__).get()
		configText = open(fileName,"r").read()
		config = json.loads(configText)

		try:
  			client = MongoClient(config["url"])
  			self.db = client[config["nameDB"]]
  			param = self.db.correoUrl.find_one()
  		except:
  			self.logger.error("Error acceso")
  			param = None


  		if param == None:
			self.logger.error("base de datos parada o param no inicializado")
			self.status = False
		else:
			self.logger.info("-- INFO -- Conexion a base de datos OK")
			self.status = True

	def find_one(self,collection,query):
		if self.status:
			self.logger.debug("Access to collection: {0}, query {1}".format(collection,query))
			return self.db[collection].find_one(query)
		else:
			self.logger.error("Bases de datos no inicalizada Find_one")
			return None

	def find(self,collection,query,sort=None):
		if self.status:
			self.logger.debug("Access to collection Multi: {0}, query {1}, sort: {2}"\
				.format(collection,query,sort))
			return self.db[collection].find(query,sort)
		else:
			self.logger.error("Bases de datos no inicalizada Find")
			return None

	def update_one(self,collection,query,change, set="set"):
		if self.status:
			self.logger.debug("Modify collection: {0}, query {1}, modify: {2}, set: {3}"\
				.format(collection,query, change,set))
			setdollar = "$"+set
			return self.db[collection].update_one(query,{setdollar:change})
		else:
			self.logger.error("Bases de datos no inicalizada Update_one")
			return None

	def update_many(self,collection,query,change, set="set"):
		if self.status:
			self.logger.debug("Modify Many collection: {0}, query {1}, modify: {2}, set: {3}"\
				.format(collection,query, change,set))
			setdollar = "$"+set
			return self.db[collection].update_many(query,{setdollar:change})
		else:
			self.logger.error("Bases de datos no inicalizada Update_one")
			return None

	def insert(self,collection,element):
		if self.status:
			self.logger.debug("Insert collection: {0}, data {1}".format(collection,element))
			return self.db[collection].insert(element)
		else:
			self.logger.error("Bases de datos no inicalizada Find")
			return None

	def delete_one(self,collection,element):
		if self.status:
			self.logger.debug("Remove collection: {0}, data {1}".format(collection,element))
			return self.db[collection].delete_one(element)
		else:
			self.logger.error("Bases de datos no inicalizada Find")
			return None

