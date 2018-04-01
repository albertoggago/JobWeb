import sys
import os
import logging

sys.path.insert(0, "..")
try:
    from pyproj.readandanalyse import ReadAndAnalyse
    from pyproj.mongodbaccess import MongoDBAccess
except ImportError:
    print('No Import')



def test_init_correct():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",logging.ERROR)
	assert readAndAnalyse.mongo_db_access.status()
	assert readAndAnalyse.mail_access.status()
	
def test_init_ErrorMongo():
	readAndAnalyse = ReadAndAnalyse("../test/config/configMongoDBError.json",logging.ERROR)
	assert not readAndAnalyse.mongo_db_access.status()
	assert readAndAnalyse.mail_access.status()

def test_init_ErrorMail():
	readAndAnalyse = ReadAndAnalyse("../test/config/configMailAccessError.json",logging.ERROR)
	assert readAndAnalyse.mongo_db_access.status()
	assert not readAndAnalyse.mail_access.status()

def test_findingMails():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",logging.ERROR)
	mongoDBAccess =  MongoDBAccess("../test/config/configOk.json","DEBUG")
	mongoDBAccess.delete_many("correo",{})
	amount =  readAndAnalyse.finding_mails()
	#Depends of the emails in the mail test
	assert amount == 6

def test_findingUrls():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",logging.ERROR)
	mongoDBAccess =  MongoDBAccess("../test/config/configOk.json","WARNING")
	mongoDBAccess.delete_many("correo",{})
	mongoDBAccess.delete_many("correoUrl",{})
	readAndAnalyse.finding_mails()
	amount =  readAndAnalyse.finding_urls()
	#Depends of the information inside of mails
	assert amount == 131
	
	dones = mongoDBAccess.find("correo",{"control":"DONE"})
	amountDones = 0
	for done in dones:
		amountDones += 1
	#Depends of the information inside of mails
	assert amountDones == 6
	
	correosUrls = mongoDBAccess.find("correoUrl",{})
	amountCorreosUrls = 0
	for correoUrl in correosUrls:
		amountCorreosUrls += 1
	#Depends of the information inside of mails
	assert amountCorreosUrls == 131

def test_scrapUrls():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",logging.ERROR)
	mongoDBAccess =  MongoDBAccess("../test/config/configOk.json",logging.ERROR)
	mongoDBAccess.delete_many("correo",{})
	mongoDBAccess.delete_many("correoUrl",{})
	readAndAnalyse.finding_mails()
	readAndAnalyse.finding_urls()
	amount = readAndAnalyse.scrap_urls(10)
	#Depends of the information inside of mails
	assert amount == {"ERROR":10}