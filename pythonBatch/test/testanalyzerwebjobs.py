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


def test_determinate_Linkedin():
	urlLinkedin = "https://www.linkedin.com/comm/jobs/view/594182902?alertAction=3Dmarkasviewed&amp;savedSearchAuthToken=3D1%26AQHd_D1jAldtMQAAAWFylK3MksuHtX-Vkv0R8L4MIHsulkZgfHDFPPThdKagN4qX5SKs9anuOhwncTrDUrEqRpn_xAamPjP4PBFVn3viQlZ-Kwm8uVFOslO_HeqAyojkovMHY2hKl0Au7dytOLDyOpD-7NpWvpb2EXR4-LrEaEU3yW7KdTcIJFmx7E-Yf3Y7jXpYcJ961L34M37L41gQXr1B7ONDfdYx7YLdo6XVjr3MJYRG1_MoveFuJ6aosWMX4XdQqRcERYDCgbWDTU4ldVG6S8_QgH6781S1qRV2mrKY9635JE-NGw%26AVIwFRZ6FlWuciClOHUVZsMrK2cC&amp;savedSearchId=3D216056663&amp;refId=3D09245227-857f-4a7f-b692-1e12ea77d225&amp;trk=3Deml-job-alert-member-details&amp;midToken=3DAQF6sbeyCrMTqg&amp;trkEmail=3Deml-email_job_alert_single_02-null-6-null-null-1j0q1v%7Ejddp9xs9%7Ees-null-jobs%7Eview&amp;lipi=3Durn%3Ali%3Apage%3Aemail_email_job_alert_single_02%3BelCA1wQjRkm7uKIFkK%2Bc8w%3D%3D"
	correoUrl = {"url":urlLinkedin}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('status','') == True
	assert result.get('control','') == 'CORPUS'
	assert result.get('page','') == 'linkedin'
	assert result.get('realUrl','') == urlLinkedin	
	assert result["newCorreoUrl"].get("titulo","") == 'Performance Support (data) Analyst Contract Dublin'
	assert result["newCorreoUrl"].get("donde","") == 'Baile \xc3\x81tha Cliath, IE'
	assert len(result["newCorreoUrl"].get("summary","")) == 488
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime(2018, 2, 8, 7, 25, 1, 0))\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == 'Computer People Inc'
	
def test_determinate_LinkedinErrorMyPage():
	urlLinkedin = "https://www.linkedin.com/in/albertoggago/"
	correoUrl = {"url":urlLinkedin}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'
	assert result.get('page','') == 'linkedin'
	assert result.get('realUrl','') == urlLinkedin	
	assert result["newCorreoUrl"].get("titulo","") == ''
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''

def test_determinate_webPageOther():
	urlOther = "http://www.youtube.com/somethig"
	correoUrl = {"url":urlOther}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('control','') == 'OTRO'
	assert result.get('page','') == 'N/D'


def test_determinate_webPageError():
	urlError = "http://www.any.com/somethig"
	correoUrl = {"url":urlError}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('control','') == 'ERROR'
	assert result.get('page','') == 'N/D'
