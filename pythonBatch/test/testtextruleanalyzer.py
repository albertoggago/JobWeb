"""Test Text Rule Analyzer"""
import sys
import datetime

sys.path.insert(0, "..")
from pyproj.textruleanalyzer import TextRuleAnalyzer


TEXT_RULE_ANALYZER = TextRuleAnalyzer("DEBUG")

def test_real_url_void():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = []
    result = "http://albertoggago.es/prueba1/prueba2"
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_real_url_error_type():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = {"from":"prueba1", "to":"changedA"}
    result = ""
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_real_url_one_rule():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "to":"changedA"}]
    result = "http://albertoggago.es/changedA/prueba2"
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_real_url_one_rule_error_to():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "tox":"changedA"}]
    result = "http://albertoggago.es/ERROR-RULE/prueba2"
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_real_url_one_rule_error_fr():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"fromxxx":"prueba1", "to":"changedA"}]
    result = "http://albertoggago.es/prueba1/prueba2"
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_real_url_two_rules():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba1", "to":"changedA"}, {"from":"prueba2", "to":"changedB"}]
    result = "http://albertoggago.es/changedA/changedB"
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_real_url_two_rules_cross():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rules = [{"from":"prueba", "to":"changed"}, {"from":"chan", "to":"rechan"}]
    result = "http://albertoggago.es/rechanged1/rechanged2"
    assert TEXT_RULE_ANALYZER.real_url_transform(text, rules) == result

def test_url_role_vacia():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {}
    result = "http://albertoggago.es/prueba1/prueba2"
    assert TEXT_RULE_ANALYZER.transform_url_role(text, rule) == result

def test_url_role_error_type():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = [{"from":"prueba1", "to":"changedA"}]
    result = ""
    assert TEXT_RULE_ANALYZER.transform_url_role(text, rule) == result

def test_url_role():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"from":"prueba1", "to":"changedA"}
    result = "http://albertoggago.es/changedA/prueba2"
    assert TEXT_RULE_ANALYZER.transform_url_role(text, rule) == result

def test_url_role_error_to():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"from":"prueba1", "tox":"changedA"}
    result = "http://albertoggago.es/ERROR-RULE/prueba2"
    assert TEXT_RULE_ANALYZER.transform_url_role(text, rule) == result

def test_url_role_error_from():
    """Test"""
    text = "http://albertoggago.es/prueba1/prueba2"
    rule = {"fromxxx":"prueba1", "to":"changedA"}
    result = "http://albertoggago.es/prueba1/prueba2"
    assert TEXT_RULE_ANALYZER.transform_url_role(text, rule) == result


def test_aplrulaftsel_void():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    rule = {}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_err_ty():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    rule = [{"in":"campo1", "out":"campo1", "valueInxxx":"a", "action":"SPACES"}]
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"a"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_error_act():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "actionxxx":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_error_in():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"inxxx":"campo1", "out":"campo1", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_error_out():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "outxxxx":"campo1", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "OUT-ERROR":""}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_error_val_in():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueInxxx":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_error_val_out():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOutX":"hello"}
    result = {"newCorreoUrl":{"campo1":"ERROR-VALUE-OUT", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_error_val_oth():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY-ANOTHER"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_ok_b_same_var():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_ok_b_oth_var():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo2", "valueIn":"a", "action":"SPACES"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":""}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_ok_same_var():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOut":"hello"}
    result = {"newCorreoUrl":{"campo1":"hello", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_ok_cp_oth_var():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo2", "valueIn":"a", "action":"COPY", "valueOut":"hello"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"hello"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_ok_cp_oth_sva():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"b", "campo2":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_aplrulaftsel_ok_cp_othothv():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"b"}, "other":"xxxx"}
    assert TEXT_RULE_ANALYZER.apply_rule_after_sel(text, rule) == result

def test_proaftgetvar_void_rule():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = []
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    TEXT_RULE_ANALYZER.process_after_get_variables(text, rule)
    assert text == result

def test_proaftgetvar_err_type_rule():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
            "another":"campo2"}
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    TEXT_RULE_ANALYZER.process_after_get_variables(text, rule)
    assert text == result

def test_proaftgetvar_one_rule():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = [{"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
             "another":"campo2"}]
    result = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"b"}, "other":"xxxx"}
    TEXT_RULE_ANALYZER.process_after_get_variables(text, rule)
    assert text == result

def test_proaftgetvar_two_rules():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = [{"in":"campo1", "out":"campo3", "valueIn":"a", "action":"COPY-ANOTHER",\
             "another":"campo2"}, \
            {"in":"campo1", "out":"campo1", "valueIn":"a", "action":"COPY", "valueOut":"hello"}]
    result = {"newCorreoUrl":{"campo1":"hello", "campo2":"b", "campo3":"b"}, "other":"xxxx"}
    TEXT_RULE_ANALYZER.process_after_get_variables(text, rule)
    assert text == result

def test_revdatok_void():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = []
    assert TEXT_RULE_ANALYZER.review_data_ok(text, rule)

def test_revdatok_error_type():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = {"campo1", "campo2", "campo3"}
    assert not TEXT_RULE_ANALYZER.review_data_ok(text, rule)

def test_revdatok_ok_full():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo1", "campo2", "campo3"]
    assert TEXT_RULE_ANALYZER.review_data_ok(text, rule)

def test_revdatok_ok_partial():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo1", "campo3"]
    assert TEXT_RULE_ANALYZER.review_data_ok(text, rule)

def test_revdatok_error_partial():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo1", "campo5"]
    assert not TEXT_RULE_ANALYZER.review_data_ok(text, rule)

def test_revdatok_error_full():
    """Test"""
    text = {"newCorreoUrl":{"campo1":"a", "campo2":"b", "campo3":"c"}, "other":"xxxx"}
    rule = ["campo5"]
    assert not TEXT_RULE_ANALYZER.review_data_ok(text, rule)

def test_split_text_void():
    """Test"""
    text_in = "text split text"
    rule = {}
    text_out = text_in
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_split_text_error_type():
    """Test"""
    text_in = "text split text"
    rule = [{"text_split": " ", "initText" : "text1"}]
    text_out = text_in
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_spltxtokwith_n():
    """Test"""
    text_in = "text1 split text2"
    rule = {"text_split": " ", "initText" : "text1"}
    text_out = "split"
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_spltxtokwith_init_text():
    """Test"""
    text_in = "text1 text2 text3"
    rule = {"text_split": " ", "n" : 2}
    text_out = "text3"
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_split_text_ok_full_first():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 0}
    text_out = "text3"
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_split_text_ok_full_midle():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 2}
    text_out = "text5"
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_split_text_ok_full_last():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 4}
    text_out = "text7"
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_split_text_out_range():
    """Test"""
    text_in = "text1 text2 text3 text4 text5 text6 text7"
    rule = {"text_split": " ", "initText" : "text2", "n" : 5}
    text_out = ""
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_split_text_ok_full_txt():
    """Test"""
    text_in = "Java Web Services Developer - Berkley Recruitment Group"
    #Error in rule 'text_split' put 'text'
    rule = {'text_split': ' - ', 'initText': None, 'n': 1}
    text_out = "Berkley Recruitment Group"
    assert TEXT_RULE_ANALYZER.split_text(text_in, rule) == text_out

def test_decrease_date_no_text():
    """Test"""
    text_in = ""
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_no_text_err():
    """Test"""
    text_in = "en un lugar de la mancha "
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_null():
    """Test"""
    text_in = "hace dia more text to read"
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_null():
    """Test"""
    text_in = "hace mes more text to read"
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_cero():
    """Test"""
    text_in = "hace 0 d\00e0as more text to read"
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_1():
    """Test"""
    text_in = "hace 1 dia more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(days=1)
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_day_10():
    """Test"""
    text_in = "hace 10 dia more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(days=10)
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_1():
    """Test"""
    text_in = "hace 1 mes more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(1*365.25/12)
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_decrease_date_month_6():
    """Test"""
    text_in = "hace 6 meses more text to read"
    date_out = datetime.datetime.now()- datetime.timedelta(6*365.25/12)
    assert abs(TEXT_RULE_ANALYZER.decrease_date(text_in) - date_out) < datetime.timedelta(days=1)

def test_format_text_out_void():
    """Test"""
    text_in = "texto a analizar"
    rule = {}
    text_out = text_in
    assert TEXT_RULE_ANALYZER.format_text_out(text_in, rule) == text_out

def test_fmttxtoutok_text():
    """Test"""
    text_in = "texto a analizar"
    rule = {"tipo":"text"}
    text_out = text_in
    assert TEXT_RULE_ANALYZER.format_text_out(text_in, rule) == text_out

def test_fmttxtoutok_text_void():
    """Test"""
    text_in = ""
    rule = {"tipo":"text"}
    text_out = text_in
    assert TEXT_RULE_ANALYZER.format_text_out(text_in, rule) == text_out

def test_fmttxtoutok_date_decre():
    """Test"""
    text_in = "hace 6 meses"
    rule = {"tipo":"fecha-dif"}
    date_out = datetime.datetime.now()- datetime.timedelta(6*365.25/12)
    assert abs(TEXT_RULE_ANALYZER.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)

def test_fmttxtoutok_date_decr_void():
    """Test"""
    text_in = ""
    rule = {"tipo":"fecha-dif"}
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)

def test_fmttxtoutok_date_witho_fmt():
    """Test"""
    text_in = "12/02/2017"
    rule = {"tipo":"fecha"}
    date_out = datetime.datetime(2017, 2, 12, 0, 0, 0, 0)
    assert TEXT_RULE_ANALYZER.format_text_out(text_in, rule) == date_out

def test_fmttxtoutok_date_guiones():
    """Test"""
    text_in = "12-02-2017"
    rule = {"tipo":"fecha", "formato":"%d-%m-%Y"}
    date_out = datetime.datetime(2017, 2, 12, 0, 0, 0, 0)
    assert TEXT_RULE_ANALYZER.format_text_out(text_in, rule) == date_out

def test_fmttxtoutok_date_guiones2():
    """Test"""
    text_in = "11-12-17"
    rule = {"tipo":"fecha", "formato":"%d-%m-%y"}
    date_out = datetime.datetime(2017, 12, 11, 0, 0, 0, 0)
    assert TEXT_RULE_ANALYZER.format_text_out(text_in, rule) == date_out

def test_fmttxtoutok_date_format():
    """Test"""
    text_in = "12/02/2017"
    rule = {"tipo":"fecha", "formato":"%d-%m-%Y"}
    date_out = datetime.datetime.now()
    assert abs(TEXT_RULE_ANALYZER.format_text_out(text_in, rule) - date_out)\
                          < datetime.timedelta(days=1)
