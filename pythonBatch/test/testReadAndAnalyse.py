import sys
import os


sys.path.insert(0, "../pyproj")
try:
    from ReadAndAnalyse import ReadAndAnalyse
    from MongoDBAccess import MongoDBAccess
except ImportError:
    print('No Import')



def test_init_correct():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",True)
	assert readAndAnalyse.mongoDBAccess.status()
	assert readAndAnalyse.mailAccess.status()
	
def test_init_ErrorMongo():
	readAndAnalyse = ReadAndAnalyse("../test/config/configMongoDBError.json",True)
	assert not readAndAnalyse.mongoDBAccess.status()
	assert readAndAnalyse.mailAccess.status()

def test_init_ErrorMail():
	readAndAnalyse = ReadAndAnalyse("../test/config/configMailError.json",True)
	assert readAndAnalyse.mongoDBAccess.status()
	assert not readAndAnalyse.mailAccess.status()

def test_findingMails():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",True)
	mongoDBAccess =  MongoDBAccess("../test/config/configOk.json")
	mongoDBAccess.delete_many("correo",{})
	amount =  readAndAnalyse.finding_mails()
	#Depends of the emails in the mail test
	assert amount == 2

def test_findingUrls():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",True)
	mongoDBAccess =  MongoDBAccess("../test/config/configOk.json")
	mongoDBAccess.delete_many("correo",{})
	mongoDBAccess.delete_many("correoUrl",{})
	readAndAnalyse.finding_mails()
	amount =  readAndAnalyse.finding_urls()
	#Depends of the information inside of mails
	assert amount == 33
	
	dones = mongoDBAccess.find("correo",{"control":"DONE"})
	amountDones = 0
	for done in dones:
		amountDones += 1
	#Depends of the information inside of mails
	assert amountDones == 2
	
	correosUrls = mongoDBAccess.find("correoUrl",{})
	amountCorreosUrls = 0
	for correoUrl in correosUrls:
		amountCorreosUrls += 1
	#Depends of the information inside of mails
	assert amountCorreosUrls == 33

def test_scrapUrls():
	readAndAnalyse = ReadAndAnalyse("../test/config/configOk.json",False)
	mongoDBAccess =  MongoDBAccess("../test/config/configOk.json")
	mongoDBAccess.delete_many("correo",{})
	mongoDBAccess.delete_many("correoUrl",{})
	readAndAnalyse.finding_mails()
	readAndAnalyse.finding_urls()
	amount = readAndAnalyse.scrap_urls()
	#Depends of the information inside of mails
	assert amount == 33