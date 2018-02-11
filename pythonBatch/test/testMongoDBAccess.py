import sys
import os
import random

sys.path.insert(0, "../pyproj")
try:
    from MongoDBAccess import MongoDBAccess
except ImportError:
    print('No Import')

def test_mongodbAcessOk():
	mongoDBAccessOk = MongoDBAccess("../test/config/configOk.json")
	
	assert mongoDBAccessOk.status()

def test_mongodbAcessError():
    mongoDBAccessError = MongoDBAccess("../test/config/configMongoDBError.json")
	
    assert not mongoDBAccessError.status()

def test_mongoDBAccess_find_oneOK():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testFindOne",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find_one("testFindOne",{"clave":"IPFind"})
	mongoDBAccess.drop("testFindOne")
	
	assert res!= None 

def test_mongoDBAccess_find_oneErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/configMongoDBError.json")
	resInsert     = mongoDBAccess.insert("testFindOneErrorDB",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find_one("testFindOneErrorDB",{"clave":"IPFind"})
	mongoDBAccess.drop("testFindOneErrorDB")
	
	assert res== None 

def test_mongoDBAccess_find_oneErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testFindOneErrorCollection",{"clave":"IPFind"})
	res = mongoDBAccess.find_one("testFindOneErrorCollectionXX",{"clave":"IP"})
	mongoDBAccess.drop("testFindOneErrorCollection")
	
	assert res== None 	

def test_mongoDBAccess_find_oneErrorFilter():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testFindOneErrorFilter",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find_one("testFindOneErrorFilter",{"clave":"IPFilter"})
	mongoDBAccess.drop("testFindOneErrorFilter")

	assert res== None 	

def test_mongoDBAccess_findOK():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	
	mongoDBAccess.insert("testFindOk",{"clave":"IPFind","value":0})
	mongoDBAccess.insert("testFindOk",{"clave":"IPFind","value":1})
	res = mongoDBAccess.find("testFindOk",{})
	countElements = 0
	for elementFinding in res:
		print "XXXXX"
		countElements =+1
	mongoDBAccess.drop("testFindOk")

	assert countElements > 0 

def test_mongoDBAccess_findErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/configMongoDBError.json")
	res = mongoDBAccess.find("correo",{})
	assert res== None


def test_mongoDBAccess_findErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	res = mongoDBAccess.find("correoX",{})
	countElements = 0
	for elementFinding in res:
		countElements +=1
	assert countElements == 0 

def test_mongoDBAccess_findErrorFilter():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	mongoDBAccess.insert("testFindErrorFilter",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find("testFindErrorFilter",{"xxx":"xxxx"})
	countElements = 0
	for elementFinding in res:
		countElements +=1
	mongoDBAccess.drop("testFindErrorFilter")
	
	assert countElements == 0 


def test_mongoDBAccess_update_oneOK():
	randomNumber  = random.randint(1,100)
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testUpdateOne",{"clave":"IPUpdateOne","value":0})
	resUpdate1    = mongoDBAccess.update_one("testUpdateOne",{"clave":"IPUpdateOne"},{'value':1})
	resFind1      = mongoDBAccess.find_one("testUpdateOne",{"clave":"IPUpdateOne"})
	resDelete     = mongoDBAccess.delete_one("testUpdateOne",{"clave":"IPUpdateOne"})
	mongoDBAccess.drop("testUpdateOne")
		
	assert resUpdate1 != None
	assert resFind1['value'] == 1


def test_mongoDBAccess_update_oneErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/configMongoDBError.json")
	res = mongoDBAccess.update_one("testUpdateOneErrorDB",{"clave":"IP"},{'valorX':"1234"})

	assert res== None 

def test_mongoDBAccess_update_oneErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testUpdateOneErrorCollection",{"clave":"IPUpdateOne","value":0})
	res = mongoDBAccess.update_one("testUpdateOneErrorCollectionXX",{"clave":"IP"},{'valorX':"1234"})
	mongoDBAccess.drop("testUpdateOneErrorCollection")

	assert res.modified_count== 0 	

def test_mongoDBAccess_update_oneErrorFind():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testUpdateOneErrorFind",{"clave":"IPUpdateOne","value":0})
	res = mongoDBAccess.update_one("testUpdateOneErrorFind",{"clave":"IPFind"},{'valorX':"1234"})
	mongoDBAccess.drop("testUpdateOneErrorFind")	
	
	assert res.modified_count== 0

def test_mongoDBAccess_update_manyOK():
	randomNumber  = random.randint(1,100)
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")

	mongoDBAccess.insert("testUpdateManyOk",{"clave":"IPUpdateMany","value":0})
	mongoDBAccess.insert("testUpdateManyOk",{"clave":"IPUpdateMany","value":0})

	resUpdate    = mongoDBAccess.update_many("testUpdateManyOk",{"clave":"IPUpdateMany"},{'value':1})
	resFind      = mongoDBAccess.find("testUpdateManyOk",{"clave":"IPUpdateMany"})
	countElements = 0
	for elementFinding in resFind:
		countElements +=1
		assert elementFinding['value'] == 1

	assert resUpdate.modified_count == 2
	mongoDBAccess.drop("testUpdateManyOk")	
	assert countElements == 2 



def test_mongoDBAccess_update_manyErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/configMongoDBError.json")
	res = mongoDBAccess.update_many("testUpdateManyErrorDB",{"clave":"IP"},{'valorX':"1234"})

	assert res== None 

def test_mongoDBAccess_update_manyErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert1    = mongoDBAccess.insert("testUpdateManyErrorColection",{"clave":"IPUpdateMany","value":0})
	resInsert     = mongoDBAccess.insert("testUpdateManyErrorColection",{"clave":"IPUpdateMany","value":0})
	res = mongoDBAccess.update_many("testUpdateManyErrorColectionXX",{"clave":"IPManyUpdateError"},{'valorX':"1234"})
	mongoDBAccess.drop("testUpdateManyErrorColection")	

	assert res.modified_count== 0 	

def test_mongoDBAccess_update_manyErrorFind():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert1    = mongoDBAccess.insert("testUpdateManyErrorFind",{"clave":"IPUpdateManyErrorF","value":0})
	res = mongoDBAccess.update_many("testUpdateManyErrorFind",{"clave":"IPUpdateManyErrorFXX"},{'value':1})

	mongoDBAccess.drop("testUpdateManyErrorFind")	
	
	assert res.modified_count== 0


def test_mongoDBAccess_insertOK():
	mongoDBAccess = MongoDBAccess("../test/config/configOk.json")
	resInsert     = mongoDBAccess.insert("testInsertOk",{"clave":"IPInsert"})
	resFind1      = mongoDBAccess.find_one("testInsertOk",{"clave":"IPInsert"})

	assert resInsert != None
	assert resFind1['clave'] == "IPInsert" 

	resRemove     = mongoDBAccess.delete_one("testInsertOk",{"clave":"IPInsert"})
	resFind2   = mongoDBAccess.find_one("testInsertOk",{"clave":"IPInsert"})
	mongoDBAccess.drop("testInsertOk")	

	assert resRemove.deleted_count  == 1
	assert resFind2   == None 

def test_mongoDBAccess_insertErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/configMongoDBError.json")
	res = mongoDBAccess.insert("testInsertError",{"clave":"IPInsertError"})

	assert res== None 