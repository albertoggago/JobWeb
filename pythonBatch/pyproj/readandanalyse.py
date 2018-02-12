#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys
import datetime
import json

#own classes
from Logger import Logger
from mongodbaccess import MongoDBAccess
from mailaccess import MailAccess
from analyzerwebjobs import AnalyzerWebJobs



class ReadAndAnalyse:

	logger          = None
	mongoDBAccess   = None
	mailAccess      = None
	analyzerWebJobs = None

	def __init__(self,fileConfig,visible,levelLog):
		self.logger = Logger(self.__class__.__name__, levelLog).get()
		self.mongoDBAccess = MongoDBAccess(fileConfig,levelLog)
		self.mailAccess    = MailAccess(fileConfig,levelLog)
		configText         = open(fileConfig,"r").read()
		allconfig          = json.loads(configText)
		config        = allconfig.get("webPagesDef",None)
		self.analyzerWebJobs = AnalyzerWebJobs(config,visible,levelLog)

		self.visible = visible
		self.logger.info("Inicio: {0}".format(datetime.datetime.now()))	
  
	def finding_mails(self):
		self.logger.info("find_emails")
		if not self.mailAccess.status(): 
			self.logger.error("Error mail Not Active")
			return None
		if not self.mongoDBAccess.status():
			self.logger.error("Error Database Not Active")
			return None
			
		countEmails = 0;
		listEmails = self.mailAccess.searchMails("inbox")

		for ele in listEmails:
			mail = self.mailAccess.composeMailJson(self.mailAccess.get(ele))
			if mail == None:
				self.logger.error("Mail generate wrong")
			else:
				self.mongoDBAccess.insert("correo",mail)
				countEmails += 1			
				self.mailAccess.store(ele)
		
		#self.mailAccess.clean()
 		self.mailAccess.logout()
 		self.logger.info("emails reads : {0:d}".format(countEmails))
 		return countEmails

 			
	def finding_urls(self):
		self.logger.info("FINDING_URLS")
		if not self.mongoDBAccess.status():
			self.logger.error("Error Database Not Active")
			return None

		countUrls = 0
		mails = self.mongoDBAccess.find("correo",{"control":{"$exists":0}},\
			                                  sort={"urls":1,"_id":1})
		for mail in mails:
			for url in mail.get("urls",[]):
				correoUrl = self.build_mailUrl(mail["_id"],url)
				countUrls += self.review_mailUrl(correoUrl,url)
			
			self.mongoDBAccess.update_one("correo",{"_id":mail["_id"]},{"control":"DONE"})
			
		
		self.logger.info("URLS read: {0:d}".format(countUrls))
		return countUrls			
				
	def build_mailUrl(self,id,url):
		correoUrl = {}
		correoUrl["idCorreo"]= id
		correoUrl["url"]= url
		correoUrl["isSended"]= False
		correoUrl["decision"]= ""
		correoUrl["datetime"]=datetime.datetime.now()
		return correoUrl


	def review_mailUrl(self,mailUrl,url):
		buscarURL = self.mongoDBAccess.find_one("correoUrl",{"url":url})
		if buscarURL == None:
			self.logger.debug("Url to save: {0}".format(url))
			self.mongoDBAccess.insert("correoUrl",mailUrl)
			return 1
		else:
			self.logger.debug("No SAVE URL: {0}".format(url))
			return 0

	def scrap_urls(self):
		self.logger.info("SCRAP_URLS")
		if not self.mongoDBAccess.status():
			self.logger.error("Error Database Not Active")
			return None

		self.reprocess_mails();

		count = {}
		count["Ok"]=0
		count["Error"]=0
		
		correosUrl = self.mongoDBAccess.find("correoUrl",\
			                      {"control":{"$exists":0},"url":{"$exists":1}})
		
		for correoUrl in correosUrl:
			status = self.scrapUrl(correoUrl)
			if status == True:
				count["Ok"] += 1
			else:
				count["Error"] += 1

		self.logger.info("-- INFO -- URLs Analysed Ok : {0:d}, No Ok: {1:d}"\
			                 .format(count["Ok"],count["Error"]))
		self.analyzerWebJobs.closeSelenium()
		return count


	def reprocess_mails(self):
		mailsReprocesError = self.mongoDBAccess.update_many("correoUrl",{"control":"ERROR"},{"control":""},set="unset")
		self.logger.info("Email_Error Reprocess: {0}".format(mailsReprocesError.modified_count))
		mailsReprocesControl = self.mongoDBAccess.update_many("correoUrl",{"control":""},{"control":""},set="unset")
		self.logger.info("Email_Blanck Reprocess: {0}".format(mailsReprocesControl.modified_count))
		


	def scrapUrl(self, correoUrl):
		self.logger.info("SCRAP_URL: {0}".format(correoUrl["url"]))
		info = self.analyzerWebJobs.analyze(correoUrl)
		self.mongoDBAccess.update_one("correoUrl",\
			             {"_id":correoUrl["_id"]},\
			             {"control":info.get("control","ERROR"),"pagina":info.get("page","None")})
		if info.get("status",False) :
			self.saveInformation(correoUrl["_id"],info.get("newCorreoUrl",correoUrl));
		return info.get("status",False)


	def saveInformacion (self, id, correoUrl):
		selg.logger.debug("Save: "+correoUrl)
		self.mongoDBAccess.update_one("correoUrl",{"_id":id},correoUrl)