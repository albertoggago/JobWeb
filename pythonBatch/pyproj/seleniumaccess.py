#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique AnalyzerWebJobs """

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumAccess(object):
    """Analyze information of each scrapint of a job and contruct information for save"""

    _logger = None
    _config_param = None

    def __init__(self, config):
        self._logger = config.get_logger(self.__class__.__name__)
        self._config_param = config.get_config_param()

    def open_selenium(self):
        """open driver for scraping"""
        self._logger.debug("Open Selenium")
        self._logger.debug("Open Driver")
        return webdriver.Remote(\
                      command_executor=self._config_param.get("urlSelenium"),\
                      desired_capabilities=DesiredCapabilities.CHROME)

    def close_selenium(self, driver):
        """close driver for scraping"""
        if driver != None:
            driver.stop_client()
            driver.close()
            driver = None
        self._logger.debug("Close Driver")
        