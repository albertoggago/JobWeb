#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Execution for sistem of read and analyze mails """

import datetime
import logging
import sys

from pyproj.readandanalyse import ReadAndAnalyse

if __name__ == '__main__':
    print "## INFO ## inicio: {0}".format(datetime.datetime.now())
    FILE = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    print "## INFO ## FILE CONFIG: {0}".format(FILE)

    READ_AND_ANALYSE = ReadAndAnalyse("config/"+FILE, logging.DEBUG)
    MAILS_READ = READ_AND_ANALYSE.finding_mails()
    print "## INFO ## Mails Read: {0}".format(MAILS_READ)
    URLS_READS = READ_AND_ANALYSE.finding_urls()
    print "## INFO ## Urls Read: {0}".format(URLS_READS)
    SCRAP_READS = READ_AND_ANALYSE.scrap_urls()
    print "## INFO ## Urls Scrap: {0}".format(SCRAP_READS)

    # print "## INFO ## Ratio: {0}".format(RATIO)
    # print "## INFO ## Delete: {0}".format(DELETE)
    # FIND_REPEATED = FindRepeated("config/config_real.json", logging.DEBUG, ratio_accept=RATIO)
    # RESULT = FIND_REPEATED.finding_open_jobs(DELETE)
    # for MAIL in RESULT.get('lines', []):
    #     if MAIL != []:
    #         print "**********************************"
    #         for COMPARE in MAIL:
    #             print COMPARE
    #         print "**********************************"
    # print "NUMBER OF JOBS: {0}".format(RESULT.get("count", ""))


    print "## INFO ## fin: {0}".format(datetime.datetime.now())

