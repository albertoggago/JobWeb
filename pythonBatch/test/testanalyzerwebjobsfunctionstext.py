"""Test ANalyzeWebJobs Functions no Selenium"""
import sys
import json

sys.path.insert(0, "..")
from pyproj.analyzerwebjobs import AnalyzerWebJobs
from pyproj.seleniumaccess import SeleniumAccess

CONFIG_TEXT2 = open("../test/config/configOk.json", "r").read()
ALL_CONFIG2 = json.loads(CONFIG_TEXT2)
CONFIG2 = ALL_CONFIG2.get("webPagesDef", None)
SELENIUM_ACCESS = SeleniumAccess(CONFIG2, "DEBUG")
ANALYZER_WEB_JOBS = AnalyzerWebJobs(CONFIG2, "DEBUG")

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
