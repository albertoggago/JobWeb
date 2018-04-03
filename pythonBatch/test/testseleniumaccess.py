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
from selenium.common.exceptions import WebDriverException

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

def test_selenium_close():
    configText = open("../test/config/configOk.json","r").read()
    allconfig  = json.loads(configText)
    config     = allconfig.get("webPagesDef",None)
    seleniumaccess = SeleniumAccess(config, "DEBUG")
    seleniumaccess.open_selenium()
    seleniumaccess.close_selenium()
    assert seleniumaccess.driver == None

def test_selenium_Access_Driver_Ok():
    configText = open("../test/config/configOk.json","r").read()
    allconfig  = json.loads(configText)
    config     = allconfig.get("webPagesDef",None)
    seleniumaccess = SeleniumAccess(config, "DEBUG")
    seleniumaccess.open_selenium()
    try :
        seleniumaccess.driver.get("http://www.google.es")
        assert True
    except WebDriverException:
        assert False
    seleniumaccess.close_selenium()

def test_selenium_Access_Driver_Malformed_URL():
    configText = open("../test/config/configOk.json","r").read()
    allconfig  = json.loads(configText)
    config     = allconfig.get("webPagesDef",None)
    seleniumaccess = SeleniumAccess(config, "DEBUG")
    seleniumaccess.open_selenium()
    try :
        seleniumaccess.driver.get("www.google.es")
        assert False
    except WebDriverException:
        assert True
    seleniumaccess.close_selenium()

       