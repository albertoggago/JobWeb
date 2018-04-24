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
    web_rules = ANALYZER_WEB_JOBS.return_rules(url)
    assert ANALYZER_WEB_JOBS.get_page(web_rules) == "N/D"
    assert ANALYZER_WEB_JOBS.get_control(web_rules, url) == "ERROR"
    assert ANALYZER_WEB_JOBS.get_new_url(web_rules, url) == url

def test_determinate_web_linkedin():
    """test_determinate_web_linkedin"""
    url = "https://www.linkedin.com"
    web_rules = ANALYZER_WEB_JOBS.return_rules(url)
    assert ANALYZER_WEB_JOBS.get_page(web_rules) == "linkedin"
    assert ANALYZER_WEB_JOBS.get_control(web_rules, url) == "REVIEW"
    assert ANALYZER_WEB_JOBS.get_new_url(web_rules, url) == url

def test_determinate_web_irishjobs():
    """test_determinate_web_irishjobs"""
    url = "https://www.irishjobs.ie"
    web_rules = ANALYZER_WEB_JOBS.return_rules(url)
    assert ANALYZER_WEB_JOBS.get_page(web_rules) == "irishjobs"
    assert ANALYZER_WEB_JOBS.get_control(web_rules, url) == "REVIEW"
    assert ANALYZER_WEB_JOBS.get_new_url(web_rules, url) == url

def test_determinate_web_other():
    """test_determinate_web_other"""
    url = "https://www.saongroup.ie"
    web_rules = ANALYZER_WEB_JOBS.return_rules(url)
    assert ANALYZER_WEB_JOBS.get_page(web_rules) == "N/D"
    assert ANALYZER_WEB_JOBS.get_control(web_rules, url) == "OTRO"
    assert ANALYZER_WEB_JOBS.get_new_url(web_rules, url) == url

def test_determinate_other_error():
    """test_determinate_other_error"""
    url = "https://www.none.com"
    web_rules = ANALYZER_WEB_JOBS.return_rules(url)
    assert ANALYZER_WEB_JOBS.get_page(web_rules) == "N/D"
    assert ANALYZER_WEB_JOBS.get_control(web_rules, url) == "ERROR"
    assert ANALYZER_WEB_JOBS.get_new_url(web_rules, url) == url

def test_determinate_other_other():
    """test_determinate_other_other"""
    url = "https://www.saongroup.ie"
    web_rules = ANALYZER_WEB_JOBS.return_rules(url)
    assert ANALYZER_WEB_JOBS.get_page(web_rules) == "N/D"
    assert ANALYZER_WEB_JOBS.get_control(web_rules, url) == "OTRO"
    assert ANALYZER_WEB_JOBS.get_new_url(web_rules, url) == url
