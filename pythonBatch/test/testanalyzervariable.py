#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Text Rule Analyzer"""
import sys
import datetime
import logging

sys.path.insert(0, "..")
try:
    from pyproj.analyzervariable import AnalyzerVariable
    from pyproj.config import Config
    from pyproj.resultanalyze import ResultAnalyze
except ImportError:
    print 'No Import'

def create_result_analyze_std2():
    """create a result_analyze std """
    result_analyze2 = ResultAnalyze(CONFIG)
    result_analyze2.set_content_variable("campo1", "a")
    result_analyze2.set_content_variable("campo2", "b")
    result_analyze2.set_content_variable("campo3", "c")
    result_analyze2.set_page("xxxx")
    return result_analyze2


FILE_CONFIG3 = "../test/config/configOk.json"
CONFIG = Config(FILE_CONFIG3, logging.DEBUG)
ANALYZER_VARIABLE = AnalyzerVariable(CONFIG)

def test_split_text_void():
    """Test"""
    text_in = "text split text"
    rule = {}
    text_out = text_in
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_split_text_error_type():
    """Test"""
    text_in = "text split text"
    rule = [{"text_split": " ", "initText" : "text1"}]
    text_out = text_in
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_spltxtokwith_n():
    """Test"""
    text_in = "text1 split text2"
    rule = {"text_split": " ", "initText" : "text1"}
    text_out = "split"
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_spltxtokwith_init_text():
    """Test"""
    text_in = "text1 text2 text3"
    rule = {"text_split": " ", "n" : 2}
    text_out = "text3"
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_split_text_ok_full_first():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 0}
    text_out = "text3"
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_split_text_ok_full_midle():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 2}
    text_out = "text5"
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_split_text_ok_full_last():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 4}
    text_out = "text7"
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_split_text_out_range():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 5}
    text_out = ""
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_split_text_ok_full_txt():
    """Test"""
    text_in = "Java Web Services Developer - Berkley Recruitment Group"
    #Error in rule 'text_split' put 'text'
    rule = {'text_split': ' - ', 'initText': None, 'n': 1}
    text_out = "Berkley Recruitment Group"
    assert ANALYZER_VARIABLE.split_text(text_in, rule) == text_out

def test_decrease_date_no_text():
    """Test"""
    text_in = ""
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_no_text_err():
    """Test"""
    text_in = "en un lugar de la mancha "
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_null():
    """Test"""
    text_in = "hace dia more text to read"
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_null():
    """Test"""
    text_in = "hace mes more text to read"
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_cero():
    """Test"""
    text_in = "hace 0 d\00e0as more text to read"
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_1():
    """Test"""
    text_in = "hace 1 dia more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(days=1)
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_10():
    """Test"""
    text_in = "hace 10 dia more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(days=10)
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_1():
    """Test"""
    text_in = "hace 1 mes more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(1*365.25/12)
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_6():
    """Test"""
    text_in = "hace 6 meses more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(6*365.25/12)
    assert abs(ANALYZER_VARIABLE.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_format_text_out_void():
    """Test"""
    text_in = "texto a analizar"
    rule = {}
    text_out = text_in
    assert ANALYZER_VARIABLE.format_text_out(text_in, rule) == text_out

def test_fmttxtoutok_text():
    """Test"""
    text_in = "texto a analizar"
    rule = {"tipo":"text"}
    text_out = text_in
    assert ANALYZER_VARIABLE.format_text_out(text_in, rule) == text_out

def test_fmttxtoutok_text_void():
    """Test"""
    text_in = ""
    rule = {"tipo":"text"}
    text_out = text_in
    assert ANALYZER_VARIABLE.format_text_out(text_in, rule) == text_out

def test_fmttxtoutok_date_decre():
    """Test"""
    text_in = "hace 6 meses"
    rule = {"tipo":"fecha-dif"}
    date_out = datetime.datetime.now()- datetime.timedelta(6*365.25/12)
    assert abs(ANALYZER_VARIABLE.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)

def test_fmttxtoutok_date_decr_void():
    """Test"""
    text_in = ""
    rule = {"tipo":"fecha-dif"}
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)

def test_fmttxtoutok_date_witho_fmt():
    """Test"""
    text_in = "12/02/2017"
    rule = {"tipo":"fecha"}
    date_out = datetime.datetime(2017, 2, 12, 0, 0, 0, 0)
    assert ANALYZER_VARIABLE.format_text_out(text_in, rule) == date_out

def test_fmttxtoutok_date_guiones():
    """Test"""
    text_in = "12-02-2017"
    rule = {"tipo":"fecha", "formato":"%d-%m-%Y"}
    date_out = datetime.datetime(2017, 2, 12, 0, 0, 0, 0)
    assert ANALYZER_VARIABLE.format_text_out(text_in, rule) == date_out

def test_fmttxtoutok_date_guiones2():
    """Test"""
    text_in = "11-12-17"
    rule = {"tipo":"fecha", "formato":"%d-%m-%y"}
    date_out = datetime.datetime(2017, 12, 11, 0, 0, 0, 0)
    assert ANALYZER_VARIABLE.format_text_out(text_in, rule) == date_out

def test_fmttxtoutok_date_format():
    """Test"""
    text_in = "12/02/2017"
    rule = {"tipo":"fecha", "formato":"%d-%m-%Y"}
    date_out = datetime.datetime.now()
    assert abs(ANALYZER_VARIABLE.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)
