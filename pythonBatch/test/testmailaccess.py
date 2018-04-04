"""test mail access"""
import sys

sys.path.insert(0, "..")
try:
    from pyproj.mailaccess import MailAccess
except ImportError:
    print 'No Import'

def test_mail_acess_ok():
    """test_mail_acess_ok"""
    mail_access = MailAccess("../test/config/configOk.json", "DEBUG")
    assert mail_access.status()

def test_mail_acess_ok_multi():
    """test_mailAcessOkMulti"""
    mail_access = MailAccess("../test/config/configOk.json", "DEBUG")
    assert mail_access.status()

    resLogout = mail_access.logout()
    assert resLogout
    assert not mail_access.status()

    resLogin = mail_access.login()
    assert resLogin
    assert mail_access.status()

def test_mail_double_logut():
    """test_mailDoubleLogut"""
    mail_access = MailAccess("../test/config/configOk.json", "DEBUG")
    assert mail_access.status()

    resLogout1 = mail_access.logout()
    resLogout2 = mail_access.logout()

    assert     resLogout1
    assert not resLogout2

def test_mail_acess_error():
    """test_mailAcessError"""
    mail_access = MailAccess("../test/config/configMailAccessError.json", "DEBUG")

    assert not mail_access.status()

def test_list_mail_ok():
    """test_listMailOk"""
    mail_access = MailAccess("../test/config/configOk.json", "DEBUG")
    listMails = mail_access.search_mails("Inbox")

    assert listMails != None

def test_list_mail_error():
    """test_listMailOk"""
    mail_access = MailAccess("../test/config/configMailAccessError.json", "DEBUG")
    listMails = mail_access.search_mails("Inbox")

    assert listMails == None

def test_list_mail_error_inbox():
    """test_listMailErrorInbox"""
    mail_access = MailAccess("../test/config/configOk.json", "DEBUG")
    listMails = mail_access.search_mails("InboxXXXX")

    assert listMails != None
