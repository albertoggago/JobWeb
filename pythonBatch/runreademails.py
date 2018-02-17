#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Execution for sistem of read and analyze mails """

import sys
import datetime
import logging

from pyproj.readandanalyse import ReadAndAnalyse

if __name__ == '__main__':
    PARAM_VISIBLE = True if len(sys.argv) > 1 else False
    print "## INFO ## inicio: {0}".format(datetime.datetime.now())
    READ_AND_ANALYSE = ReadAndAnalyse("config/config.json", PARAM_VISIBLE, logging.INFO)
    MAILS_READ = READ_AND_ANALYSE.finding_mails()
    print "## INFO ## Mails Read: {0}".format(MAILS_READ)
    URLS_READS = READ_AND_ANALYSE.finding_urls()
    print "## INFO ## Urls Read: {0}".format(URLS_READS)
    SCRAP_READS = READ_AND_ANALYSE.scrap_urls()
    print "## INFO ## Urls Scrap: {0}".format(SCRAP_READS)
    print "## INFO ## fin: {0}".format(datetime.datetime.now())

