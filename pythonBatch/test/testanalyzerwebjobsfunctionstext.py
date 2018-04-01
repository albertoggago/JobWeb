import sys
import os
import json
import datetime
import pymongo
import pytest

sys.path.insert(0, "..")
from pyproj.analyzerwebjobs import AnalyzerWebJobs

configText = open("../test/config/configOk.json","r").read()
allconfig  = json.loads(configText)
config     = allconfig.get("webPagesDef",None)
time_out   = 20
analyzerWebJobs = AnalyzerWebJobs(config,"DEBUG")

def test_determinate_web_error():
    url = "https://www.none.com"
    result = {}
    analyzerWebJobs.determinate_web(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "ERROR"
        
def test_determinate_web_linkedin():
    url = "https://www.linkedin.com"
    result = {}
    analyzerWebJobs.determinate_web(result, url)
    assert result["page"] == "linkedin"
    assert result["control"] == "REVIEW"

def test_determinate_web_irishjobs():
    url = "https://www.irishjobs.ie"
    result = {}
    analyzerWebJobs.determinate_web(result, url)
    assert result["page"] == "irishjobs"
    assert result["control"] == "REVIEW"

def test_determinate_web_other():
    url = "https://www.saongroup.ie"
    result = {}
    analyzerWebJobs.determinate_web(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "OTRO"

def test_determinate_other_error():
    url = "https://www.none.com"
    result = {}
    analyzerWebJobs.determinate_other(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "ERROR"
        
def test_determinate_other_other():
    url = "https://www.saongroup.ie"
    result = {}
    analyzerWebJobs.determinate_other(result, url)
    assert result["page"] == "N/D"
    assert result["control"] == "OTRO"
        

