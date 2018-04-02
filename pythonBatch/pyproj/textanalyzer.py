#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique TextAnalyzer """
import datetime
import types

#own classes
from pyproj.logger import Logger

class TextAnalyzer(object):
    """Analyze text for AnalizerWebJobs"""

    logger = None

    def __init__(self, level_log):
        self.logger = Logger(self.__class__.__name__, level_log).get()

    def real_url_transform(self, web_intro, rules):
        """ transform url using rules to eliminate wrong data"""
        self.logger.info("Rules Transform URL: ")
        self.logger.info(rules)
        if not isinstance(rules, types.ListType):
            self.logger.error("Rules not List")
            return ""
        web_output = web_intro
        for rule_url_transform in rules:
            web_output = self.transform_url_role(web_output, rule_url_transform)
        return web_output

    def transform_url_role(self, url, rule):
        """ Transform url with one rule"""
        self.logger.info("Rule Transform URL: ")
        self.logger.info(rule)
        if not isinstance(rule, types.DictType):
            self.logger.error("Rule not Dictionary")
            return ""
        return url.replace(rule.get("from", "NOFIND12345"), rule.get("to", "ERROR-RULE"))

    def data_after_selenium(self, data_imput, rules_after_selenium):
        """ With rules transform output for modify data """
        data_output = data_imput
        self.logger.info("Rules Transform after Selenium")
        self.logger.info(rules_after_selenium)
        if not isinstance(rules_after_selenium, types.ListType):
            self.logger.error("Rules not List")
            return data_imput
        for rule in rules_after_selenium:
            self.apply_rule_after_sel(data_output, rule)
        return data_imput

    def apply_rule_after_sel(self, data_imput, rule):
        """ get rule and aply to output"""
        data_output = data_imput
        self.logger.debug("Rule Unique Transform after Selenium")
        if not isinstance(rule, types.DictType):
            self.logger.error("Rule not Dict")
            return data_imput
        self.logger.debug(rule.get("valueIn", "yyyy"))
        self.logger.debug(data_output["newCorreoUrl"].get(rule.get("in", "xxxx")))
        in_variable = rule.get("in", "IN-ERROR")
        if data_output["newCorreoUrl"].get(in_variable) != None and\
           data_output["newCorreoUrl"].get(in_variable)\
           .encode('utf-8', 'ignore') ==\
               rule.get("valueIn", "VALUE-ERROR"):
            action = rule.get("action")
            out_variable = rule.get("out", "OUT-ERROR")
            self.logger.debug(action)
            if action == "SPACES":
                data_output["newCorreoUrl"][out_variable] = ''
            elif action == "COPY":
                data_output["newCorreoUrl"][out_variable] =\
                      rule.get("valueOut", "ERROR-VALUE-OUT")
            elif action == "COPY-ANOTHER":
                another_variable = rule.get("another", "ERROR-ANOTHER")
                if another_variable != "ERROR-ANOTHER":
                    data_output["newCorreoUrl"][out_variable] = \
                    data_output["newCorreoUrl"][another_variable]
            self.logger.debug(rule.get("out", "zzz"))
            self.logger.debug(data_output["newCorreoUrl"][out_variable])
            self.logger.debug(data_output)

        return data_output

    def review_data_ok(self, data_imput, rules_review_data):
        """ review which elements are mandatory """
        self.logger.info("Rules Review Data")
        self.logger.info(rules_review_data)
        if not isinstance(rules_review_data, types.ListType):
            self.logger.error("Rules not List")
            return False
        status = True
        for variable_review in rules_review_data:
            if not data_imput.get("newCorreoUrl", {}).get(variable_review, "") :
                status = False
        return status

    def split_text(self, text, split_rule):
        """Split text with rule defined"""
        self.logger.info("Process Split: ")
        self.logger.debug(split_rule)
        if not isinstance(split_rule, types.DictType):
            self.logger.error("Rule not Dict")
            return text

        cfg_position_initial = split_rule.get("n", 0)
        cfg_text_initial = split_rule.get("initText", "")
        cfg_text_split = split_rule.get("text_split", "ERROR-SPLIT-SEPARATOR")
        self.logger.debug("cfg_position_initial: %s", cfg_position_initial)
        self.logger.debug("cfg_text_initial: %s", cfg_text_initial)
        self.logger.debug("cfg_text_split: %s", cfg_text_split)

        text_clean = text.decode("utf-8", errors='ignore') #.encode("utf-8", errors='ignore')

        list_text_split = text_clean.split(cfg_text_split)

        if cfg_text_initial is None or\
           cfg_text_initial == ''   or\
           list_text_split.count(cfg_text_initial) == 0:
            position_split_prev = -1
        else:
            position_split_prev = list_text_split.index(cfg_text_initial)
        if len(list_text_split) > (cfg_position_initial+position_split_prev+1):
            split_out = list_text_split[cfg_position_initial+position_split_prev+1]
        else:
            split_out = ""
        return split_out

    def format_text_out(self, text, out):
        """Format text for output"""
        self.logger.info("Format Text")
        self.logger.debug(text)
        self.logger.debug(out)
        tipo = out.get("tipo", "text")
        if tipo == "text":
            return text
        elif tipo == "fecha-dif":
            return self.decrease_date(text)
        elif tipo == "fecha":
            if text == "":
                return datetime.datetime.now()
            else:
                try:
                    return datetime.datetime.strptime(text, out.get("formato", "%d/%m/%Y"))
                except ValueError as error:
                    self.logger.error("Error Find Date information: %s", error.args)
                    return datetime.datetime.now()
        return None

    def decrease_date(self, date_imput):
        """ Decrease date """
        self.logger.info("Decrease_Date")
        self.logger.debug(date_imput)
        date_imput = date_imput.lower()
        list_date = date_imput.split()
        list_date_number = [int(s) for s in date_imput.split() if s.isdigit()]
        if list_date_number:
            number_date = list_date_number[0]
        else:
            number_date = 0
        delta_number = datetime.timedelta(number_date)
        list_string_month = ['mes', 'meses', 'month', 'months']
        for string_month in list_string_month:
            if string_month in list_date:
                delta_number = datetime.timedelta(number_date*365.25/12)
        date_final = datetime.datetime.now() - delta_number
        return date_final
