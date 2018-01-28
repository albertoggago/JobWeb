import sys
import os
import random

sys.path.insert(0, "../pyproj")
try:
    from MailAccess import MailAccess
except ImportError:
    print('No Import')

def test_mailAcessOk():
	mailAccess = MailAccess("../test/config/mailAccessOk.json")
	
	assert mailAccess.status


def test_mailAcessOkMulti():
	mailAccess = MailAccess("../test/config/mailAccessOk.json")
	assert mailAccess.status
	
	resLogout = mailAccess.logout()
	resLogin  = mailAccess.login()

	assert resLogout
	assert resLogin
	assert mailAccess.status

def test_mailAcessError():
	mailAccess = MailAccess("../test/config/mailAccessError.json")
	
	assert not mailAccess.status


def test_listMailOk():
	mailAccess = MailAccess("../test/config/mailAccessOk.json")
	listMails =  mailAccess.searchMails("Inbox")
	
	assert listMails != None

def test_listMailError():
	mailAccess = MailAccess("../test/config/mailAccessError.json")
	listMails =  mailAccess.searchMails("Inbox")
	
	assert listMails == None

def test_listMailErrorInbox():
	mailAccess = MailAccess("../test/config/mailAccessOk.json")
	listMails =  mailAccess.searchMails("InboxXXXX")
	
	assert listMails != None


