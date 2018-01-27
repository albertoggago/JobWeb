import sys
import os
sys.path.insert(0, "../pyproj")


try:
    from Logger import Logger
except ImportError:
    print('No Import')

#from ..pyproj.Logger import Logger 


def test_logger_test():
	sys.path.insert(0, "../test")
	os.remove("log/test.log")
	
	logger = Logger("test").get()
	logger.error("Error")
	data = open("log/test.log","r").read()
	
	assert " ERROR:log_namespace.test Error" in data 