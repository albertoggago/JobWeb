#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique AnalyzerWebJobs """
import datetime
import types

from selenium.common.exceptions import NoSuchElementException

#own classes

class AnalyzerVariable(object):
    """ main class"""

    _logger = None
    _config = None


    def __init__(self, config):
        self._config = config
        self._logger = config.get_logger(self.__class__.__name__)

    def process(self, variable, rules_transform, driver):
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
            text_split = self.split_text(text_after_secuence, split)

        #out
        self._logger.debug("text_split: %s", text_split)

        out = rules_transform.get("out", {"tipo":"text", "initText":None})
        self._logger.debug(out)

        text_out = self.format_text_out(text_split, out)

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

    def split_text(self, text, split_rule):
        """Split text with rule defined"""
        self._logger.info("Process Split: ")
        self._logger.debug(split_rule)
        if not isinstance(split_rule, types.DictType):
            self._logger.error("Rule not Dict")
            return text

        cfg_position_initial = split_rule.get("n", 0)
        cfg_text_initial = split_rule.get("initText", "")
        cfg_text_split = split_rule.get("text_split", "ERROR-SPLIT-SEPARATOR")
        self._logger.debug("cfg_position_initial: %s", cfg_position_initial)
        self._logger.debug("cfg_text_initial: %s", cfg_text_initial)
        self._logger.debug("cfg_text_split: %s", cfg_text_split)

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
        self._logger.info("Format Text")
        self._logger.debug(text)
        self._logger.debug(out)
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
                    self._logger.error("Error Find Date information: %s", error.args)
                    return datetime.datetime.now()
        return None

    def decrease_date(self, date_imput):
        """ Decrease date """
        self._logger.info("Decrease_Date")
        self._logger.debug(date_imput)
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
