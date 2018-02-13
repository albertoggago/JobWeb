import sys
import os
import random

sys.path.insert(0, "..")
try:
    from pyproj.mailaccess import MailAccess
except ImportError:
    print('No Import')

def test_mailAcessOk():
	mailAccess = MailAccess("../test/config/configOk.json","DEBUG")
	assert mailAccess.status()

def test_mailAcessOkMulti():
	mailAccess = MailAccess("../test/config/configOk.json","DEBUG")
	assert mailAccess.status()
	
	resLogout = mailAccess.logout()
	assert resLogout
	assert not mailAccess.status()

	resLogin  = mailAccess.login()
	assert resLogin
	assert mailAccess.status()

def test_mailDoubleLogut():
	mailAccess = MailAccess("../test/config/configOk.json","DEBUG")
	assert mailAccess.status()
	
	resLogout1 = mailAccess.logout()
	resLogout2  = mailAccess.logout()

	assert     resLogout1
	assert not resLogout2

def test_mailAcessError():
	mailAccess = MailAccess("../test/config/configMailAccessError.json","DEBUG")
	
	assert not mailAccess.status()
	

def test_listMailOk():
	mailAccess = MailAccess("../test/config/configOk.json","DEBUG")
	listMails =  mailAccess.search_mails("Inbox")
	
	assert listMails != None

def test_listMailError():
	mailAccess = MailAccess("../test/config/configMailAccessError.json","DEBUG")
	listMails =  mailAccess.search_mails("Inbox")
	
	assert listMails == None

def test_listMailErrorInbox():
	mailAccess = MailAccess("../test/config/configOk.json","DEBUG")
	listMails =  mailAccess.search_mails("InboxXXXX")
	
	assert listMails != None