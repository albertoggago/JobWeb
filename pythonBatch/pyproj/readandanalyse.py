#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" file include class ReadAndAnalyse """

import datetime
import urllib2
from selenium.common.exceptions import WebDriverException

from pyproj.mongodbaccess import MongoDBAccess
from pyproj.mailaccess import MailAccess
from pyproj.analyzerwebjobs import AnalyzerWebJobs
from pyproj.seleniumaccess import SeleniumAccess


class ReadAndAnalyse(object):
    """ Class for read and analize information, combine class"""
    _logger = None
    _mongo_db_access = None
    _mail_access = None
    _analyzer_web_jobs = None
    _seleniumaccess = None
    _config_param = None

    def __init__(self, config):
        self._logger = config.get_logger(self.__class__.__name__)
        self._config_param = config.get_config_param()

        self._mongo_db_access = MongoDBAccess(config)
        self._mail_access = MailAccess(config)
        self._seleniumaccess = SeleniumAccess(config)
        self._analyzer_web_jobs = AnalyzerWebJobs(config)
        self._logger.info("Inicio: %s", datetime.datetime.now())

    def finding_mails(self):
        """Module for looking for emails return emails finding """
        self._logger.info("find_emails")
        if not self._mail_access.status():
            self._logger.error("Error mail Not Active")
            return None
        if not self._mongo_db_access.status():
            self._logger.error("Error Database Not Active")
            return None

        count_emails = 0
        list_emails = self._mail_access.search_mails("inbox")

        for ele in list_emails:
            mail = self._mail_access.compose_mail_json(self._mail_access.get(ele))
            if mail is None:
                self._logger.error("Mail generate wrong")
            else:
                self._logger.debug("Insert into Control")
                self._logger.debug("control: %s", mail.get("control"))
                self._logger.debug("urls: %s", mail.get("urls"))
                self._logger.debug("datetime: %s", mail.get("datetime"))
                self._mongo_db_access.insert("correo", mail)
                count_emails += 1
                self._mail_access.store(ele)

        if self._config_param.get("env", "DEV") == "PRODUCTION":
            self._logger.info("CLEAN EMAIL")
            self._mail_access.clean()
        self._mail_access.logout()
        self._logger.info("emails reads : %s", count_emails)
        return count_emails

    def finding_urls(self):
        """ Find urls inside of mails saved """
        self._logger.info("FINDING_URLS")
        if not self._mongo_db_access.status():
            self._logger.error("Error Database Not Active")
            return None

        count_urls = 0
        mails = self._mongo_db_access.find("correo", {"control":{"$exists":0}}, \
                                              sort={"urls":1, "_id":1})
        for mail in mails:
            for url in mail.get("urls", []):
                correo_url = build_mail_url(mail["_id"], url)
                count_urls += self.review_mail_url(correo_url, url)
            self._mongo_db_access.update_one("correo", {"_id":mail["_id"]}, {"control":"DONE"})
        self._logger.info("URLS read: %s", count_urls)
        return count_urls

    def review_mail_url(self, mail_url, url):
        """ review mail url looking for in dabase and when not exist save"""
        buscar_url = self._mongo_db_access.find_one("correoUrl", {"url":url})
        if buscar_url is None:
            self._logger.debug("Url to save: %s", url)
            self._mongo_db_access.insert("correoUrl", mail_url)
            return 1
        else:
            self._logger.debug("No SAVE URL: %s", url)
            return 0

    def scrap_urls(self, limite=None):
        """ srap url using system of parameters and save this information in data base"""
        driver = self._seleniumaccess.open_selenium()
        self._logger.info("SCRAP_URLS")
        if not self._mongo_db_access.status():
            self._logger.error("Error Database Not Active")
            return None
        self.reprocess_mails()
        count = {}
        correos_url = self._mongo_db_access.find("correoUrl", \
                                  {"control":{"$exists":0}, "url":{"$exists":1}}, limite=limite)
        for correo_url in correos_url:
            try:
                control = self.scrap_url(correo_url, driver)
            except urllib2.URLError:
                control = "ERROR_URL"
            except WebDriverException:
                control = "ERROR_WEBDRIVER_ERROR"
            accumulate_dic(count, {control:1})
        self._logger.info("-- INFO -- URLs Analysed  %s", count)
        self._seleniumaccess.close_selenium(driver)
        return count

    def reprocess_mails(self):
        """ reprocess mails in status Error"""
        mails_reproces_error = self._mongo_db_access\
               .update_many("correoUrl", {"control":"ERROR"}, {"control":""}, is_set="unset")
        self._logger.info("Email_Error Reprocess: %s", mails_reproces_error.modified_count)
        mails_reproces_control = self._mongo_db_access\
               .update_many("correoUrl", {"control":""}, {"control":""}, is_set="unset")
        self._logger.info("Email_Blanck Reprocess: %d", mails_reproces_control.modified_count)

    def scrap_url(self, correo_url, driver):
        """  scrap one url retrieve the information locate """
        self._logger.info("SCRAP_URL: %s", correo_url["url"])
        data_of_scraping = self._analyzer_web_jobs.analyze(correo_url, driver)
        self._mongo_db_access.update_one("correoUrl", \
                         {"_id":correo_url["_id"]}, \
                         {"control":data_of_scraping.get("control", "ERROR"),\
                           "pagina":data_of_scraping.get("page", "None"),\
                           "urlOk":data_of_scraping.get("urlOk", "None")})
        if data_of_scraping.get("status", False):
            self.save_scraping(correo_url["_id"],\
                                  data_of_scraping.get("newCorreoUrl",\
                                  correo_url))
        return data_of_scraping.get("contol", "ERROR")

    def save_scraping(self, id_code, correo_url):
        """ save information into database """
        self._logger.debug("Save: ")
        self._logger.debug(correo_url)
        self._mongo_db_access.update_one("correoUrl", {"_id":id_code}, correo_url)

    def get_mongo_db_access(self):
        """Return method of mongodbaccess"""
        return self._mongo_db_access

    def get_mail_access(self):
        """Return method of mongodbaccess"""
        return self._mail_access

def build_mail_url(id_code, url):
    """ Build structure of correoUrl"""
    correo_url = {}
    correo_url["idCorreo"] = id_code
    correo_url["url"] = url
    correo_url["isSended"] = False
    correo_url["decision"] = ""
    correo_url["datetime"] = datetime.datetime.now()
    return correo_url

def accumulate_dic(dict_big, dict_to_add):
    """get two dicts and add first the data of second"""
    for key, value in dict_to_add.iteritems():
        dict_big[key] = dict_big.get(key, 0) + value
    return dict_big
