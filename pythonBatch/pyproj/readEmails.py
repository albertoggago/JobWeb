#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

from ReadAndAnalyse import ReadAndAnalyse

if __name__ == '__main__':
	param_visible = True if len(sys.argv)>1 else False
	print "## INFO ## inicio: {0}".format(datetime.datetime.now())
	readAndAnalyse = ReadAndAnalyse("config/config.json",param_visible,"INFO")
	mailsReads     =  readAndAnalyse.finding_mails()
	print "## INFO ## Mails Read: {0}".format(mailsReads)
	urlsReads      =  readAndAnalyse.finding_urls()
	print "## INFO ## Urls Read: {0}".format(urlsReads)
	scrapReads     = readAndAnalyse.scrap_urls()
	print "## INFO ## Urls Scrap: {0}".format(scrapReads)
	print "## INFO ## fin: {0}".format(datetime.datetime.now())

