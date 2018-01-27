import sys
import os
sys.path.insert(0, "../pyproj")
try:
    from MongoDBAccess import MongoDBAccess
except ImportError:
    print('No Import')

def test_mongodbAcessOk():
	sys.path.insert(0, "../test")
	mongoDBAccessOk = MongoDBAccess("../test/config/testMongoDBOk.json")
	
	assert mongoDBAccessOk.status

def test_mongodbAcessError():
    sys.path.insert(0, "../test")
    mongoDBAccessError = MongoDBAccess("../test/config/testMongoDBError.json")
	
    assert not mongoDBAccessError.status 