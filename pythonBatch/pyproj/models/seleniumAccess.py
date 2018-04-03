#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique AnalyzerWebJobs """

#import string
#import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from pyvirtualdisplay import Display

#own classes
from pyproj.logger import Logger
from pyproj.textanalyzer import TextAnalyzer


class SeleniumAccess(object):
    """Analyze information of each scrapint of a job and contruct information for save"""

    config = None
    logger = None
    #display = None
    driver = None
    text_analyzer = None

    def __init__(self, config, level_log):
        self.logger = Logger(self.__class__.__name__, level_log).get()
        self.config = config
        self.text_analyzer = TextAnalyzer(level_log)

    def open_selenium(self):
        """open driver for scraping"""
        self.driver = webdriver.Remote(\
                      command_executor=self.config.get("urlSelenium"),\
                      desired_capabilities=DesiredCapabilities.CHROME)

    def close_selenium(self):
        """close driver for scraping"""
        if self.driver != None:
            self.driver.stop_client()
            self.driver.close()
            #self.display.stop()

    def analyze(self, correo_url):
        """module analyze get url and prepare scraping"""
        if self.driver is None:
            return {}
        result = {}
        self.determinate_web(result, correo_url["url"])
        if result.get("control", "") == "REVIEW":
            self.driver.get(result.get("urlOk", ""))
            self.find_data(result)
        else:
            result["status"] = False
        return result

    def determinate_web(self, result_imput, web_url):
        """ determinate web where working to set configuration to analize of this web"""
        self.logger.info("determinate Web")
        for web in self.config.get("pages", []):
            if web.get("ruleFind", "ERROR-GET-RULEFIND") in web_url:
                self.logger.info("Locate web: %s", web.get("name", "ERROR"))
                result_imput["page"] = web.get("name", "ERROR")
                result_imput["control"] = "REVIEW"
                result_imput["urlOk"] =\
                    self.text_analyzer.real_url_transform(web_url, web.get("rulesTransformUrl", []))

        if result_imput.get("page", None) is None:
            self.determinate_other(result_imput, web_url)

    def determinate_other(self, result, web_url):
        """it has got a list of web to ignore and not compute"""
        for web in self.config.get("otherPages", []):
            if web in web_url:
                self.logger.info("Locate web OTHER: %s", web)
                result["page"] = "N/D"
                result["control"] = "OTRO"
        if result.get("page", None) is None:
            self.logger.info("Locate web ERROR: %s", web_url)
            result["page"] = "N/D"
            result["control"] = "ERROR"

    def find_data(self, result_imput):
        """Find Information using rules of web"""
        self.logger.info("Find Data")
        rules_page = {}
        pages = self.config["pages"]
        for page in pages:
            if page["name"] == result_imput["page"]:
                self.logger.info("Locate page get rules: ")
                self.logger.debug(page)
                rules_page = page

        necesary_variables = rules_page.get("necesaryVariables", [])
        result_imput["newCorreoUrl"] = {}
        for variable in necesary_variables:
            result_imput["newCorreoUrl"][variable] = self.process_variable(variable,\
                                      rules_page.get("rulesTransformData", []).get(variable, {}))

        #determinate rules after search
        result_with_global_rules =\
            self.text_analyzer.data_after_selenium(result_imput,\
                                                        rules_page.get("rulestransformFinal", []))
        result_with_global_rules["status"] = \
            self.text_analyzer.review_data_ok(result_with_global_rules,\
                                             rules_page.get("rulesOkFinding", []))
        if result_with_global_rules["status"]:
            result_with_global_rules["control"] = "CORPUS"
        else:
            result_with_global_rules["control"] = "SEARCH"
        self.logger.debug(result_with_global_rules)
        return result_with_global_rules

    def process_variable(self, variable, rules_transform):
        """analize each varable of rules"""
        self.logger.info("Process Variable: %s", variable)
        self.logger.info(rules_transform)

        #secuences
        secuences = rules_transform.get("secuences", [{"tipo":"class", "elemento":"xx"}])
        self.logger.debug(secuences)
        text_after_secuence = self.in_driver_data_and_return_text(secuences)

        #split
        self.logger.debug("text_after_secuence: %s", text_after_secuence)
        split = rules_transform.get("split", None)
        self.logger.debug(split)
        if split is None:
            text_split = text_after_secuence
        else:
            text_split = self.text_analyzer.split_text(text_after_secuence, split)

        #out
        self.logger.debug("text_split: %s", text_split)

        out = rules_transform.get("out", {"tipo":"text", "initText":None})
        self.logger.debug(out)

        text_out = self.text_analyzer.format_text_out(text_split, out)

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
