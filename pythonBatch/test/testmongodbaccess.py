"""Test mongo DB Access"""
import sys
import os
import random

sys.path.insert(0, "..")
try:
    from pyproj.mongodbaccess import MongoDBAccess
except ImportError:
    print('No Import')

def test_ok():
    """test_ok"""
    mongo_db_access_ok = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    
    assert mongo_db_access_ok.status()

def test_file_error():
    """test_file_error"""
    try :
        MongoDBAccess("../test/config/config_okxx.json", "DEBUG")
        assert False
    except IOError:
        assert True

def test_error():
    """test_error"""
    mongo_db_access_error = MongoDBAccess("../test/config/configMongoDBError.json", "DEBUG")
    
    assert not mongo_db_access_error.status()

def test_find_one_ok():
    """test_find_one_ok"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testFindOne", {"clave":"IPFind", "value":0})
    res = mongo_db_access.find_one("testFindOne", {"clave":"IPFind"})
    mongo_db_access.drop("testFindOne")
    
    assert res != None

def test_find_one_error_db():
    """test_find_one_error_db"""
    mongo_db_access = MongoDBAccess("../test/config/configMongoDBError.json", "DEBUG")
    mongo_db_access.insert("testFindone_error_db", {"clave":"IPFind", "value":0})
    res = mongo_db_access.find_one("testFindone_error_db", {"clave":"IPFind"})
    mongo_db_access.drop("testFindone_error_db")

    assert res is None

def test_find_one_error_collection():
    """test_find_one_error_collection"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testFindone_errorCollection", {"clave":"IPFind"})
    res = mongo_db_access.find_one("testFindone_errorCollectionXX", {"clave":"IP"})
    mongo_db_access.drop("testFindone_errorCollection")
    assert res is None

def test_find_one_error_filter():
    """test_find_one_error_filter"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testFindone_errorFilter", {"clave":"IPFind", "value":0})
    res = mongo_db_access.find_one("testFindone_errorFilter", {"clave":"IPFilter"})
    mongo_db_access.drop("testFindone_errorFilter")

    assert res is None

def test_find_ok():
    """test_find_ok"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testFind_ok", {"clave":"IPFind", "value":0})
    mongo_db_access.insert("testFind_ok", {"clave":"IPFind", "value":1})
    res = mongo_db_access.find("testFind_ok", {})
    count_elements = 0
    for element_finding in res:
        if element_finding != None:
            print "XXXXX"
        count_elements = +1
    mongo_db_access.drop("testFind_ok")

    assert count_elements > 0

def test_find_error_db():
    """test_find_error_db"""
    mongo_db_access = MongoDBAccess("../test/config/configMongoDBError.json", "DEBUG")
    res = mongo_db_access.find("correo", {})
    assert res is None

def test_find_error_collection():
    """test_find_error_collection"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    res = mongo_db_access.find("correoX", {})
    count_elements = 0
    for element_finding in res:
        if element_finding != None:
            count_elements += 1
    assert count_elements == 0

def test_find_error_filter():
    """test_find_error_filter"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testFindErrorFilter", {"clave":"IPFind", "value":0})
    res = mongo_db_access.find("testFindErrorFilter", {"xxx":"xxxx"})
    count_elements = 0
    for element_finding in res:
        if element_finding != None:
            count_elements += 1
    mongo_db_access.drop("testFindErrorFilter")

    assert count_elements == 0

def test_update_one_ok():
    """test_update_one_ok"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testUpdateOne", {"clave":"IPUpdateOne", "value":0})
    res_update1 = mongo_db_access.update_one("testUpdateOne", {"clave":"IPUpdateOne"}, {'value':1})
    res_find1 = mongo_db_access.find_one("testUpdateOne", {"clave":"IPUpdateOne"})
    mongo_db_access.delete_one("testUpdateOne", {"clave":"IPUpdateOne"})
    mongo_db_access.drop("testUpdateOne")

    assert res_update1 != None
    assert res_find1['value'] == 1

def test_update_one_error_db():
    """test_update_one_error_db"""
    mongo_db_access = MongoDBAccess("../test/config/configMongoDBError.json", "DEBUG")
    res = mongo_db_access.update_one("testUpdateone_error_db", {"clave":"IP"}, {'valorX':"1234"})

    assert res is None

def test_update_one_error_collect():
    """test_update_one_error_collection"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testUpdateone_errorCollection",\
                                        {"clave":"IPUpdateOne", "value":0})
    res = mongo_db_access.update_one("testUpdateone_errorCollectionXX",\
                                     {"clave":"IP"}, {'valorX':"1234"})
    mongo_db_access.drop("testUpdateone_errorCollection")

    assert res.modified_count == 0

def test_update_one_error_find():
    """test_update_one_error_find"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.insert("testUpdateone_errorFind",\
                                        {"clave":"IPUpdateOne", "value":0})
    res = mongo_db_access.update_one("testUpdateone_errorFind",\
                                     {"clave":"IPFind"}, {'valorX':"1234"})
    mongo_db_access.drop("testUpdateone_errorFind")

    assert res.modified_count == 0

def test_update_many_ok():
    """test_update_many_ok"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")

    mongo_db_access.insert("testUpdateMany_ok", {"clave":"IPUpdateMany", "value":0})
    mongo_db_access.insert("testUpdateMany_ok", {"clave":"IPUpdateMany", "value":0})

    res_update = mongo_db_access.update_many("testUpdateMany_ok",\
                                                {"clave":"IPUpdateMany"}, {'value':1})
    res_find = mongo_db_access.find("testUpdateMany_ok", {"clave":"IPUpdateMany"})
    count_elements = 0
    for element_finding in res_find:
        count_elements += 1
        assert element_finding['value'] == 1

    assert res_update.modified_count == 2
    mongo_db_access.drop("testUpdateMany_ok")
    assert count_elements == 2



def test_update_many_error_db():
    """test_update_many_error_db"""
    mongo_db_access = MongoDBAccess("../test/config/configMongoDBError.json", "DEBUG")
    res = mongo_db_access.update_many("testUpdateManyErrorDB", {"clave":"IP"}, {'valorX':"1234"})

    assert res is None

def test_update_many_error_collection():
    """test_update_many_error_collection"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    res_insert1 = mongo_db_access.insert("testUpdateManyErrorColection",\
                                         {"clave":"IPUpdateMany", "value":0})
    res_insert = mongo_db_access.insert("testUpdateManyErrorColection",\
                                        {"clave":"IPUpdateMany", "value":0})
    res = mongo_db_access.update_many("testUpdateManyErrorColectionXX",\
                                      {"clave":"IPManyUpdateError"}, {'valorX':"1234"})
    mongo_db_access.drop("testUpdateManyErrorColection")

    assert res.modified_count == 0

def test_update_many_error_find():
    """test_update_many_error_find"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    res_insert1 = mongo_db_access.insert("testUpdateManyErrorFind",\
                                         {"clave":"IPUpdateManyErrorF", "value":0})
    res = mongo_db_access.update_many("testUpdateManyErrorFind",\
                                      {"clave":"IPUpdateManyErrorFXX"}, {'value':1})
    mongo_db_access.drop("testUpdateManyErrorFind")

    assert res.modified_count == 0

def test_insert_ok():
    """test_insert_ok"""
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    res_insert = mongo_db_access.insert("testInsert_ok", {"clave":"IPInsert"})
    res_find1 = mongo_db_access.find_one("testInsert_ok", {"clave":"IPInsert"})

    assert res_insert != None
    assert res_find1['clave'] == "IPInsert"

    resRemove = mongo_db_access.delete_one("testInsert_ok", {"clave":"IPInsert"})
    res_find2 = mongo_db_access.find_one("testInsert_ok", {"clave":"IPInsert"})
    mongo_db_access.drop("testInsert_ok")

    assert resRemove.deleted_count == 1
    assert res_find2 is None

def test_insertError_db():
    """test_insertError_db"""
    mongo_db_access = MongoDBAccess("../test/config/configMongoDBError.json", "DEBUG")
    res = mongo_db_access.insert("testInsertError", {"clave":"IPInsertError"})

    assert res is None
