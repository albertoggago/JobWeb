#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test class"""
import sys
import os
import json
import datetime

sys.path.insert(0, "..")
from pyproj.textanalyzer import TextAnalyzer

configText = open("../test/config/configOk.json", "r").read()
allconfig = json.loads(configText)
config = allconfig.get("webPagesDef", None)

text_analyzer = TextAnalyzer("DEBUG")

def test_real_url_transform_void():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = []
    result = "http://albertoggago.es/prueba1/prueba2"
    assert text_analyzer.real_url_transform(text, rules) == result

def test_real_url_transform_error_type():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = {"from":"prueba1", "to":"changedA"}
    result = ""
    assert text_analyzer.real_url_transform(text, rules) == result

def test_real_url_transform_one_rule():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "to":"changedA"}]
    result = "http://albertoggago.es/changedA/prueba2"
    assert text_analyzer.real_url_transform(text, rules) == result

def test_real_url_transform_one_rule_error_to():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "tox":"changedA"}]
    result = "http://albertoggago.es/ERROR-RULE/prueba2"
    assert text_analyzer.real_url_transform(text, rules) == result

def test_real_url_transform_one_rule_error_from():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"fromxxx":"prueba1", "to":"changedA"}]
    result = "http://albertoggago.es/prueba1/prueba2"
    assert text_analyzer.real_url_transform(text, rules) == result

def test_real_url_transform_two_rules():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "to":"changedA"}, {"from":"prueba2", "to":"changedB"}]
    result = "http://albertoggago.es/changedA/changedB"
    assert text_analyzer.real_url_transform(text, rules) == result

def test_real_url_transform_two_rules_cross():
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba", "to":"changed"}, {"from":"chan", "to":"rechan"}]
    result = "http://albertoggago.es/rechanged1/rechanged2"
    assert text_analyzer.real_url_transform(text, rules) == result

def test_transform_url_role_vacia():
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {}
    result = "http://albertoggago.es/prueba1/prueba2"
    assert text_analyzer.transform_url_role(text, rule) == result

def test_transform_url_role_error_type():
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = [{"from":"prueba1", "to":"changedA"}]
    result = ""
    assert text_analyzer.transform_url_role(text, rule) == result

def test_transform_url_role():
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"from":"prueba1", "to":"changedA"}
    result = "http://albertoggago.es/changedA/prueba2"
    assert text_analyzer.transform_url_role(text, rule) == result

def test_transform_url_role_error_to():
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"from":"prueba1", "tox":"changedA"}
    result = "http://albertoggago.es/ERROR-RULE/prueba2"
    assert text_analyzer.transform_url_role(text, rule) == result

def test_transform_url_role_error_from():
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"fromxxx":"prueba1", "to":"changedA"}
    result = "http://albertoggago.es/prueba1/prueba2"
    assert text_analyzer.transform_url_role(text, rule) == result


def test_apply_rule_after_sel_void():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    rule = {}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_error_type():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    rule = [{"in":"campo1", "out":"campo1", "valueInxxx":"a", "action":"SPACES"}]
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_Error_action():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "actionxxx":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_Error_in():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"inxxx":"campo1", "out":"campo1", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_Error_out():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "outxxxx":"campo1", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "OUT-ERROR":""}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_Error_value_in():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueInxxx":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_Error_value_out():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOutX":"hello"}
    result = {"newCorreoUrl":{"campo1":"ERROR-VALUE-OUT", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_Error_value_another():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY-ANOTHER"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_ok_spaces_same_variable():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_ok_spaces_other_variable():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo2", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":""}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_ok_copy_same_variable():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOut":"hello"}
    result = {"newCorreoUrl":{"campo1":"hello", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_ok_copy_other_variable():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo2", "valueIn":"a", "action":"COPY", "valueOut":"hello"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"hello"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_ok_copy_another_same_variable():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"b", "campo2":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_apply_rule_after_sel_ok_copy_another_other_variable():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"b"}, "other":"xxxx"}
    assert text_analyzer.apply_rule_after_sel(text, rule) == result

def test_data_after_selenium_void_rule():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = []
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    assert text_analyzer.data_after_selenium(text, rule) == result

def test_data_after_selenium_error_type_rule():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    assert text_analyzer.data_after_selenium(text, rule) == result

def test_data_after_selenium_one_rule():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = [{"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
             "another":"campo2"}]
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"b"}, "other":"xxxx"}
    assert text_analyzer.data_after_selenium(text, rule) == result

def test_data_after_selenium_two_rules():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = [{"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
             "another":"campo2"}, \
            {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOut":"hello"}]
    result = {"newCorreoUrl":{"campo1":"hello", "campo2":"b", "campo3":"b"}, "other":"xxxx"}
    assert text_analyzer.data_after_selenium(text, rule) == result

def test_review_data_ok_void():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = []
    assert text_analyzer.review_data_ok(text, rule)

def test_review_data_ok_error_type():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"campo1", "campo2", "campo3"}
    assert not text_analyzer.review_data_ok(text, rule)

def test_review_data_ok_ok_full():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo1", "campo2", "campo3"]
    assert text_analyzer.review_data_ok(text, rule)

def test_review_data_ok_ok_partial():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo1", "campo3"]
    assert text_analyzer.review_data_ok(text, rule)

def test_review_data_ok_error_partial():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo1", "campo5"]
    assert not text_analyzer.review_data_ok(text, rule)

def test_review_data_ok_error_full():
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo5"]
    assert not text_analyzer.review_data_ok(text, rule)

def test_split_text_void():
    text_in = "text split text"
    rule = {}
    text_out = text_in
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_error_type():
    text_in = "text split text"
    rule = [{"text_split": " ", "initText" : "text1"}]
    text_out = text_in
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_ok_without_n():
    text_in = "text1 split text2"
    rule = {"text_split": " ", "initText" : "text1"}
    text_out = "split"
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_ok_without_init_text():
    text_in = "text1 text2 text3"
    rule = {"text_split": " ", "n" : 2}
    text_out = "text3"
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_ok_full_first():
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 0}
    text_out = "text3"
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_ok_full_midle():
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 2}
    text_out = "text5"
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_ok_full_last():
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 4}
    text_out = "text7"
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_out_range():
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 5}
    text_out = ""
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_split_text_ok_full_berkley_recruiteland():
    text_in = "Java Web Services Developer - Berkley Recruitment Group"
    #Error in rule 'text_split' put 'text'
    rule = {'text_split': ' - ', 'initText': None, 'n': 1}
    text_out = "Berkley Recruitment Group"
    assert text_analyzer.split_text(text_in, rule) == text_out

def test_decrease_date_no_text():
    text_in = ""
    date_out = datetime.datetime.now()
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_no_text_error():
    text_in = "en un lugar de la mancha "
    date_out = datetime.datetime.now()
    diff = 0
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_null():
    text_in = "hace dia more text to read"
    date_out = datetime.datetime.now()
    diff = 0
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_null():
    text_in = "hace mes more text to read"
    date_out = datetime.datetime.now()
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_cero():
    text_in = "hace 0 d\00e0as more text to read"
    date_out = datetime.datetime.now()
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_1():
    text_in = "hace 1 dia more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(days=1)
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_10():
    text_in = "hace 10 dia more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(days=10)
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_1():
    text_in = "hace 1 mes more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(1*365.25/12)
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_6():
    text_in = "hace 6 meses more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(6*365.25/12)
    assert abs(text_analyzer.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_format_text_out_void():
    text_in = "texto a analizar"
    rule = {}
    text_out = text_in
    assert text_analyzer.format_text_out(text_in, rule) == text_out

def test_format_text_out_ok_text():
    text_in = "texto a analizar"
    rule = {"tipo":"text"}
    text_out = text_in
    assert text_analyzer.format_text_out(text_in, rule) == text_out

def test_format_text_out_ok_text_void():
    text_in = ""
    rule = {"tipo":"text"}
    text_out = text_in
    assert text_analyzer.format_text_out(text_in, rule) == text_out

def test_format_text_out_ok_dateDecreasing():
    text_in = "hace 6 meses"
    rule = {"tipo":"fecha-dif"}
    date_out = datetime.datetime.now()- datetime.timedelta(6*365.25/12)
    assert abs(text_analyzer.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)

def test_format_text_out_ok_dateDecreasing_void():
    text_in = ""
    rule = {"tipo":"fecha-dif"}
    date_out = datetime.datetime.now()
    assert abs(text_analyzer.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)

def test_format_text_out_ok_date_without_format():
    text_in = "12/02/2017"
    rule = {"tipo":"fecha"}
    date_out = datetime.datetime(2017, 2, 12, 0, 0, 0, 0)
    assert text_analyzer.format_text_out(text_in, rule) == date_out

def test_format_text_out_ok_date_guiones():
    text_in = "12-02-2017"
    rule = {"tipo":"fecha", "formato":"%d-%m-%Y"}
    date_out = datetime.datetime(2017, 2, 12, 0, 0, 0, 0)
    assert text_analyzer.format_text_out(text_in, rule) == date_out

def test_format_text_out_ok_date_guiones():
    text_in = "11-12-17"
    rule = {"tipo":"fecha", "formato":"%d-%m-%y"}
    date_out = datetime.datetime(2017, 12, 11, 0, 0, 0, 0)
    assert text_analyzer.format_text_out(text_in, rule) == date_out

def test_format_text_out_ok_date_format():
    text_in = "12/02/2017"
    rule = {"tipo":"fecha", "formato":"%d-%m-%Y"}
    date_out = datetime.datetime.now()
    assert abs(text_analyzer.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)
