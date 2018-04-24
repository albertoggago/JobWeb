#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique AnalyzerWebJobs """
from selenium.common.exceptions import NoSuchElementException

#own classes
from pyproj.textruleanalyzer import TextRuleAnalyzer
from pyproj.resultanalyze import ResultAnalyze

NONE_DETERMINATE = "N/D"
CONTROL_OK = "REVIEW"
CONTROL_OTHER = "OTRO"
CONTROL_ERROR = "ERROR"
CONTROL_ALL_OK = "CORPUS"
CONTROL_ALL_NOTHING = "SEARCH"

class AnalyzerWebJobs(object):
    """Analyze information of each scrapint of a job and contruct information for save"""

    _config_param_analyze = None
    _logger = None
    _text_rule_analyzer = None
    _config = None

    def __init__(self, config):
        self._config = config
        self._config_param_analyze = config.get_config_param().get("webPagesDef", {})
        self._logger = config.get_logger(self.__class__.__name__)
        self._text_rule_analyzer = TextRuleAnalyzer(config)

    def analyze(self, correo_url, driver):
        """module analyze get url and prepare scraping"""
        url = correo_url["url"]
        web_rules = self.return_rules(url)
        result_analyze = ResultAnalyze(self._config)
        result_analyze.set_page(self.get_page(web_rules))
        result_analyze.set_control(self.get_control(web_rules, url))
        result_analyze.set_new_url(self.get_new_url(web_rules, url))
        return self.review_continue_process(driver, result_analyze)

    def return_rules(self, web_url):
        """ determinate web where working to set configuration to analize of this web"""
        self._logger.info("get page of list")
        for web_rules in self._config_param_analyze.get("pages", []):
            if web_rules.get("ruleFind", "ERROR-GET-RULEFIND") in web_url:
                self._logger.info("Locate : %s", web_rules)
                return web_rules
        return None

    def get_page(self, web_rules):
        """  fin state web depending of page """
        self._logger.info("get control")
        if web_rules is None:
            return NONE_DETERMINATE
        else:
            return web_rules.get("name", "ERROR")

    def get_control(self, web_rules, url):
        """  fin state web depending of page """
        self._logger.info("get control")
        if web_rules is None:
            return self.get_control_other(url)
        else:
            return CONTROL_OK

    def get_control_other(self, url):
        """it has got a list of web to ignore and not compute"""
        for web in self._config_param_analyze.get("otherPages", []):
            if web in url:
                return CONTROL_OTHER
        return CONTROL_ERROR

    def get_new_url(self, web_rules, web_url):
        """get new url"""
        if web_rules is None:
            return web_url
        else:
            return  self._text_rule_analyzer\
                        .real_url_transform(web_url, web_rules.get("rulesTransformUrl", []))

    def review_continue_process(self, driver, result_analyze):
        """ review if is necessary contiue """
        if result_analyze.get_control() == CONTROL_OK:
            driver.get(result_analyze.get_new_url())
            self.analyze_page(result_analyze, driver)
        else:
            result_analyze.set_status(False)
        return result_analyze.get_return_all()

    def analyze_page(self, result_analyze, driver):
        """analyze a page correct, result_analyze"""
        self._logger.info("Find Rules Web Content")
        print "page: {0}".format(result_analyze.get_page())
        rules_page = self.return_rules(result_analyze.get_new_url())
        print "Rules_page: {0}".format(rules_page)

        #process search in rule variable
        for rule_variable in rules_page.get("necesaryVariables", []):
            result_analyze.set_content_variable(\
                   rule_variable, \
                   self.get_text_variable(rule_variable,\
                                         rules_page.get("rulesTransformData", [])\
                                                   .get(rule_variable, {}),\
                                          driver))

        #determinate rules after search
        self._text_rule_analyzer\
            .process_after_get_variables(result_analyze, \
                                         rules_page.get("rulestransformFinal", []))
        result_analyze.set_status(self._text_rule_analyzer.review_data_ok(result_analyze,\
                                                          rules_page.get("rulesOkFinding", [])))
        result_analyze.set_control(CONTROL_ALL_OK if result_analyze.get_status() \
                                                  else CONTROL_ALL_NOTHING)

        self._logger.debug(result_analyze.get_return_all())

    def get_text_variable(self, variable, rules_transform, driver):
        """analize each varable of rules"""
        self._logger.info("Process Variable: %s", variable)
        self._logger.info(rules_transform)

        #secuences
        secuences = rules_transform.get("secuences", [{"tipo":"class", "elemento":"xx"}])
        self._logger.debug(secuences)
        text_after_secuence = self.in_driver_data_and_return_text(secuences, driver)

        #split
        self._logger.debug("text_after_secuence: %s", text_after_secuence)
        split = rules_transform.get("split", None)
        self._logger.debug(split)
        if split is None:
            text_split = text_after_secuence
        else:
            text_split = self._text_rule_analyzer.split_text(text_after_secuence, split)

        #out
        self._logger.debug("text_split: %s", text_split)

        out = rules_transform.get("out", {"tipo":"text", "initText":None})
        self._logger.debug(out)

        text_out = self._text_rule_analyzer.format_text_out(text_split, out)

        return text_out

    def in_driver_data_and_return_text(self, secuences, driver):
        """ Select of driver selenium data using secuences rules"""
        driver_work = driver
        try:
            for secuence in secuences:
                if secuence["tipo"] == "class":
                    driver_work = driver_work.find_element_by_class_name(secuence["elemento"])
                elif secuence["tipo"] == "tag":
                    driver_work = driver_work.find_element_by_tag_name(secuence["elemento"])
            text_after_secuence = driver_work.text.encode("utf-8", errors='ignore')
            self._logger.debug("text_after_secuence %s", text_after_secuence)
            return text_after_secuence
        except NoSuchElementException as error:
            self._logger.warning("Error secuences: ")
            self._logger.warning(secuences)
            self._logger.warning("Error find information: %s", error.args)
            return ""
