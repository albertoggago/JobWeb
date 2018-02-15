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
                       self.function_real_url_transform(web_url, web.get("ruleTransformUrl", {}))

        if result_web.get("page", None) is None:
            result_web = self.determinate_other(result_web, web_url)
        return result_web

    def function_real_url_transform(self, web_intro, rules):
        """ transform url using rules to eliminate wrong data"""
        self.logger.info("Rules Transform URL: ")
        self.logger.info(rules)
        web_output = web_intro
        for rule_url_transform in rules:
            web_output = self.function_transform_url_role(web_output, rule_url_transform)
        return web_output

    def function_transform_url_role(self, url, rule):
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
        result_with_global_rules =\
            self.function_data_after_selenium(data_after_selenium,\
                                                        rules_page.get("rulestransformFinal"))
        result_with_global_rules["status"] = \
            self.function_review_data_ok(result_with_global_rules, rules_page.get("rulesOkFinding"))
        if result_with_global_rules["status"]:
            result_with_global_rules["control"] = "CORPUS"
        else:
            result_with_global_rules["control"] = "SEARCH"
        self.logger.debug(result_with_global_rules)
        return result_with_global_rules

    def function_data_after_selenium(self, data_imput, rules_after_selenium):
        """ With rules transform output for modify data """
        data_output = data_imput
        self.logger.info("Rules Transform after Selenium")
        self.logger.info(rules_after_selenium)
        for rule in rules_after_selenium:
            self.function_apply_rule_to_data(data_output, rule)
        return data_imput

    def function_apply_rule_to_data(self, data_imput, rule):
        """ get rule and aply to output"""
        data_output = data_imput
        self.logger.debug("Rule Unique Transform after Selenium")
        self.logger.debug(data_output["newCorreoUrl"].get(rule.get("in", "xxxx")))
        self.logger.debug(rule.get("valueIn", "yyyy"))
        if data_output["newCorreoUrl"].get(rule.get("in", "xxxx")).\
           decode('utf-8', errors='ignore') == rule.get("valueIn", "yyyy"):
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

    def function_review_data_ok(self, data_imput, rules_review_data):
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

        #secuences
        secuences = rules_transform.get("secuences", [{"tipo":"class", "elemento":"xx"}])
        self.logger.debug(secuences)
        text_after_secuence = self.in_driver_data_and_return_text(secuences)

        #split
        self.logger.debug("text_after_secuence: "+text_after_secuence)
        split = rules_transform.get("split", None)
        self.logger.debug(split)
        if split is None:
            text_split = text_after_secuence
        else:
            text_split = self.function_split_text(text_after_secuence, split)

        #out
        self.logger.debug("text_split: "+text_split)

        out = rules_transform.get("out", {"tipo":"text", "initText":None})
        self.logger.debug(out)

        text_out = self.function_format_text_out(text_split, out)

        return text_out

    def in_driver_data_and_return_text(self, secuences):
        """ Select of driver selenium data using secuences rules"""
        driver_work = self.driver
        try:
            for secuence in secuences:
                if secuence["tipo"] == "class":
                    driver_work = driver_work.find_element_by_class_name(secuence["elemento"])
                elif secuence["tipo"] == "tag":
                    driver_work = driver_work.find_element_by_tag_name(secuence["elemento"])
            text_after_secuence = driver_work.text.encode("utf-8", errors='ignore')
            self.logger.debug("text_after_secuence %s", text_after_secuence)
            return text_after_secuence
        except NoSuchElementException as error:
            self.logger.warning("Error secuences: ")
            self.logger.warning(secuences)
            self.logger.warning("Error find information: %s", error.args)
            return ""

    def function_split_text(self, text, split_rule):
        """Split text with rule defined"""
        self.logger.info("Process Split: ")
        self.logger.debug(split_rule)
        cfg_position_initial = split_rule.get("n", 0)
        cfg_text_initial = split_rule.get("initText", "")
        cfg_text_split = split_rule.get("text", "")

        text_clean = text.decode("utf-8", errors='ignore')#.encode("utf-8", errors='ignore')

        list_text_split = text_clean.split(cfg_text_split)

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

    def function_format_text_out(self, text, out):
        """Format text for output"""
        self.logger.info("Format Text")
        self.logger.debug(text)
        self.logger.debug(out)
        if out["tipo"] == "text":
            return text
        elif out["tipo"] == "fecha-dif":
            return self.function_decrease_date(text)
        elif out["tipo"] == "fecha":
            if text == "":
                return datetime.datetime.now()
            else:
                return datetime.datetime.strptime(text, out["formato"])
        return None

    def function_decrease_date(self, date_imput):
        """ Decrease date """
        self.logger.info("Decrease_Date")
        self.logger.debug(date_imput)
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



"""