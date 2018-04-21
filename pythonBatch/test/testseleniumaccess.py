#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Selenium Access"""
import sys
import urllib2
import logging
from selenium.common.exceptions import WebDriverException

sys.path.insert(0, "..")
try:
    from pyproj.config import Config
    from pyproj.seleniumaccess import SeleniumAccess
except ImportError:
    print 'No Import'

FILE_CONFIG = "../test/config/configOk.json"
CONFIG = Config(FILE_CONFIG, logging.DEBUG)
FILE_CONFIG_ERROR = "../test/config/configMongoDBError.json"
CONFIG_ERROR = Config(FILE_CONFIG_ERROR, logging.DEBUG)



def test_selenium_ok():
    """test_selenium_Ok"""
    seleniumaccess = SeleniumAccess(CONFIG)
    driver = seleniumaccess.open_selenium()
    assert driver != None
    seleniumaccess.close_selenium(driver)

def test_selenium_error():
    """test_selenium_Error"""
    seleniumaccess = SeleniumAccess(CONFIG_ERROR)
    try:
        seleniumaccess.open_selenium()
        assert False
    except urllib2.URLError:
        assert True

def test_driver_ok():
    """test_Driver_Ok"""
    seleniumaccess = SeleniumAccess(CONFIG)
    driver = seleniumaccess.open_selenium()
    try:
        driver.get("http://www.google.es")
        assert True
    except WebDriverException:
        assert False
    seleniumaccess.close_selenium(driver)

def test_driver_malformed_url():
    """test_Driver_Malformed_URL"""
    seleniumaccess = SeleniumAccess(CONFIG)
    driver = seleniumaccess.open_selenium()
    try:
        driver.get("www.google.es")
        assert False
    except WebDriverException:
        assert True
    seleniumaccess.close_selenium(driver)
