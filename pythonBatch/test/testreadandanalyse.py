#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test readanalyse"""
import sys
import logging

sys.path.insert(0, "..")
try:
    from pyproj.readandanalyse import ReadAndAnalyse
    from pyproj.mongodbaccess import MongoDBAccess
except ImportError:
    print 'No Import'

def test_init_error_fichero():
    """test_init_error_fichero"""
    read_and_analyse = ReadAndAnalyse("../test/config/configOkXXXX.json", logging.ERROR)
    assert not read_and_analyse.mongo_db_access.status()
    assert not read_and_analyse.mail_access.status()

def test_init_correct():
    """test_init_correct"""
    read_and_analyse = ReadAndAnalyse("../test/config/configOk.json", logging.ERROR)
    assert read_and_analyse.mongo_db_access.status()
    assert read_and_analyse.mail_access.status()

def test_init_error_mongo():
    """test_init_ErrorMongo"""
    read_and_analyse = ReadAndAnalyse("../test/config/configMongoDBError.json", logging.ERROR)
    assert not read_and_analyse.mongo_db_access.status()
    assert read_and_analyse.mail_access.status()

def test_init_error_mail():
    """test_init_ErrorMail"""
    read_and_analyse = ReadAndAnalyse("../test/config/configMailAccessError.json", logging.ERROR)
    assert read_and_analyse.mongo_db_access.status()
    assert not read_and_analyse.mail_access.status()

def test_finding_mails():
    """test_findingMails"""
    read_and_analyse = ReadAndAnalyse("../test/config/configOk.json", logging.ERROR)
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "DEBUG")
    mongo_db_access.delete_many("correo", {})
    amount = read_and_analyse.finding_mails()
    #Depends of the emails in the mail test
    assert amount == 6

def test_finding_urls():
    """test_findingUrls"""
    read_and_analyse = ReadAndAnalyse("../test/config/configOk.json", logging.ERROR)
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", "WARNING")
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

def test_scrap_urls():
    """test_scrapUrls"""
    read_and_analyse = ReadAndAnalyse("../test/config/configOk.json", logging.ERROR)
    mongo_db_access = MongoDBAccess("../test/config/configOk.json", logging.ERROR)
    mongo_db_access.delete_many("correo", {})
    mongo_db_access.delete_many("correoUrl", {})
    read_and_analyse.finding_mails()
    read_and_analyse.finding_urls()
    amount = read_and_analyse.scrap_urls(10)
    #Depends of the information inside of mails
    assert amount == {"ERROR":10}
