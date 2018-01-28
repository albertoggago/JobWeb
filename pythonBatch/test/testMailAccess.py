import sys
import os
import random

sys.path.insert(0, "../pyproj")
try:
    from MailAccess import MailAccess
except ImportError:
    print('No Import')

def test_mailAcessOk():
	mailAccess = MailAccess("../test/config/mailAccess.json")
	
	assert mailAccess


def test_mailAcessOk():
	mailAccess = MailAccess("../test/config/mailAccess.json")
	
	assert mailAccess
