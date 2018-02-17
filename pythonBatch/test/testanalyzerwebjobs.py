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

@pytest.mark.timeout(time_out)
def test_determinate_Linkedin():
	data = {}
	data["a"] = "b"
	urlLinkedin = "https://www.linkedin.com/comm/jobs/view/594182902?alertAction=3Dmarkasviewed&amp;savedSearchAuthToken=3D1%26AQHd_D1jAldtMQAAAWFylK3MksuHtX-Vkv0R8L4MIHsulkZgfHDFPPThdKagN4qX5SKs9anuOhwncTrDUrEqRpn_xAamPjP4PBFVn3viQlZ-Kwm8uVFOslO_HeqAyojkovMHY2hKl0Au7dytOLDyOpD-7NpWvpb2EXR4-LrEaEU3yW7KdTcIJFmx7E-Yf3Y7jXpYcJ961L34M37L41gQXr1B7ONDfdYx7YLdo6XVjr3MJYRG1_MoveFuJ6aosWMX4XdQqRcERYDCgbWDTU4ldVG6S8_QgH6781S1qRV2mrKY9635JE-NGw%26AVIwFRZ6FlWuciClOHUVZsMrK2cC&amp;savedSearchId=3D216056663&amp;refId=3D09245227-857f-4a7f-b692-1e12ea77d225&amp;trk=3Deml-job-alert-member-details&amp;midToken=3DAQF6sbeyCrMTqg&amp;trkEmail=3Deml-email_job_alert_single_02-null-6-null-null-1j0q1v%7Ejddp9xs9%7Ees-null-jobs%7Eview&amp;lipi=3Durn%3Ali%3Apage%3Aemail_email_job_alert_single_02%3BelCA1wQjRkm7uKIFkK%2Bc8w%3D%3D"
	correoUrl = {"url":urlLinkedin}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
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
	
@pytest.mark.timeout(time_out)
def test_determinate_recruitireland():
	url_recruitireland = "https://www.recruitireland.com/job/?JobID=3D15323238&utm_source=3Djobalerts&utm_medium=3Demail&utm_campaign=3DJobAlerts"
	url_real_recruitireland = "https://www.recruitireland.com/job/?JobID=15323238&utm_source=jobalerts&utm_medium=email&utm_campaign=JobAlerts"
	correoUrl = {"url":url_recruitireland}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'recruitireland'
	assert result.get('realUrl','') == url_real_recruitireland	
	assert result["newCorreoUrl"].get("titulo","") == 'BUSINESS ANALYST'
	assert result["newCorreoUrl"].get("donde","") == 'DUBLIN SOUTH'
	assert len(result["newCorreoUrl"].get("summary","")) == 1086
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime(2018, 2, 15, 12, 0, 0, 0))\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == 'CPL'
	assert result.get('status','') == True
	assert result.get('control','') == 'CORPUS'
	assert result["newCorreoUrl"].get("salary","") == 'NEGOTIABLE'
	assert result["newCorreoUrl"].get("jobType","") == 'CONTRACT'

@pytest.mark.timeout(time_out)
def test_determinate_irishjobs():
	url_irishjobs = "https://www.irishjobs.ie/Jobs/Senior-Javascript-UI-Developer-8134189.aspx?adobeid=jajob&jacid=525770-02-2018&jst=1_tJ8AOY57h0AzRlf6ylCQld&utm_source=JobAlert&utm_medium=clicks&utm_campaign=Jbe+Applications"
	correoUrl = {"url":url_irishjobs}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'irishjobs'
	assert result.get('realUrl','') == url_irishjobs	
	assert result["newCorreoUrl"].get("titulo","") == 'SENIOR JAVASCRIPT UI DEVELOPER'
	assert result["newCorreoUrl"].get("donde","") == 'Galway / Galway city'
	assert len(result["newCorreoUrl"].get("summary","")) == 913
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime(2018, 2, 13, 12, 0, 0, 0))\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == 'STELFOX'
	assert result.get('status','') == True
	assert result.get('control','') == 'CORPUS'
	assert result["newCorreoUrl"].get("salary","") == 'Negotiable'
	assert result["newCorreoUrl"].get("jobType","") == 'Permanent full-time'

@pytest.mark.timeout(time_out)
def test_determinate_jobs_ie():
	url_jobsie = "https://www.jobs.ie/ApplyForJob.aspx?Id=1683365&jst=3Dm1XZicalx_wFcls3wvyk6DKe&utm_source=3Djobalerts&utm_medium=3Demail&utm_campaign=3DJob%2BAlerts&cid=jajob&jacid=3DJob_Alert_1263851-02-2018"
	url_real_jobsie = "https://www.jobs.ie/ApplyForJob.aspx?Id=1683365&jst=m1XZicalx_wFcls3wvyk6DKe&utm_source=jobalerts&utm_medium=email&utm_campaign=Job%2BAlerts&cid=jajob&jacid=Job_Alert_1263851-02-2018"
	correoUrl = {"url":url_jobsie}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'jobs.ie'
	assert result.get('realUrl','') == url_real_jobsie	
	assert result["newCorreoUrl"].get("titulo","") == 'Audio Visual/ VC Technician'
	assert result["newCorreoUrl"].get("donde","") == 'Grand Canal Square, Grand Canal Dock, Dublin 2'
	assert len(result["newCorreoUrl"].get("summary","")) == 2873
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime(2018, 2, 16, 12, 0, 0, 0))\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == 'Milestone Technologies'
	assert result.get('status','') == True
	assert result.get('control','') == 'CORPUS'
	assert result["newCorreoUrl"].get("salary","") == 'Negotiable'
	assert result["newCorreoUrl"].get("jobType","") == 'Permanent | Full Time'

@pytest.mark.timeout(time_out)
def test_determinate_jobs_monster():
	url_monster = "https://job-openings.monster.ie/Java-Web-Services-Developer-Dublin-Dublin-IE-Berkley-Recruitment-Group/11/193191188?aid=149460911&uid=3D100010B3583BE8DD89155F4EF0CDEA2CA719AFD497202D5CB85DC317A6886350151F6A1B6505A0D849734DE5E772C04AC54FD7BB2D9DBFF8A286CADD157C04BF851EB6447FE228EF7451516C10D2F9829BE457&WT.mc_n=JSAHG10&jvs=3De,ar,l,1"
	url_real_monster = "https://job-openings.monster.ie/Java-Web-Services-Developer-Dublin-Dublin-IE-Berkley-Recruitment-Group/11/193191188?aid=149460911&uid=100010B3583BE8DD89155F4EF0CDEA2CA719AFD497202D5CB85DC317A6886350151F6A1B6505A0D849734DE5E772C04AC54FD7BB2D9DBFF8A286CADD157C04BF851EB6447FE228EF7451516C10D2F9829BE457&WT.mc_n=JSAHG10&jvs=e,ar,l,1"
	correoUrl = {"url":url_monster}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'monster.ie'
	assert result.get('realUrl','') == url_real_monster	
	assert result["newCorreoUrl"].get("titulo","") == 'Java Web Services Developer'
	assert result["newCorreoUrl"].get("donde","") == 'Dublin, Dublin'
	assert len(result["newCorreoUrl"].get("summary","")) == 983
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime(2018, 2, 9, 12, 0, 0, 0))\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == 'Berkley Recruitment Group'
	assert result.get('status','') == True
	assert result.get('control','') == 'CORPUS'

@pytest.mark.timeout(time_out)
def test_determinate_LinkedinErrorMyPage():
	urlLinkedin = "https://www.linkedin.com/in/albertoggago/"
	correoUrl = {"url":urlLinkedin}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
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
	assert result["newCorreoUrl"].get("company","") == '<NO DEFINIDA>'

@pytest.mark.timeout(time_out)
def test_determinate_recruitireland_error_no_exits():
	url_recruitireland = "http://www.recruitireland.com/job/?JobID=3D153224144525&amp;utm_source=3Djobalerts&amp;utm_medium=3Demail&amp;utm_campaign=3DJobAlerts"
	url_real_recruitireland = "http://www.recruitireland.com/job/?JobID=153224144525&amp;utm_source=jobalerts&amp;utm_medium=email&amp;utm_campaign=JobAlerts"
	correoUrl = {"url":url_recruitireland}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'recruitireland'
	assert result.get('realUrl','') == url_real_recruitireland	
	assert result["newCorreoUrl"].get("titulo","") == ''
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'
	
@pytest.mark.timeout(time_out)
def test_determinate_recruitireland_error_retired():
	url_recruitireland = "https://www.recruitireland.com/job/?JobID=3D15315978&utm_source=3Djobalerts&utm_medium=3Demail&utm_campaign=3DJobAlerts"
	url_real_recruitireland = "https://www.recruitireland.com/job/?JobID=15315978&utm_source=jobalerts&utm_medium=email&utm_campaign=JobAlerts"
	correoUrl = {"url":url_recruitireland}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'recruitireland'
	assert result.get('realUrl','') == url_real_recruitireland	
	assert result["newCorreoUrl"].get("titulo","") == ''
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'

@pytest.mark.timeout(time_out)
def test_determinate_irishjobs_error_retired():
	url_irishjobs = "https://www.irishjobs.ie/Jobs/Senior-FrontEnd-Engineer-8112985.aspx?adobeid=jajob&jacid=525770-12-2017&jst=z6kbolHKteomUWY3Lf73W1sP&utm_source=JobAlert&utm_medium=clicks&utm_campaign=Jbe+Applications"
	correoUrl = {"url":url_irishjobs}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'irishjobs'
	assert result.get('realUrl','') == url_irishjobs	
	assert result["newCorreoUrl"].get("titulo","") == 'SENIOR FRONTEND ENGINEER'
	assert result["newCorreoUrl"].get("donde","") == 'Kildare / Wicklow / Dublin'
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime(2018, 1, 19, 12, 0, 0, 0))\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == 'VIASAT'
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'
	assert result["newCorreoUrl"].get("salary","") == 'Negotiable'
	assert result["newCorreoUrl"].get("jobType","") == 'Permanent full-time'


@pytest.mark.timeout(time_out)
def test_determinate_irishjobs_error_error():
	url_irishjobs = "https://www.irishjobs.ie/Jobs/Senior-Fron-Engineer-8112985.aspx?adobeid=jajob&jacid=525770-12-2017&jst=z6kbolHKteomUWY3Lf73W1sP&utm_source=JobAlert&utm_medium=clicks&utm_campaign=Jbe+Applications"
	correoUrl = {"url":url_irishjobs}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'irishjobs'
	assert result.get('realUrl','') == url_irishjobs	
	assert result["newCorreoUrl"].get("titulo","") == ''
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'

@pytest.mark.timeout(time_out)
def test_determinate_jobsie_error_retired():
	url_jobsie = "https://www.jobs.ie/ApplyForJob.aspx?Id=3D1671149&jst=3DtasndzhbOQL7jKXJPAJaFsxg&utm_source=3Djobalerts&utm_medium=email&utm_campaign=3DJob%2BAlerts&cid=jajob&jacid=Job_Alert_1263851-12-2017"
	url_real_jobsie = "https://www.jobs.ie/ApplyForJob.aspx?Id=1671149&jst=tasndzhbOQL7jKXJPAJaFsxg&utm_source=jobalerts&utm_medium=email&utm_campaign=Job%2BAlerts&cid=jajob&jacid=Job_Alert_1263851-12-2017"
	correoUrl = {"url":url_jobsie}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'jobs.ie'
	assert result.get('realUrl','') == url_real_jobsie	
	assert result["newCorreoUrl"].get("titulo","") == ''
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'
	
@pytest.mark.timeout(time_out)
def test_determinate_jobsie_error_noexist():
	url_jobsie = "https://www.jobs.ie/ApplyForJob.aspx?Id=16744441149&jst=tasndzhbOQL7jKXJPAJaFsxg&utm_source=jobalerts&utm_medium=email&utm_campaign=Job%2BAlerts&cid=jajob&jacid=Job_Alert_1263851-12-2017"
	url_real_jobsie = "https://www.jobs.ie/ApplyForJob.aspx?Id=16744441149&jst=tasndzhbOQL7jKXJPAJaFsxg&utm_source=jobalerts&utm_medium=email&utm_campaign=Job%2BAlerts&cid=jajob&jacid=Job_Alert_1263851-12-2017"
	correoUrl = {"url":url_jobsie}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'jobs.ie'
	assert result.get('realUrl','') == url_real_jobsie	
	assert result["newCorreoUrl"].get("titulo","") == ''
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'

@pytest.mark.timeout(time_out)
def test_determinate_monster_error_retired():
	url_monster = "https://job-openings.monster.ie/v2/job/expired?JobID=3D187199556&aid=3D149460911&uid=10001060440B2C63BD4967960768D8002AEE74CE25A02E161703EED6BF313CD07DB4318118C6CC54F323D68238085E096699F8B4416FC152EF08A624EEA0BCF498995DAB945D7B2B51BB0EE6F29BE5E5A3A9D0&WT.mc_n=3DJSAHG10&jvs=e,ar,l,1"
	url_real_monster = "https://job-openings.monster.ie/v2/job/expired?JobID=187199556&aid=149460911&uid=10001060440B2C63BD4967960768D8002AEE74CE25A02E161703EED6BF313CD07DB4318118C6CC54F323D68238085E096699F8B4416FC152EF08A624EEA0BCF498995DAB945D7B2B51BB0EE6F29BE5E5A3A9D0&WT.mc_n=JSAHG10&jvs=e,ar,l,1"
	correoUrl = {"url":url_monster}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'monster.ie'
	assert result.get('realUrl','') == url_real_monster
	assert result["newCorreoUrl"].get("titulo","") == 'Employers'
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'
	
@pytest.mark.timeout(time_out)
def test_determinate_monster_error_noexist():
	url_monster = "https://job-openings.monster.ie/v2/job/expired?JobID=3D187199444556&aid=3D149460911&uid=10001060440B2C63BD4967960768D8002AEE74CE25A02E161703EED6BF313CD07DB4318118C6CC54F323D68238085E096699F8B4416FC152EF08A624EEA0BCF498995DAB945D7B2B51BB0EE6F29BE5E5A3A9D0&WT.mc_n=3DJSAHG10&jvs=e,ar,l,1"
	url_real_monster = "https://job-openings.monster.ie/v2/job/expired?JobID=187199444556&aid=149460911&uid=10001060440B2C63BD4967960768D8002AEE74CE25A02E161703EED6BF313CD07DB4318118C6CC54F323D68238085E096699F8B4416FC152EF08A624EEA0BCF498995DAB945D7B2B51BB0EE6F29BE5E5A3A9D0&WT.mc_n=JSAHG10&jvs=e,ar,l,1"
	correoUrl = {"url":url_monster}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('page','') == 'monster.ie'
	assert result.get('realUrl','') == url_real_monster	
	assert result["newCorreoUrl"].get("titulo","") == 'Employers'
	assert result["newCorreoUrl"].get("donde","") == ''
	assert result["newCorreoUrl"].get("summary","") == ''
	assert abs(result["newCorreoUrl"].get("fecha","") - datetime.datetime.now())\
	       < datetime.timedelta(days=1)
	assert result["newCorreoUrl"].get("company","") == ''
	assert result.get('status','') == False
	assert result.get('control','') == 'SEARCH'
	
@pytest.mark.timeout(time_out)
def test_determinate_webPageOther():
	urlOther = "http://www.youtube.com/somethig"
	correoUrl = {"url":urlOther}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('control','') == 'OTRO'
	assert result.get('page','') == 'N/D'


@pytest.mark.timeout(time_out)
def test_determinate_webPageError():
	urlError = "http://www.any.com/somethig"
	correoUrl = {"url":urlError}	
	analyzerWebJobs = AnalyzerWebJobs(config,False,"DEBUG")
	analyzerWebJobs.open_selenium()
	result = analyzerWebJobs.analyze(correoUrl)
	analyzerWebJobs.close_selenium()
	assert result.get('control','') == 'ERROR'
	assert result.get('page','') == 'N/D'
