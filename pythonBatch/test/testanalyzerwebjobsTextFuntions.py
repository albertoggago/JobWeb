import sys
import os
import json
import datetime

sys.path.insert(0, "..")
try:
    from pyproj.analyzerwebjobs import AnalyzerWebJobs
except ImportError:
    print('No Import')

configText = open("../test/config/configOk.json","r").read()
allconfig  = json.loads(configText)
config     = allconfig.get("webPagesDef",None)

#function_real_url_transform
#function_transform_url_role
#function_apply_rule_to_data
#function_review_data_ok
#function_split_text
#function_decrease_date
#function_transform_data_after_selenium
#function_format_text_out



def function_real_url_transform():
    analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
    text = "xxxx"
    rule = {"in":"x","out":"y"}
    result = "xxxx"
    assert analyzerWebJobs.function_real_url_transform(text,rule) == result