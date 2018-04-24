#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Test analyze web Jobs with selenium"""
import sys
import logging
sys.path.append("..")

try:
    from pyproj.config import Config
    from pyproj.resultanalyze import ResultAnalyze
except ImportError:
    print 'No Import'

FILE_CONFIG = "../test/config/configOk.json"
CONFIG = Config(FILE_CONFIG, logging.DEBUG)

def test_result_analyze_ok():
    """test_Linkedin"""
    result_analyze = ResultAnalyze(CONFIG)
    page = "page"
    control = "OK"
    url = "http://www.ok.org"
    status = "ERROR"
    variable = "fieldA"
    value = 55
    result_analyze.set_page(page)
    result_analyze.set_control(control)
    result_analyze.set_new_url(url)
    result_analyze.set_status(status)
    result_analyze.set_content_variable(variable, value)

    assert result_analyze.get_page() == page
    assert result_analyze.get_control() == control
    assert result_analyze.get_new_url() == url
    assert result_analyze.get_status() == status
    assert result_analyze.get_status() == status

def test_result_analyze_out_ok():
    """test_Linkedin"""
    result_analyze = ResultAnalyze(CONFIG)
    page = "page"
    control = "OK"
    url = "http://www.ok.org"
    status = "ERROR"
    variable = "fieldA"
    value = 55
    result_analyze.set_page(page)
    result_analyze.set_control(control)
    result_analyze.set_new_url(url)
    result_analyze.set_status(status)
    result_analyze.set_content_variable(variable, value)
    result = result_analyze.get_return_all()

    assert len(result) == 5
    assert result.get("page", "") == page
    assert result.get("control", "") == control
    assert result.get("urlOk", "") == url
    assert result.get("page", "") == page
    assert result.get("status", "") == status
    assert result.get("newCorreoUrl", "") == {variable : value}
