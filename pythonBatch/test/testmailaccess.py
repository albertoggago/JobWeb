#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test mail access"""
import logging
import sys

sys.path.insert(0, "..")
try:
    from pyproj.config import Config
    from pyproj.mailaccess import MailAccess
except ImportError:
    print 'No Import'

FILE_CONFIG = "../test/config/configOk.json"
CONFIG = Config(FILE_CONFIG, logging.DEBUG)
FILE_CONFIG_ERROR = "../test/config/configMailAccessError.json"
CONFIG_ERROR = Config(FILE_CONFIG_ERROR, logging.DEBUG)


def test_mail_acess_ok():
    """test_mail_acess_ok"""
    mail_access = MailAccess(CONFIG)
    assert mail_access.status()

def test_mail_acess_ok_multi():
    """test_mailAcessOkMulti"""
    mail_access = MailAccess(CONFIG)
    assert mail_access.status()

    res_logout = mail_access.logout()
    assert res_logout
    assert not mail_access.status()

    res_login = mail_access.login()
    assert res_login
    assert mail_access.status()

def test_mail_double_logut():
    """test_mailDoubleLogut"""
    mail_access = MailAccess(CONFIG)
    assert mail_access.status()

    res_logout1 = mail_access.logout()
    res_logout2 = mail_access.logout()

    assert     res_logout1
    assert not res_logout2

def test_mail_acess_error():
    """test_mailAcessError"""
    mail_access = MailAccess(CONFIG_ERROR)

    assert not mail_access.status()

def test_list_mail_ok():
    """test_listMailOk"""
    mail_access = MailAccess(CONFIG)
    list_mails = mail_access.search_mails("Inbox")

    assert list_mails != None

def test_list_mail_error():
    """test_listMailOk"""
    mail_access = MailAccess(CONFIG_ERROR)
    list_mails = mail_access.search_mails("Inbox")

    assert list_mails is None

def test_list_mail_error_inbox():
    """test_listMailErrorInbox"""
    mail_access = MailAccess(CONFIG)
    list_mails = mail_access.search_mails("InboxXXXX")

    assert list_mails != None
