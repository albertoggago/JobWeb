#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique FindRepeated """

import datetime
from difflib import SequenceMatcher

from pyproj.logger import Logger
from pyproj.mongodbaccess import MongoDBAccess


METHODS_TO_FIND = [{"name":"summary", "weight":6.0},
                   {"name":"donde", "weight":2.0},
                   {"name":"company", "weight":2.0},
                   {"name":"titulo", "weight":1.0}]
LIMIT_DIAS = 15.0

class FindRepeated(object):
    """ Analize all text and looking for repeated """
    logger = None
    mongo_db_access = None
    ratio_bottom = None

    def __init__(self, fileConfig, levelLog, ratio_accept=1.0):
        self.ratio_bottom = ratio_accept
        self.logger = Logger(self.__class__.__name__, levelLog).get()
        self.mongo_db_access = MongoDBAccess(fileConfig, levelLog)
        self.logger.info("Inicio: %s", datetime.datetime.now())

    def finding_open_jobs(self, delete_database):
        """ find all open jobs for determinate if are repeated """
        delete_database = True if delete_database is True else False
        self.logger.info("Access all elements without response in database")
        count_jobs = 0
        report = {}
        report["lines"] = []
        jobs_finding = self.mongo_db_access\
               .find("correoUrl", {"control":"CORPUS", "decision":""})
        for job_finding in jobs_finding:
            count_jobs += 1
            line_report = self.analyse_job(job_finding, delete_database)
            report["lines"].append(line_report)
        report["count"] = count_jobs
        return report

    def analyse_job(self, job, delete_database):
        """ analyse a job determinate """
        _id = job.get("_id", "")
        self.logger.info("analize job %s", _id)
        #step one get same title
        title = job.get("titulo", "")
        self.logger.info("title: %s", title)
        list_similar = []
        list_similar.append({"ID_ORIGIN":_id, "TITLE: ":job.get("titulo", "")})
        jobs_similar = self.mongo_db_access\
               .find("correoUrl", {"control":"CORPUS", "titulo":title, "_id":{"$nin":[_id]}},\
                   sort={"fecha":-1})
        for job_similar in jobs_similar:
            info_similar = self.compare_similar(job, job_similar)
            list_similar.append(info_similar)
            equals = self.calculate_equals(info_similar)
            if equals:
                if delete_database:
                    self.delete_logic_job(job)
                list_similar.append({"status":"delete"})
                return list_similar
        #return list_similar
        return []

    def compare_similar(self, job_origin, job_compare):
        """ compare two similars jobs"""
        _id_compare = job_compare.get("_id", "")
        self.logger.info("_id simmilar: %s", _id_compare)
        comparation = {}
        #comparation["_id_origin"] = _id_origin
        comparation["_id_similar"] = _id_compare
        time_origin = job_origin.get("fecha", datetime.datetime.now())
        time_compare = job_compare.get("fecha", datetime.datetime.now())
        comparation["dif_dias"] = (time_origin - time_compare).days
        for method_complete in METHODS_TO_FIND:
            method = method_complete.get("name", "x")
            sequence_matcher = SequenceMatcher(None, job_origin.get(method, "aaaaa"),\
                                                    job_compare.get(method, "bbbbb"))
            comparation["ratio_"+method] = sequence_matcher.ratio()
        return comparation

    def calculate_equals(self, data):
        """ this method determinate the level of ranking for delete something"""
        self.logger.info("calculate equals")
        # In this moment 0 days and 1 in all ratios, calculate a number with all ratios.
        # days lineal 7 day less tha 7 days nothing
        # methos value
        dif_dias = data.get("dif_dias", 99)
        dif_dias = 99 if dif_dias < 0 else dif_dias
        var_count = 1.0
        ratio = -10.0 if dif_dias > LIMIT_DIAS else 1 - dif_dias / LIMIT_DIAS
        for method in METHODS_TO_FIND:
            weight_method = method.get("weight", 1)
            ratio += data.get("ratio_"+method.get("name", "xx"), 0) * weight_method
            var_count += weight_method
        return True if ratio / var_count >= self.ratio_bottom else False


    def delete_logic_job(self, job):
        """ analyse a job determinate """
        _id = job.get("_id", "")
        self.logger.info("delete Logic job: %s", _id)
        if _id != "":
            return self.mongo_db_access\
                   .update_one("correoUrl", {"_id":_id}, {"control":"DELETED"})
        return False
