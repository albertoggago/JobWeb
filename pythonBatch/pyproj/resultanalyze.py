#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" save and manage result analyze """

ERROR = "ERROR"

class ResultAnalyze(object):
    """Analyze information of each scrapint of a job and contruct information for save"""

    _config_param_analyze = None
    _logger = None

    _var_page = None
    _var_control = None
    _var_new_url = None
    _var_status = None
    _var_list_content_variable = {}

    def __init__(self, config):
        self._config_param_analyze = config.get_config_param()
        self._logger = config.get_logger(self.__class__.__name__)

    def get_page(self):
        """ save variable page"""
        return self._var_page

    def get_control(self):
        """ save variable page"""
        return self._var_control

    def get_new_url(self):
        """ save variable page"""
        return self._var_new_url

    def get_status(self):
        """ save variable page"""
        return self._var_status

    def get_content_variable(self, variable):
        """ return a specific variable saved"""
        return self._var_list_content_variable.get(variable, ERROR)

    def set_page(self, page):
        """ save variable page"""
        self._var_page = page

    def set_control(self, control):
        """ save variable page"""
        self._var_control = control

    def set_new_url(self, new_url):
        """ save variable page"""
        self._var_new_url = new_url

    def set_status(self, status):
        """ save variable page"""
        self._var_status = status

    def set_content_variable(self, var, value):
        """ add element to content variables"""
        self._var_list_content_variable[var] = value

    def get_return_all(self):
        """ return all variables saved inside """
        return {"page":self._var_page, \
                "control":self._var_control, \
                "urlOk": self._var_new_url,
                "status": self._var_status,
                "newCorreoUrl": self._var_list_content_variable}
