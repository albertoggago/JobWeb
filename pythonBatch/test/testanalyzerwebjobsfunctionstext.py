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
    from pyproj.resultanalyze import ResultAnalyze
except ImportError:
    print 'No Import'

FILE_CONFIG2 = "../test/config/configOk.json"
CONFIG = Config(FILE_CONFIG2, logging.DEBUG)
CONFIG_PARAM = CONFIG.get_config_param()

SELENIUM_ACCESS = SeleniumAccess(CONFIG)
ANALYZER_WEB_JOBS = AnalyzerWebJobs(CONFIG)

def create_result_analyze_std():
    """create a result_analyze std """
    result_analyze = ResultAnalyze(CONFIG)
    result_analyze.set_content_variable("campo1", "a")
    result_analyze.set_content_variable("campo2", "b")
    result_analyze.set_content_variable("campo3", "c")
    result_analyze.set_page("xxxx")
    return result_analyze


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

def test_real_url_void():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = []
    result = "http://albertoggago.es/prueba1/prueba2"
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_real_url_error_type():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = {"from":"prueba1", "to":"changedA"}
    result = ""
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_real_url_one_rule():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "to":"changedA"}]
    result = "http://albertoggago.es/changedA/prueba2"
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_real_url_one_rule_error_to():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "tox":"changedA"}]
    result = "http://albertoggago.es/ERROR-RULE/prueba2"
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_real_url_one_rule_error_fr():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"fromxxx":"prueba1", "to":"changedA"}]
    result = "http://albertoggago.es/prueba1/prueba2"
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_real_url_two_rules():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "to":"changedA"}, {"from":"prueba2", "to":"changedB"}]
    result = "http://albertoggago.es/changedA/changedB"
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_real_url_two_rules_cross():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba", "to":"changed"}, {"from":"chan", "to":"rechan"}]
    result = "http://albertoggago.es/rechanged1/rechanged2"
    assert ANALYZER_WEB_JOBS.real_url_transform(text, rules) == result

def test_url_role_vacia():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {}
    result = "http://albertoggago.es/prueba1/prueba2"
    assert ANALYZER_WEB_JOBS.transform_url_role(text, rule) == result

def test_url_role_error_type():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = [{"from":"prueba1", "to":"changedA"}]
    result = ""
    assert ANALYZER_WEB_JOBS.transform_url_role(text, rule) == result

def test_url_role():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"from":"prueba1", "to":"changedA"}
    result = "http://albertoggago.es/changedA/prueba2"
    assert ANALYZER_WEB_JOBS.transform_url_role(text, rule) == result

def test_url_role_error_to():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"from":"prueba1", "tox":"changedA"}
    result = "http://albertoggago.es/ERROR-RULE/prueba2"
    assert ANALYZER_WEB_JOBS.transform_url_role(text, rule) == result

def test_url_role_error_from():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"fromxxx":"prueba1", "to":"changedA"}
    result = "http://albertoggago.es/prueba1/prueba2"
    assert ANALYZER_WEB_JOBS.transform_url_role(text, rule) == result

def test_aplrulaftsel_void():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_err_ty():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = [{"in":"campo1", "out":"campo1", "valueInxxx":"a", "action":"SPACES"}]
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_error_act():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "actionxxx":"SPACES"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_error_in():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"inxxx":"campo1", "out":"campo1", "valueIn":"a", "action":"SPACES"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_error_out():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "outxxxx":"campo1", "valueIn":"a", "action":"SPACES"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_content_variable("OUT-ERROR") == ""
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_error_val_in():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueInxxx":"a", "action":"SPACES"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_error_val_out():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOutX":"hello"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "ERROR-VALUE-OUT"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_error_val_oth():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY-ANOTHER"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_ok_b_same_var():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"SPACES"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == ""
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_ok_b_oth_var():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo2", "valueIn":"a", "action":"SPACES"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == ""
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_ok_same_var():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOut":"hello"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "hello"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_ok_cp_oth_var():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo2", "valueIn":"a", "action":"COPY", "valueOut":"hello"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "hello"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_ok_cp_oth_sva():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "b"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_aplrulaftsel_ok_cp_othothv():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    ANALYZER_WEB_JOBS.apply_rule_after_sel(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_content_variable("campo3") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_proaftgetvar_void_rule():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = []
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    ANALYZER_WEB_JOBS.process_after_get_variables(text, rule)
    assert text == result

def test_proaftgetvar_err_type_rule():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    ANALYZER_WEB_JOBS.process_after_get_variables(text, rule)
    assert text == result

def test_proaftgetvar_one_rule():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = [{"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
             "another":"campo2"}]
    ANALYZER_WEB_JOBS.process_after_get_variables(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "a"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_content_variable("campo3") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_proaftgetvar_two_rules():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = [{"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
             "another":"campo2"}, \
            {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOut":"hello"}]
    ANALYZER_WEB_JOBS.process_after_get_variables(result_analyze, rule)
    assert result_analyze.get_content_variable("campo1") == "hello"
    assert result_analyze.get_content_variable("campo2") == "b"
    assert result_analyze.get_content_variable("campo3") == "b"
    assert result_analyze.get_page() == "xxxx"

def test_revdatok_void():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = []
    assert ANALYZER_WEB_JOBS.review_data_ok(result_analyze, rule)

def test_revdatok_error_type():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = {"campo1", "campo2", "campo3"}
    assert not ANALYZER_WEB_JOBS.review_data_ok(result_analyze, rule)

def test_revdatok_ok_full():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = ["campo1", "campo2", "campo3"]
    assert ANALYZER_WEB_JOBS.review_data_ok(result_analyze, rule)

def test_revdatok_ok_partial():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = ["campo1", "campo3"]
    assert ANALYZER_WEB_JOBS.review_data_ok(result_analyze, rule)

def test_revdatok_error_partial():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = ["campo1", "campo5"]
    assert not ANALYZER_WEB_JOBS.review_data_ok(result_analyze, rule)

def test_revdatok_error_full():
    """Test"""
    result_analyze = create_result_analyze_std()
    rule = ["campo5"]
    assert not ANALYZER_WEB_JOBS.review_data_ok(result_analyze, rule)

