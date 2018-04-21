#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" file include class ReadAndAnalyse """

import json

from pyproj.logger import Logger


class Config(object):
    """ Process of save config and focus the level log"""
    _config_param = None
    _level_log = None

    def __init__(self, fileConfig, levelLog):
        self._level_log = levelLog
        try:
            self._config_param = json.loads(open(fileConfig, "r").read())
        except IOError:
            self._config_param = {}
            print "File Error: {}".format(fileConfig)

    def get_level_log(self):
        """return level log"""
        return self._level_log

    def get_logger(self, name):
        """return logger configurate"""
        return Logger(name, self._level_log).get()

    def get_config_param(self):
        """ return config """
        return self._config_param
