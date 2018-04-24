#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" process web page and analyse """
import types

#own classes
from pyproj.resultanalyze import ResultAnalyze
from pyproj.analyzervariable import AnalyzerVariable

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
    _config = None

    def __init__(self, config):
        self._config = config
        self._config_param_analyze = config.get_config_param().get("webPagesDef", {})
        self._logger = config.get_logger(self.__class__.__name__)

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
            return  self.real_url_transform(web_url, web_rules.get("rulesTransformUrl", []))

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
                        AnalyzerVariable(self._config) \
                                         .process( \
                                         rule_variable,\
                                         rules_page.get("rulesTransformData", [])\
                                                   .get(rule_variable, {}),\
                                         driver) \
                        )

        #determinate rules after search
        self.process_after_get_variables(result_analyze, \
                                         rules_page.get("rulestransformFinal", []))
        result_analyze.set_status(self.review_data_ok(result_analyze,\
                                                          rules_page.get("rulesOkFinding", [])))
        result_analyze.set_control(CONTROL_ALL_OK if result_analyze.get_status() \
                                                  else CONTROL_ALL_NOTHING)

        self._logger.debug(result_analyze.get_return_all())

    def real_url_transform(self, web_intro, rules):
        """ transform url using rules to eliminate wrong data"""
        self._logger.info("Rules Transform URL: ")
        self._logger.info(rules)
        if not isinstance(rules, types.ListType):
            self._logger.error("Rules not List")
            return ""
        web_output = web_intro
        for rule_url_transform in rules:
            web_output = self.transform_url_role(web_output, rule_url_transform)
        return web_output

    def transform_url_role(self, url, rule):
        """ Transform url with one rule"""
        self._logger.info("Rule Transform URL: ")
        self._logger.info(rule)
        if not isinstance(rule, types.DictType):
            self._logger.error("Rule not Dictionary")
            return ""
        return url.replace(rule.get("from", "NOFIND12345"), rule.get("to", "ERROR-RULE"))

    def process_after_get_variables(self, result_analyze, rules_after_selenium):
        """ With rules transform output for modify data """
        self._logger.info("Rules Transform after Selenium")
        self._logger.info(rules_after_selenium)
        if not isinstance(rules_after_selenium, types.ListType):
            self._logger.error("Rules not List")
        for rule in rules_after_selenium:
            self.apply_rule_after_sel(result_analyze, rule)

    def apply_rule_after_sel(self, result_analyze, rule):
        """ get rule and aply to output"""
        self._logger.debug("Rule Unique Transform after Selenium")
        if not isinstance(rule, types.DictType):
            self._logger.error("Rule not Dict")
        else:
            self.apply_rule_after_sel_correct(result_analyze, rule)

    def apply_rule_after_sel_correct(self, result_analyze, rule):
        """part apply rule after sel correct"""
        self._logger.debug(rule.get("valueIn", "yyyy"))
        self._logger.debug(result_analyze.get_content_variable(rule.get("in", "xxxx")))
        in_variable = rule.get("in", "IN-ERROR")
        if result_analyze.get_content_variable(in_variable) != None and\
           result_analyze.get_content_variable(in_variable)\
           .decode('utf-8', 'ignore')\
           .encode('utf-8', 'ignore') ==\
               rule.get("valueIn", "VALUE-ERROR"):
            action = rule.get("action")
            out_variable = rule.get("out", "OUT-ERROR")
            self._logger.debug(action)
            if action == "SPACES":
                result_analyze.set_content_variable(out_variable, "")
            elif action == "COPY":
                result_analyze.set_content_variable(out_variable, \
                                                    rule.get("valueOut", "ERROR-VALUE-OUT"))
            elif action == "COPY-ANOTHER":
                another_variable = rule.get("another", "ERROR-ANOTHER")
                if another_variable != "ERROR-ANOTHER":
                    result_analyze \
                      .set_content_variable(out_variable, \
                                            result_analyze.get_content_variable(another_variable))
            self._logger.debug(rule.get("out", "zzz"))
            self._logger.debug(result_analyze.get_content_variable(out_variable))

    def review_data_ok(self, result_analyze, rules_review_data):
        """ review which elements are mandatory """
        self._logger.info("Rules Review Data")
        self._logger.info(rules_review_data)
        if not isinstance(rules_review_data, types.ListType):
            self._logger.error("Rules not List")
            return False
        status = True
        print rules_review_data
        for variable_review in rules_review_data:
            print variable_review
            print result_analyze.get_content_variable(variable_review)
            if result_analyze.get_content_variable(variable_review) == "":
                status = False
        return status
