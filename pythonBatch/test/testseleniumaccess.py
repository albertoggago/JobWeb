import sys
import os
import json
import datetime
import pymongo
import pytest

sys.path.insert(0, "..")
from pyproj.analyzerwebjobs import AnalyzerWebJobs
from pyproj.seleniumaccess import SeleniumAccess
import urllib2

def test_selenium_Ok():
    configText = open("../test/config/configOk.json","r").read()
    allconfig  = json.loads(configText)
    config     = allconfig.get("webPagesDef",None)
    seleniumaccess = SeleniumAccess(config, "DEBUG")
    seleniumaccess.open_selenium()
    assert seleniumaccess.driver != None
    seleniumaccess.close_selenium()

def test_selenium_Error():
    configText = open("../test/config/configMongoDBError.json","r").read()
    allconfig  = json.loads(configText)
    config     = allconfig.get("webPagesDef",None)
    seleniumaccess = SeleniumAccess(config, "DEBUG")
    try:
        seleniumaccess.open_selenium()
        assert False
    except urllib2.URLError:
        assert True
    