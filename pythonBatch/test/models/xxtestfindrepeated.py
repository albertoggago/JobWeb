import sys
import logging

sys.path.insert(0, "..")
from pyproj.findrepeated    import FindRepeated
from pyproj.mongoDBAccess   import MongoDBAccess

def test_database_ok():
    findrepeated = FindRepeated("../test/config/configOk_real.json",logging.DEBUG)
    assert findrepeated.mongo_db_access.status()

def test_database_find_similar_not_return_himself():
    findrepeated = FindRepeated("../test/config/configOk_real.json",logging.DEBUG)
    mongoDBAccess = MongoDBAccess("../test/config/configOk_real.json",logging.DEBUG)
    element =  mongoDBAccess.find_one("correoUrl", {"control":"CORPUS", "decision":""})
    if element is None:
        assert True
    else:
        list_comparative = findrepeated.analyse_job(element,False)
        finded = False
        print list_comparative
        for comparation in list_comparative:
            if  element.get("_id","") == comparation.get("_id_similar",""):
                finded = True
        assert not finded

def test_database_read_all_jobs():
    findrepeated = FindRepeated("../test/config/configOk_real.json",logging.DEBUG)
    result = findrepeated.finding_open_jobs(True)
    print result
    assert result.get("count",-1) >= 0
    
