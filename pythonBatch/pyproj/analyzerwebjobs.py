#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique AalyzeWebJobs """
import datetime

#import string
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

#own classes
from pyproj.logger import Logger


class AnalyzerWebJobs(object):
    """Analyze information of each scrapint of a job and contruct information for save"""

    config = None
    logger = None
    driver = None

    def __init__(self, config, visible, level_log):
        self.logger = Logger(self.__class__.__name__, level_log).get()
        self.config = config
        if not visible:
            display = Display(visible=0, size=(1024, 768))
            display.start()
        self.driver = webdriver.Chrome()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.ERROR)

    def analyze(self, correo_url):
        """module analyze get url and prepare scraping"""
        result = {}
        result_with_page = self.determinate_web(result, correo_url["url"])
        if result_with_page.get("control", "") == "REVIEW":
            self.driver.get(result_with_page.get("realUrl", ""))
            result_with_data = self.find_data(result_with_page)
            return result_with_data
        else:
            result_with_page["status"] = False
            return result_with_page

    def close_selenium(self):
        """close driver for scraping"""
        self.driver.close()

    def determinate_web(self, result_imput, web_url):
        """ determinate web where working to set configuration to analize of this web"""
        result_web = result_imput
        self.logger.info("determinate Web")
        for web in self.config.get("pages", {}):
            if web.get("ruleFind") in web_url:
                self.logger.info("Locate web: "+web.get("name", "ERROR"))
                result_web["page"] = web.get("name", "ERROR")
                result_web["control"] = "REVIEW"
                result_web["realUrl"] =\
                       self.real_url_transform(web_url, web.get("ruleTransformUrl", {}))

        if result_web.get("page", None) is None:
            result_web = self.determinate_other(result_web, web_url)
        return result_web

    def real_url_transform(self, web_intro, rules):
        """ transform url using rules to eliminate wrong data"""
        self.logger.info("Rules Transform URL: ")
        self.logger.info(rules)
        web_output = web_intro
        for rule_url_transform in rules:
            web_output = self.transform_ulr_rule(web_output, rule_url_transform)
        return web_output

    def transform_ulr_rule(self, url, rule):
        """ Transform url with one rule"""
        self.logger.info("Rule Transform URL: ")
        self.logger.info(rule)
        return url.replace(rule.get("from", ""), rule.get("to", ""))

    def determinate_other(self, result_imput, web_url):
        """it has got a list of web to ignore and not compute"""
        result_other = result_imput
        for web in self.config.get("otherPages", {}):
            if web in web_url:
                self.logger.info("Locate web OTHER: "+web)
                result_other["page"] = "N/D"
                result_other["control"] = "OTRO"
        if result_other.get("page", None) is None:
            self.logger.info("Locate web ERROR: ")
            result_other["page"] = "N/D"
            result_other["control"] = "ERROR"
        return result_other

    def find_data(self, result_imput):
        """Find Information using rules of web"""
        self.logger.info("Find Data")
        data_after_selenium = result_imput
        rules_page = {}
        pages = self.config["pages"]
        for page in pages:
            if page["name"] == result_imput["page"]:
                self.logger.info("Locate page get rules: ")
                self.logger.debug(page)
                rules_page = page

        necesary_variables = rules_page.get("necesaryVariables", "")
        data_after_selenium["newCorreoUrl"] = {}
        for variable in necesary_variables:
            result_variable = self.process_variable(variable,\
                                      rules_page.get("rulesTransformUrl", {}).get(variable, {}))
            data_after_selenium["newCorreoUrl"][variable] = result_variable

        #determinate rules after search
        result_with_global_rules = self.transform_data_after_selenium(data_after_selenium,\
            rules_page.get("rulestransformFinal"))
        result_with_global_rules["status"] = \
            self.review_data_ok(result_with_global_rules, rules_page.get("rulesOkFinfing"))
        if result_with_global_rules["status"]:
            result_with_global_rules["control"] = "CORPUS"
        else:
            result_with_global_rules["control"] = "SEARCH"
        return result_with_global_rules

    def transform_data_after_selenium(self, data_imput, rules_after_selenium):
        """ With rules transform output for modify data """
        data_output = data_imput
        self.logger.info("Rules Transform after Selenium")
        self.logger.info(rules_after_selenium)
        for rule in rules_after_selenium:
            self.apply_rule_to_data(data_output, rule)
        return data_imput

    def apply_rule_to_data(self, data_imput, rule):
        """ get rule and aply to output"""
        data_output = data_imput
        self.logger.debug("Rule Unique Transform after Selenium")
        self.logger.debug(data_output["newCorreoUrl"].get(rule.get("in", "xxxx")))
        self.logger.debug(rule.get("valueIn", "yyyy"))
        if data_output["newCorreoUrl"].get(rule.get("in", "xxxx")).decode('utf-8') == \
            rule.get("valueIn", "yyyy"):
            action = rule.get("action")
            self.logger.debug(action)
            if action == "SPACES":
                data_output["newCorreoUrl"][rule.get("out", "zzz")] = ''
            elif action == "COPY":
                data_output["newCorreoUrl"][rule.get("out", "zzz")] = rule.get("valueOut", "ERROR")
            elif action == "COPY-ANOTHER":
                data_output["newCorreoUrl"][rule.get("out", "zzz")] = \
                data_output["newCorreoUrl"][rule.get("another", "zzz")]
            self.logger.debug(rule.get("out", "zzz"))
            self.logger.debug(data_output["newCorreoUrl"][rule.get("out", "zzz")])
            self.logger.debug(data_output)
        return data_output

    def review_data_ok(self, data_imput, rules_review_data):
        """ review which elements are mandatory """
        self.logger.info("Rules Review Data")
        self.logger.info(rules_review_data)
        status = True
        for variable_review in rules_review_data:
            if data_imput.get("newCorreoUrl", {}).get(variable_review, "") is "":
                status = False
        return status

    def process_variable(self, variable, rules_transform):
        """analize each varable of rules"""
        self.logger.info("Process Variable: "+variable)
        self.logger.info(rules_transform)
        secuences = rules_transform.get("secuences", [{"tipo":"class", "elemento":"xx"}])
        self.logger.debug(secuences)
        split = rules_transform.get("split", None)
        self.logger.debug(split)
        out = rules_transform.get("out", {"tipo":"text", "initText":None})
        self.logger.debug(out)

        driver_work = self.driver

        #secuences
        try:
            for secuence in secuences:
                if secuence["tipo"] == "class":
                    driver_work = driver_work.find_element_by_class_name(secuence["elemento"])
                elif secuence["tipo"] == "tag":
                    driver_work = driver_work.find_element_by_tag_name(secuence["elemento"])
            text_after_secuence = driver_work.text.encode("utf-8")
            self.logger.debug("text_after_secuence %s", text_after_secuence)
        except NoSuchElementException as error:
            self.logger.warning("Error secuences: ")
            self.logger.warning(secuences)
            self.logger.warning("Error find information: %s", error.args)
            text_after_secuence = ""

        #split
        self.logger.debug("text_after_secuence: "+text_after_secuence)

        if split is None:
            text_split = text_after_secuence
        else:
            text_split = self.split_text(text_after_secuence, split)
        self.logger.debug("text_split: "+text_split)

        #out
        text_out = format_text_out(text_split, out)

        return text_out

    def split_text(self, text, split_rule):
        """Split text with rule defined"""
        self.logger.info("Process Split: ")
        self.logger.debug(split_rule)
        cfg_position_initial = split_rule.get("n", 0)
        cfg_text_initial = split_rule.get("initText", "")
        cfg_text_split = split_rule.get("text", "")

        list_text_split = text.split(cfg_text_split)

        if cfg_text_initial is None or\
           cfg_text_initial == ''   or\
           list_text_split.count(cfg_text_initial) == 0:
            position_split_prev = 0
        else:
            position_split_prev = list_text_split.index(cfg_text_initial)
        if len(list_text_split) > (cfg_position_initial+position_split_prev):
            split_out = list_text_split[cfg_position_initial+position_split_prev]
        else:
            split_out = ""
        return split_out

#Functions

def format_text_out(text, out):
    """Format text for output"""
    if out["tipo"] == "text":
        return text
    elif out["tipo"] == "fecha-dif":
        return decrease_date(text)
    elif out["tipo"] == "fecha":
        if text == "":
            return datetime.datetime.now()
        else:
            return datetime.datetime.strptime(text, out["formato"])
    return None

def decrease_date(date_imput):
    """ Decrease date """
    date_imput = date_imput.lower()
    list_date = date_imput.split()
    list_date_number = [int(s) for s in date_imput.split() if s.isdigit()]
    if len(list_date_number) > 0:
        number_date = list_date_number[0]
    else:
        number_date = 0
    delta_number = datetime.timedelta(days=number_date)
    list_string_month = ['mes', 'meses', 'month', 'months']
    for string_month in list_string_month:
        if string_month in list_date:
            delta_number = datetime.timedelta(months=number_date)
    date_final = datetime.datetime.now() - delta_number
    return date_final

"""
    def analizador (driver, secuencia=[{"tipo":"class", "elemento":"xx"}], split=None, \
                                                             salida={"tipo":"text", "initText":None}, vision=0):
        try:
        #fase localizador
            if vision==1:
                print "+++++++++++++++++++++++++++++++++++++++++++"
                print "                                     modo Visual "
                print "+++++++++++++++++++++++++++++++++++++++++++"
            if vision==1:
                print "+ secuencia: {0}".format(secuencia)
                print "+ split:         {0}".format(split)
                print "+ salida:        {0}".format(salida)
                print "+++++++++++++++++++++++++++++++++++++++++++"
            driverTemp=driver 
            for ele in secuencia:
                if ele["tipo"] == "class":
                    driverTemp = driverTemp.find_element_by_class_name(ele["elemento"])
                elif ele["tipo"] == "tag":
                    driverTemp = driverTemp.find_element_by_tag_name(ele["elemento"])
            driverTemp = driverTemp.text.encode("utf-8")
            if vision==1:
                print "+ Despues de driver: {0}".format(driverTemp)
                print "+++++++++++++++++++++++++++++++++++++++++++"
        #fase split                
            if (split == None):
                splitTemp = driverTemp
            else:
                dataTemp = driverTemp.split(split["text"])

                if vision==1:
                    print "+ Paso Split: {0}".format(dataTemp)
                    print "+++++++++++++++++++++++++++++++++++++++++++"

                if split["initText"]== None:
                    pos = 0
                else:
                    pos = dataTemp.index(split["initText"])
                if len(dataTemp)> (split["n"]+pos):
                    splitTemp = dataTemp[split["n"]+pos]
                else:
                    splitTemp = ""
            if vision==1:
                print "+ Despues de split: {0}".format(splitTemp)
                print "+++++++++++++++++++++++++++++++++++++++++++"

        #fase salida
            if salida["tipo"]=="text":
                salida = splitTemp
            elif salida["tipo"]=="fecha-dif":
                salida = fechaDecreciente(splitTemp)
            elif salida["tipo"]=="fecha":
                if splitTemp =="":
                    salida = datetime.datetime.now()
                else:
                    salida = datetime.datetime.strptime(splitTemp, salida["formato"])

            if vision==1:
                print "+++++++++++++++++++++++++++++++++++++++++++"
                print "SALIDA: //{0}//".format(salida)
                print "+++++++++++++++++++++++++++++++++++++++++++"
            return salida
        except NoSuchElementException as e:
            print "+++++++++++++++++++++++++++++++++++++++++++"
            print "                 ERROR: {0}".format(e)
            print "+++++++++++++++++++++++++++++++++++++++++++"

            return ""



    def pending(self, correoUrl):
            if ("linkedin" in url ):
                pagina = "linkedin"
                urlOk = url
                driver.get(urlOk)

                if ver==1:
                    print "***** PAGINA: {0}".format(pagina)
                    print "***** URL: {0}".format(urlOk)
                
                titulo    = analizador(driver, secuencia=[{"tipo":"class", "elemento":"title"}], vision=ver)
                donde     = analizador(driver, secuencia=[{"tipo":"class", "elemento":"location"}], vision=ver)
                summary = analizador(driver, secuencia=[{"tipo":"class", "elemento":"summary"}], vision=ver)
                fecha     = analizador(driver, secuencia=[{"tipo":"class", "elemento":"posted"}], salida={"tipo":"fecha-dif"}, vision=ver)
                company = analizador(driver, secuencia=[{"tipo":"class", "elemento":"company"}], vision=ver)

                if titulo in ["Destaca en lo que haces", "Consultor - Científico de Datos - Scrum Master"]:
                    titulo = ""

                if (company == "") and not (titulo ==""):
                    company = "<NO DEFINIDA>"


                control = self.guardarInformacion(pagina, idCorreoUrl, urlOk, titulo, donde, summary, fecha, company)
                if control=="CORPUS":
                    sumaUrl2Ok +=1


            if ("irishjobs" in url):
                pagina = "irishjob"
                urlOk = url[:url.find("=")]
                driver.get(urlOk)

                if ver==1:
                    print "***** PAGINA: {0}".format(pagina)
                    print "***** URL: {0}".format(urlOk)


                titulo    = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-description"}, {"tipo":"tag", "elemento":"h1"}], vision=ver)
                company = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-description"}, {"tipo":"tag", "elemento":"h2"}], vision=ver)
                donde     = analizador(driver, secuencia=[{"tipo":"class", "elemento":"location"}], vision=ver)
                 if (titulo=="" and company == "" and donde == ""):
                    summary = ""
                else:
                    summary = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-details"}], vision=ver)

                if company == "":
                    company = titulo


                if (titulo=="" and company == "" and donde == "" and summary==""):
                    fecha = ""
                else:
                    fecha     = analizador(driver, \
                                    secuencia=[{"tipo":"class", "elemento":"updated-time"}], split={"text":" ", "n":1, "initText":None}, \
                                    salida={"tipo":"fecha", "formato":"%d/%m/%Y"}, vision=ver)

                control = self.guardarInformacion(pagina, idCorreoUrl, urlOk, titulo, donde, summary, fecha, company)
                if control=="CORPUS":
                    sumaUrl2Ok +=1


            if ("recruitireland" in url):
                pagina = "recruitireland"
                urlOk =string.replace(url, "=2E", ".")
                urlOk =string.replace(urlOk, "=3D", "=")
                driver.get(urlOk)

                if ver==1:
                    print "***** PAGINA: {0}".format(pagina)
                    print "***** URL: {0}".format(urlOk)

                titulo    = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-header"}], split={"text":"\n", "n":0, "initText":None}, vision=ver)
                if    titulo =="THIS JOB HAS BEEN REMOVED BY THE ADVERTISER." :
                    titulo    = ""
                    company = ""
                    donde     = ""
                    summary = ""
                    fecha     = ""
                else:
                    donde     = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-info"}], \
                                        split={"text":"\n", "n":1, "initText":"Location:"}, vision=ver)
                    summary = analizador(driver, secuencia=[{"tipo":"class", "elemento":"generic-text"}], vision=ver)
                    fecha     = analizador(driver, \
                                    secuencia=[{"tipo":"class", "elemento":"job-info"}], split={"text":"\n", "n":1, "initText":"Posted on:"}, \
                                    salida={"tipo":"fecha", "formato":"%d-%b-%Y"}, vision=ver)
                    if (titulo == "" and donde == "" and summary == "" and fecha == ""):
                        company = ""
                    else:
                        company = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-owner-description"}, {"tipo":"tag", "elemento":"a"}], vision=ver)

                control = self.guardarInformacion(pagina, idCorreoUrl, urlOk, titulo, donde, summary, fecha, company)

                if control=="CORPUS":
                    sumaUrl2Ok +=1

            if ".jobs.ie" in url:
                pagina = "jobs.ie"
                urlOk =string.replace(url, "=3D", "=")
                driver.get(urlOk)
                if ver==1:
                    print "***** PAGINA: {0}".format(pagina)
                    print "***** URL: {0}".format(urlOk)
                titulo    = analizador(driver, secuencia=[{"tipo":"class", "elemento":"padding"}, {"tipo":"tag", "elemento":"h1"}], \
                                                    split={"text":"\xe2\x80\x93", "initText":None, "n":0}, vision=ver)
                company = analizador(driver, secuencia=[{"tipo":"class", "elemento":"sidebar"}, {"tipo":"class", "elemento":"acc-panel"}], \
                                    split={"text":"\n", "initText":None, "n":1}, vision=ver)
                donde     = analizador(driver, secuencia=[{"tipo":"class", "elemento":"c1"}], \
                                                    split={"text":"\n", "initText":None, "n":1}, vision=ver)
                summary = analizador(driver, secuencia=[{"tipo":"class", "elemento":"job-description"}], vision=ver)
                fecha     = analizador(driver, \
                                secuencia=[{"tipo":"class", "elemento":"c2"}], split={"text":"\n", "n":3, "initText":None}, \
                                salida={"tipo":"fecha", "formato":"%d-%m-%Y"}, vision=ver)
                
                control = self.guardarInformacion(pagina, idCorreoUrl, urlOk, titulo, donde, summary, fecha, company)
                if control=="CORPUS":
                    sumaUrl2Ok +=1




            if ".monster." in url:                    
                pagina = "monster.ie"
                urlOk =string.replace(url, "=3D", "=")
                driver.get(urlOk)
                if ver==1:
                    print "***** PAGINA: {0}".format(pagina)
                    print "***** URL: {0}".format(urlOk)
                titulo    = analizador(driver, secuencia=[{"tipo":"class", "elemento":"title"}], split={"text":" - ", "n":0, "initText":None}, vision=ver)
                if (titulo=="Does your CV pass the 6-second test?") or ("visualizaciones" in titulo):
                    titulo    = ""
                    company = ""
                    donde     = ""
                    summary = ""
                    fecha     = ""
                else:

                    company = analizador(driver, secuencia=[{"tipo":"class", "elemento":"title"}], split={"text":" - ", "n":1, "initText":None}, vision=ver)
                    donde     = analizador(driver, secuencia=[{"tipo":"class", "elemento":"subtitle"}], vision=ver)
                    summary = analizador(driver, secuencia=[{"tipo":"class", "elemento":"details-content"}], vision=ver)
                    fecha = analizador(driver, secuencia=[{"tipo":"class", "elemento":"mux-job-summary"}], \
                                                                                            split={"text":"\n", "n":1, "initText":"Posted"}, 
                                                                                            salida={"tipo":"fecha-dif"}, vision=ver)


                control = self.guardarInformacion(pagina, idCorreoUrl, urlOk, titulo, donde, summary, fecha, company)
                if control=="CORPUS":
                    sumaUrl2Ok +=1


            #proceso OTRO
            lista = ["saongroup", "mailchimp", "www.w3.org", ".png", "123.ie", ".jpg", "hero.ie", "www.facebook.com", "twitter.com", \
                             "plus.google.com", "youtube.com", "maps.google.com", "awstrack.me", ".gif", "/logos/", "www.albertoggago.es", \
                             "register-cv", "login", "jobs-alerts", "logs11.xiti.com", "emltrk.com", "www.w3c.org", "www.lectiva.com", \
                             "infojobs", "monster.secure.force.com", "caliber", "computerfutures", "vodafone.ie", "profitsflow", "citywonders", \
                             "googleusercontent", "googleapis"]
            otroInd = False
            for ele in lista:
                if ele in url:
                    otroInd = True
            if otroInd:
                control = "OTRO"
                pagina ="N/D"



            if (control==""):
                if pagina == "":
                    pagina ="N/D"
                if urlOk =="":
                    urlOk = url
                print "** ERROR************************************************************************" 
                print "URL ERRONEA: "+urlOk
                print "** ERROR************************************************************************" 
                control = "ERROR"

            sumaUrl2 +=1

            self.mongoDBAccess.update_one("correoUrl", {"_id":idCorreoUrl}, {"control":control, "pagina":pagina})

    def saveInformacion (self, correoUrl):
        if not (titulo=="" or donde == "" or summary == "" or fecha =="" or company == ""):
            actualiza = {}
            actualiza["urlOk"]=urlOk
            actualiza["titulo"]=titulo
            actualiza["donde"]=donde
            actualiza["summary"]=summary
            actualiza["fecha"]=fecha
            actualiza["company"]=company

            self.mongoDBAccess.update_one("correoUrl", {"_id":correoUrl}, actualiza)
            return "CORPUS"
        elif (titulo=="" and donde == "" and summary == "" and fecha =="" and company == ""):
            print "++++++++++++++++++++++++++++++++++++++"
            print "                             SEARCH "
            print "++++++++++++++++++++++++++++++++++++++"
            print "urlOk    :    //{0}".format(urlOk)
            return "SEARCH"
        else: 
            print "**********************************"
            print "                             ERROR "
            print "**********************************"
            print "pagina    {0}".format(pagina)
            print "**********************************"
            print "urlOk    :    //{0}".format(urlOk)
            print "titulo :    //{0}//".format(titulo)
            print "donde    :    //{0}//".format(donde)
            print "summary:    //{0}//".format(summary[:20])
            print "fecha    :    //{0}//".format(fecha)
            print "company:    //{0}//".format(company)
            print "**********************************"
            return "ERROR"



#review code
def recursivo (x):
    print x
    if not(x.text is None):
        print x.text.encode('utf-8')
    for z in x:
        recursivo(z)

def fechaDecreciente (date_imput):
    date_imput = date_imput.lower()
    list_date = date_imput.split()
    list_date_number = [int(s) for s in date_imput.split() if s.isdigit()]
    if len(list_date_number)>0:
        number_date = list_date_number[0]
    else:
        number_date = 0
    fecha = datetime.datetime.now()
    if ('dias' in list_date or 'días' in list_date or 'dia' in list_date or 'día' in list_date or 'day' in list_date or 'days' in list_date):
        delta_number = datetime.timedelta(days=number_date)
        fecha = fecha - delta_number
    elif ('mes' in list_date or 'meses' in list_date or 'month' in list_date or 'months' in list_date ):
        delta_number = datetime.timedelta(months=number_date)
        fecha = fecha - delta_number
    return fecha



def analizador (driver, secuencia=[{"tipo":"class", "elemento":"xx"}], split=None, salida={"tipo":"text", "initText":None}, vision=0):
    #split={"text"="-", "n"=0}
    try:
    #fase localizador
        if vision==1:
            print "+++++++++++++++++++++++++++++++++++++++++++"
            print "                                     modo Visual "
            print "+++++++++++++++++++++++++++++++++++++++++++"
        if vision==1:
            print "+ secuencia: {0}".format(secuencia)
            print "+ split:         {0}".format(split)
            print "+ salida:        {0}".format(salida)
            print "+++++++++++++++++++++++++++++++++++++++++++"
        driverTemp=driver 
        for ele in secuencia:
            if ele["tipo"] == "class":
                driverTemp = driverTemp.find_element_by_class_name(ele["elemento"])
            elif ele["tipo"] == "tag":
                driverTemp = driverTemp.find_element_by_tag_name(ele["elemento"])
        driverTemp = driverTemp.text.encode("utf-8")
        if vision==1:
            print "+ Despues de driver: {0}".format(driverTemp)
            print "+++++++++++++++++++++++++++++++++++++++++++"
    #fase split                
        if (split == None):
            splitTemp = driverTemp
        else:
            dataTemp = driverTemp.split(split["text"])

            if vision==1:
                print "+ Paso Split: {0}".format(dataTemp)
                print "+++++++++++++++++++++++++++++++++++++++++++"

            if split["initText"]== None:
                pos = 0
            else:
                pos = dataTemp.index(split["initText"])
            if len(dataTemp)> (split["n"]+pos):
                splitTemp = dataTemp[split["n"]+pos]
            else:
                splitTemp = ""
        if vision==1:
            print "+ Despues de split: {0}".format(splitTemp)
            print "+++++++++++++++++++++++++++++++++++++++++++"

    #fase salida
        if salida["tipo"]=="text":
            salida = splitTemp
        elif salida["tipo"]=="fecha-dif":
            salida = fechaDecreciente(splitTemp)
        elif salida["tipo"]=="fecha":
            if splitTemp =="":
                salida = datetime.datetime.now()
            else:
                salida = datetime.datetime.strptime(splitTemp, salida["formato"])

        if vision==1:
            print "+++++++++++++++++++++++++++++++++++++++++++"
            print "SALIDA: //{0}//".format(salida)
            print "+++++++++++++++++++++++++++++++++++++++++++"
        return salida
    except NoSuchElementException as e:
        print "+++++++++++++++++++++++++++++++++++++++++++"
        print "                 ERROR: {0}".format(e)
        print "+++++++++++++++++++++++++++++++++++++++++++"

        return ""
"""
