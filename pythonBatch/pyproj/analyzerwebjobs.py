#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique AnalyzerWebJobs """
from selenium.common.exceptions import NoSuchElementException

#own classes
from pyproj.textruleanalyzer import TextRuleAnalyzer


class AnalyzerWebJobs(object):
    """Analyze information of each scrapint of a job and contruct information for save"""

    _config_param_analyze = None
    _logger = None
    _text_rule_analyzer = None

    def __init__(self, config):
        self._config_param_analyze = config.get_config_param().get("webPagesDef", {})
        self._logger = config.get_logger(self.__class__.__name__)
        self._text_rule_analyzer = TextRuleAnalyzer(config)

    def analyze(self, correo_url, driver):
        """module analyze get url and prepare scraping"""
        if driver is None:
            self._logger.debug("Driver NULL!!!!!")
            return {}
        result = {}
        self.determinate_web(result, correo_url["url"])
        if result.get("control", "") == "REVIEW":
            driver.get(result.get("urlOk", ""))
            self.find_rules_web_content(result, driver)
        else:
            result["status"] = False
        return result

    def determinate_web(self, json_info_web, web_url):
        """ determinate web where working to set configuration to analize of this web"""
        self._logger.info("determinate Web")
        for web in self._config_param_analyze.get("pages", []):
            if web.get("ruleFind", "ERROR-GET-RULEFIND") in web_url:
                self._logger.info("Locate web: %s", web.get("name", "ERROR"))
                json_info_web["page"] = web.get("name", "ERROR")
                json_info_web["control"] = "REVIEW"
                json_info_web["urlOk"] =\
                    self._text_rule_analyzer\
                        .real_url_transform(web_url, web.get("rulesTransformUrl", []))

        if json_info_web.get("page", None) is None:
            self.determinate_other_web(json_info_web, web_url)

    def determinate_other_web(self, json_info, web_url):
        """it has got a list of web to ignore and not compute"""
        for web in self._config_param_analyze.get("otherPages", []):
            if web in web_url:
                self._logger.info("Locate web OTHER: %s", web)
                json_info["page"] = "N/D"
                json_info["control"] = "OTRO"
        if json_info.get("page", None) is None:
            self._logger.info("Locate web ERROR: %s", web_url)
            json_info["page"] = "N/D"
            json_info["control"] = "ERROR"

    def find_rules_web_content(self, json_info_web, driver):
        """Find Information using rules of web"""
        self._logger.info("Find Rules Web Content")
        rules_page = {}
        for page in self._config_param_analyze.get("pages", {}):
            if page["name"] == json_info_web["page"]:
                self._logger.info("Locate page get rules: ")
                self._logger.debug(page)
                rules_page = page

        necesary_variables = rules_page.get("necesaryVariables", [])
        json_info_web["newCorreoUrl"] = {}
        for variable in necesary_variables:
            json_info_web["newCorreoUrl"][variable] = self.process_variable(variable,\
                                      rules_page.get("rulesTransformData", []).get(variable, {}),\
                                                                            driver)

        #determinate rules after search
        self._text_rule_analyzer.process_after_get_variables(json_info_web,\
                                                        rules_page.get("rulestransformFinal", []))
        json_info_web["status"] = \
            self._text_rule_analyzer.review_data_ok(json_info_web,\
                                             rules_page.get("rulesOkFinding", []))
        if json_info_web["status"]:
            json_info_web["control"] = "CORPUS"
        else:
            json_info_web["control"] = "SEARCH"
        self._logger.debug(json_info_web)

    def process_variable(self, variable, rules_transform, driver):
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
