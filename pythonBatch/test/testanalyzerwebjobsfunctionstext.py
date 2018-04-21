#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test ANalyzeWebJobs Functions no Selenium"""
import sys
import logging

sys.path.append("..")

try:
    from pyproj.seleniumaccess import SeleniumAccess
    from pyproj.analyzerwebjobs import AnalyzerWebJobs
    from pyproj.config import Config
except ImportError:
    print 'No Import'

FILE_CONFIG2 = "../test/config/configOk.json"
CONFIG = Config(FILE_CONFIG2, logging.DEBUG)
CONFIG_PARAM = CONFIG.get_config_param()

SELENIUM_ACCESS = SeleniumAccess(CONFIG)
ANALYZER_WEB_JOBS = AnalyzerWebJobs(CONFIG)

def test_determinate_web_error():
    """test_determinate_web_error"""
    url = "https://www.none.com"
    result = {}
    ANALYZER_WEB_JOBS.determinate_web(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "ERROR"

def test_determinate_web_linkedin():
    """test_determinate_web_linkedin"""
    url = "https://www.linkedin.com"
    result = {}
    ANALYZER_WEB_JOBS.determinate_web(result, url)
    assert result["page"] == "linkedin"
    assert result["control"] == "REVIEW"

def test_determinate_web_irishjobs():
    """test_determinate_web_irishjobs"""
    url = "https://www.irishjobs.ie"
    result = {}
    ANALYZER_WEB_JOBS.determinate_web(result, url)
    assert result["page"] == "irishjobs"
    assert result["control"] == "REVIEW"

def test_determinate_web_other():
    """test_determinate_web_other"""
    url = "https://www.saongroup.ie"
    result = {}
    ANALYZER_WEB_JOBS.determinate_web(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "OTRO"

def test_determinate_other_error():
    """test_determinate_other_error"""
    url = "https://www.none.com"
    result = {}
    ANALYZER_WEB_JOBS.determinate_other_web(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "ERROR"

def test_determinate_other_other():
    """test_determinate_other_other"""
    url = "https://www.saongroup.ie"
    result = {}
    ANALYZER_WEB_JOBS.determinate_other_web(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "OTRO"
