#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test readanalyse"""
import sys
import logging

sys.path.insert(0, "..")
try:
    from pyproj.config import Config
    from pyproj.readandanalyse import ReadAndAnalyse
    from pyproj.mongodbaccess import MongoDBAccess
except ImportError:
    print 'No Import'

FILE_CONFIG_OK = "../test/config/configOk.json"
CONFIG_OK = Config(FILE_CONFIG_OK, logging.DEBUG)
FILE_CONFIG_ERROR = "../test/config/configOkXXXXXXX.json"
CONFIG_ERROR = Config(FILE_CONFIG_ERROR, logging.DEBUG)
FILE_CONFIG_ERROR_MAIL = "../test/config/configMailAccessError.json"
CONFIG_ERROR_MAIL = Config(FILE_CONFIG_ERROR_MAIL, logging.DEBUG)
FILE_CONFIG_ERROR_MONGODB = "../test/config/configMongoDBError.json"
CONFIG_ERROR_MONGODB = Config(FILE_CONFIG_ERROR_MONGODB, logging.DEBUG)

def test_ra_init_error_fichero():
    """test_ra_init_error_fichero"""
    read_and_analyse = ReadAndAnalyse(CONFIG_ERROR)
    assert not read_and_analyse.get_mongo_db_access_status()
    assert not read_and_analyse.get_mail_access_status()

def test_ra_init_correct():
    """test_ra_init_correct"""
    read_and_analyse = ReadAndAnalyse(CONFIG_OK)
    assert read_and_analyse.get_mongo_db_access_status()
    assert read_and_analyse.get_mail_access_status()

def test_ra_init_error_mongo():
    """test_ra_init_ErrorMongo"""
    read_and_analyse = ReadAndAnalyse(CONFIG_ERROR_MONGODB)
    assert not read_and_analyse.get_mongo_db_access_status()
    assert read_and_analyse.get_mail_access_status()

def test_ra_init_error_mail():
    """test_ra_init_ErrorMail"""
    read_and_analyse = ReadAndAnalyse(CONFIG_ERROR_MAIL)
    assert read_and_analyse.get_mongo_db_access_status()
    assert not read_and_analyse.get_mail_access_status()

def test_ra_finding_mails():
    """test_ra_findingMails"""
    read_and_analyse = ReadAndAnalyse(CONFIG_OK)
    mongo_db_access = MongoDBAccess(CONFIG_OK)
    mongo_db_access.delete_many("correo", {})
    amount = read_and_analyse.finding_mails()
    #Depends of the emails in the mail test
    assert amount == 6

def test_ra_finding_urls():
    """test_ra_findingUrls"""
    read_and_analyse = ReadAndAnalyse(CONFIG_OK)
    mongo_db_access = MongoDBAccess(CONFIG_OK)
    mongo_db_access.delete_many("correo", {})
    mongo_db_access.delete_many("correoUrl", {})
    read_and_analyse.finding_mails()
    amount = read_and_analyse.finding_urls()
    #Depends of the information inside of mails
    assert amount == 131

    dones = mongo_db_access.find("correo", {"control":"DONE"})
    amount_dones = 0
    for done in dones:
        if done != None:
            amount_dones += 1
    #Depends of the information inside of mails
    assert amount_dones == 6

    correos_urls = mongo_db_access.find("correoUrl", {})
    amount_correos_urls = 0
    for correo_url in correos_urls:
        if correo_url != None:
            amount_correos_urls += 1
    #Depends of the information inside of mails
    assert amount_correos_urls == 131

def test_ra_scrap_urls():
    """test_ra_scrapUrls"""
    read_and_analyse = ReadAndAnalyse(CONFIG_OK)
    mongo_db_access = MongoDBAccess(CONFIG_OK)
    mongo_db_access.delete_many("correo", {})
    mongo_db_access.delete_many("correoUrl", {})
    read_and_analyse.finding_mails()
    read_and_analyse.finding_urls()
    amount = read_and_analyse.scrap_urls(10)
    #Depends of the information inside of mails
    assert amount == {"ERROR":10}
