#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" file include class ReadAndAnalyse """

import datetime
import json

from pyproj.logger import Logger
from pyproj.mongodbaccess import MongoDBAccess
from pyproj.mailaccess import MailAccess
from pyproj.analyzerwebjobs import AnalyzerWebJobs



class ReadAndAnalyse(object):
    """ Class for read and analize information, combine class"""
    logger = None
    mongo_db_access = None
    mail_access = None
    analyzer_web_jobs = None
    env = None

    def __init__(self, fileConfig, levelLog):
        self.logger = Logger(self.__class__.__name__, levelLog).get()
        self.mongo_db_access = MongoDBAccess(fileConfig, levelLog)
        self.mail_access = MailAccess(fileConfig, levelLog)
        config_text = open(fileConfig, "r").read()
        allconfig = json.loads(config_text)
        config = allconfig.get("webPagesDef", None)
        self.env = allconfig.get("env", "DEV")
        self.analyzer_web_jobs = AnalyzerWebJobs(config, levelLog)

        self.logger.info("Inicio: %s", datetime.datetime.now())

    def finding_mails(self):
        """Module for looking for emails return emails finding """
        self.logger.info("find_emails")
        if not self.mail_access.status():
            self.logger.error("Error mail Not Active")
            return None
        if not self.mongo_db_access.status():
            self.logger.error("Error Database Not Active")
            return None

        count_emails = 0
        list_emails = self.mail_access.search_mails("inbox")

        for ele in list_emails:
            mail = self.mail_access.compose_mail_json(self.mail_access.get(ele))
            if mail is None:
                self.logger.error("Mail generate wrong")
            else:
                self.logger.debug("Insert into Control")
                self.logger.debug("control: %s", mail.get("control"))
                self.logger.debug("urls: %s", mail.get("urls"))
                self.logger.debug("datetime: %s", mail.get("datetime"))
                self.mongo_db_access.insert("correo", mail)
                count_emails += 1
                self.mail_access.store(ele)

        if self.env == "PRODUCTION":
            self.logger.info("CLEAN EMAIL")
            self.mail_access.clean()
        self.mail_access.logout()
        self.logger.info("emails reads : %s", count_emails)
        return count_emails

    def finding_urls(self):
        """ Find urls inside of mails saved """
        self.logger.info("FINDING_URLS")
        if not self.mongo_db_access.status():
            self.logger.error("Error Database Not Active")
            return None

        count_urls = 0
        mails = self.mongo_db_access.find("correo", {"control":{"$exists":0}}, \
                                              sort={"urls":1, "_id":1})
        for mail in mails:
            for url in mail.get("urls", []):
                correo_url = build_mail_url(mail["_id"], url)
                count_urls += self.review_mail_url(correo_url, url)
            self.mongo_db_access.update_one("correo", {"_id":mail["_id"]}, {"control":"DONE"})
        self.logger.info("URLS read: %s", count_urls)
        return count_urls

    def review_mail_url(self, mail_url, url):
        """ review mail url looking for in dabase and when not exist save"""
        buscar_url = self.mongo_db_access.find_one("correoUrl", {"url":url})
        if buscar_url is None:
            self.logger.debug("Url to save: %s", url)
            self.mongo_db_access.insert("correoUrl", mail_url)
            return 1
        else:
            self.logger.debug("No SAVE URL: %s", url)
            return 0

    def scrap_urls(self, limite=None):
        """ srap url using system of parameters and save this information in data base"""
        self.analyzer_web_jobs.open_selenium()
        self.logger.info("SCRAP_URLS")
        if not self.mongo_db_access.status():
            self.logger.error("Error Database Not Active")
            return None
        self.reprocess_mails()
        count = {}
        correos_url = self.mongo_db_access.find("correoUrl", \
                                  {"control":{"$exists":0}, "url":{"$exists":1}}, limite=limite)
        for correo_url in correos_url:
            control = self.scrap_url(correo_url)
            if count.get(control, 0) == 0:
                count[control] = 1
            else:
                count[control] += 1

        self.logger.info("-- INFO -- URLs Analysed  %s", count)
        self.analyzer_web_jobs.close_selenium()
        return count

    def reprocess_mails(self):
        """ reprocess mails in status Error"""
        mails_reproces_error = self.mongo_db_access\
               .update_many("correoUrl", {"control":"ERROR"}, {"control":""}, is_set="unset")
        self.logger.info("Email_Error Reprocess: %s", mails_reproces_error.modified_count)
        mails_reproces_control = self.mongo_db_access\
               .update_many("correoUrl", {"control":""}, {"control":""}, is_set="unset")
        self.logger.info("Email_Blanck Reprocess: %d", mails_reproces_control.modified_count)

    def scrap_url(self, correo_url):
        """  scrap one url retrieve the information locate """
        self.logger.info("SCRAP_URL: %s", correo_url["url"])
        data_of_scraping = self.analyzer_web_jobs.analyze(correo_url)
        self.mongo_db_access.update_one("correoUrl", \
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
        self.logger.debug("Save: ")
        self.logger.debug(correo_url)
        self.mongo_db_access.update_one("correoUrl", {"_id":id_code}, correo_url)

def build_mail_url(id_code, url):
    """ Build structure of correoUrl"""
    correo_url = {}
    correo_url["idCorreo"] = id_code
    correo_url["url"] = url
    correo_url["isSended"] = False
    correo_url["decision"] = ""
    correo_url["datetime"] = datetime.datetime.now()
    return correo_url
