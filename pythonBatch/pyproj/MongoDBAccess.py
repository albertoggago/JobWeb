from pymongo import MongoClient
from Logger import Logger
import json

#class for analize emails.
class MongoDBAccess():

	status = None;
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