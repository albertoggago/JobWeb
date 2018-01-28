import sys
import os
import random

sys.path.insert(0, "../pyproj")
try:
    from MongoDBAccess import MongoDBAccess
except ImportError:
    print('No Import')

def test_mongodbAcessOk():
	mongoDBAccessOk = MongoDBAccess("../test/config/testMongoDBOk.json")
	
	assert mongoDBAccessOk.status

def test_mongodbAcessError():
    mongoDBAccessError = MongoDBAccess("../test/config/testMongoDBError.json")
	
    assert not mongoDBAccessError.status

def test_mongoDBAccess_find_oneOK():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find_one("variosTest",{"clave":"IPFind"})
	resDelete     = mongoDBAccess.delete_one("variosTest",{"clave":"IPFind"})
	
	assert res!= None 

def test_mongoDBAccess_find_oneErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBError.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find_one("variosTest",{"clave":"IPFind"})
	resDelete     = mongoDBAccess.delete_one("variosTest",{"clave":"IPFind"})
	
	assert res== None 

def test_mongoDBAccess_find_oneErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPFind"})
	res = mongoDBAccess.find_one("variosXX",{"clave":"IP"})
	resDelete     = mongoDBAccess.delete_one("variosTest",{"clave":"IPFind"})
	
	assert res== None 	

def test_mongoDBAccess_find_oneErrorFilter():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPFind","value":0})
	res = mongoDBAccess.find_one("variosTest",{"clave":"IPFilter"})
	resDelete     = mongoDBAccess.delete_one("variosTest",{"clave":"IPFind"})
	
	assert res== None 	

def test_mongoDBAccess_findOK():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	res = mongoDBAccess.find("correo",{})

	countElements = 0
	for elementFinding in res:
		countElements =+1
	assert countElements > 0 

def test_mongoDBAccess_findErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBError.json")
	res = mongoDBAccess.find("correo",{})

	assert res== None 

def test_mongoDBAccess_findErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	res = mongoDBAccess.find("correoX",{})

	countElements = 0
	for elementFinding in res:
		countElements +=1
	assert countElements == 0 

def test_mongoDBAccess_findErrorFilter():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	res = mongoDBAccess.find("correo",{"xxx":"xxxx"})

	countElements = 0
	for elementFinding in res:
		countElements +=1
	assert countElements == 0 


def test_mongoDBAccess_update_oneOK():
	randomNumber  = random.randint(1,100)
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPUpdateOne","value":0})
	resUpdate1    = mongoDBAccess.update_one("variosTest",{"clave":"IPUpdateOne"},{'value':1})
	resFind1      = mongoDBAccess.find_one("variosTest",{"clave":"IPUpdateOne"})
	resDelete     = mongoDBAccess.delete_one("variosTest",{"clave":"IPUpdateOne"})
		
	assert resUpdate1 != None
	assert resFind1['value'] == 1


def test_mongoDBAccess_update_oneErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBError.json")
	res = mongoDBAccess.update_one("variosTest",{"clave":"IP"},{'valorX':"1234"})

	assert res== None 

def test_mongoDBAccess_update_oneErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	res = mongoDBAccess.update_one("variosXX",{"clave":"IP"},{'valorX':"1234"})
	
	assert res.modified_count== 0 	

def test_mongoDBAccess_update_oneErrorFind():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPUpdateOne","value":0})
	res = mongoDBAccess.update_one("variosTest",{"clave":"IPFind"},{'valorX':"1234"})
	resDelete     = mongoDBAccess.delete_one("variosTest",{"clave":"IPUpdateOne"})
	
	assert res.modified_count== 0

def test_mongoDBAccess_update_manyOK():
	randomNumber  = random.randint(1,100)
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")

	resInsert1    = mongoDBAccess.insert("variosTest",{"clave":"IPUpdateMany","value":0})
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPUpdateMany","value":0})

	resUpdate1    = mongoDBAccess.update_many("variosTest",{"clave":"IPUpdateMany"},{'value':1})
	resFind1      = mongoDBAccess.find("variosTest",{"clave":"IPUpdateMany"})

	assert resUpdate1 != None
	countElements1 = 0
	for elementFinding in resFind1:
		countElements1 +=1
		assert elementFinding['value'] == 1
	assert countElements1 == 2 
	 

	resDeleted1 = mongoDBAccess.delete_one("variosTest",{"clave":"IPUpdateMany"})
	resDeleted2 = mongoDBAccess.delete_one("variosTest",{"clave":"IPUpdateMany"})
	resFind2   = mongoDBAccess.find("variosTest",{"clave":"IPUpdateMany"})

	assert resDeleted1.deleted_count == 1
	assert resDeleted2.deleted_count == 1
	countElements2 = 0
	for elementFinding in resFind1:
		countElements2 +=1
	assert countElements2 == 0 


def test_mongoDBAccess_update_manyErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBError.json")
	res = mongoDBAccess.update_many("variosTest",{"clave":"IP"},{'valorX':"1234"})

	assert res== None 

def test_mongoDBAccess_update_manyErrorCollection():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	res = mongoDBAccess.update_many("variosTest",{"clave":"IPManyUpdateError"},{'valorX':"1234"})
	
	assert res.modified_count== 0 	

def test_mongoDBAccess_update_manyErrorFind():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert1    = mongoDBAccess.insert("variosTest",{"clave":"IPUpdateManyErrorF","value":0})
	res = mongoDBAccess.update_many("variosTest",{"clave":"IPUpdateManyErrorFXX"},{'value':1})
	resDelete1    = mongoDBAccess.delete_one("variosTest",{"clave":"IPUpdateManyErrorF"})
	
	assert res.modified_count== 0




def test_mongoDBAccess_insertOK():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBOk.json")
	resInsert     = mongoDBAccess.insert("variosTest",{"clave":"IPInsert"})
	resFind1      = mongoDBAccess.find_one("variosTest",{"clave":"IPInsert"})

	assert resInsert != None
	assert resFind1['clave'] == "IPInsert" 

	resRemove     = mongoDBAccess.delete_one("variosTest",{"clave":"IPInsert"})
	resFind2   = mongoDBAccess.find_one("variosTest",{"clave":"IPInsert"})

	assert resRemove.deleted_count  == 1
	assert resFind2   == None 

def test_mongoDBAccess_insertErrorDB():
	mongoDBAccess = MongoDBAccess("../test/config/testMongoDBError.json")
	res = mongoDBAccess.insert("variosTest",{"clave":"IPInsertError"})

	assert res== None 

