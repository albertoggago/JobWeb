#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" RUN all models using data of data base"""

import sys
import datetime
import logging

from pyproj.findrepeated import FindRepeated

def is_float(value):
    """ Determine if something is float"""
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    print
    print "## INFO ## inicio: {0}".format(datetime.datetime.now())
    RATIO = float(sys.argv[1]) if len(sys.argv) > 1 and is_float(sys.argv[1]) else 1.0
    DELETE = (sys.argv[2] == "True") if len(sys.argv) > 2 else False
    FILE = sys.argv[3] if len(sys.argv) > 3 else "config.json"
    print "Ratio: {0}".format(RATIO)
    print "Delete: {0}".format(DELETE)
    FIND_REPEATED = FindRepeated("config/"+FILE, logging.DEBUG, ratio_accept=RATIO)
    RESULT = FIND_REPEATED.finding_open_jobs(DELETE)
    for MAIL in RESULT.get('lines', []):
        if MAIL != []:
            print "**********************************"
            for COMPARE in MAIL:
                print COMPARE
            print "**********************************"
    print "NUMBER OF JOBS: {0}".format(RESULT.get("count", ""))
    print "## INFO ## fin: {0}".format(datetime.datetime.now())
