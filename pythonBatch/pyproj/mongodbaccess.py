#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Only a Class MongoDBAccess"""

import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from pyproj.logger import Logger

class MongoDBAccess(object):
    """Class to access to MongoDB allow access and review connections"""

    db_access = None
    _client = None

    def __init__(self, fileName, levelLog):
        """Need a file where has got all parameters and level of Loggin"""
        self.logger = Logger(self.__class__.__name__, levelLog).get()
        self.logger.setLevel('INFO')
        if fileName:
            config_text = open(fileName, "r").read()
            config = json.loads(config_text)
        else:
            config = {}
            config["url"] = "localhost:27017"
            config["nameDB"] = "temp"

        try:
            self.logger.debug(config["url"])
            self._client = MongoClient(config["url"])
            self.db_access = self._client[config["nameDB"]]
            self.logger.info("-- INFO -- DATA BASE CONECT OK")
        except ConnectionFailure:
            self.logger.error("ConnectionFailure")
        except OperationFailure:
            self.logger.error("Authentication failure")

    def status(self):
        """Determinate True is connect or False if is not connect"""
        try:
            self.logger.debug(self._client.server_info())
            return True
        except ConnectionFailure:
            self.logger.error("ConnectionFailure")
            return False
        except OperationFailure:
            self.logger.error("Authentication failure")
            return False

    def find_one(self, collection, query):
        """Find one element only return a json element"""
        if self.status():
            self.logger.info("Access to collection: %s, query %s", collection, query)
            return self.db_access[collection].find_one(query)
        else:
            self.logger.error("Database Not INIT Find_one")
            return None

    def find(self, collection, query, sort=None, limite=None):
        """Find several elements is a cursor, atention for line in cursor is better"""
        if self.status():
            self.logger.info("Access to collection Multi: %s, query: %s, sort: %s, limit: %s",\
                collection, query, sort, limite)
            limite = 0 if limite is None else limite
            sort = None if sort is None else sort.items()
            return self.db_access[collection].find(query, sort=sort, limit=limite)
        else:
            self.logger.error("Database Not INIT Find")
            return None

    def update_one(self, collection, query, change, is_set="set"):
        """Update One return status of update"""
        if self.status():
            self.logger.info("Modify collection: %s, query: %s, modify: %s, set: %s",\
                collection, query, change, is_set)
            setdollar = "$"+is_set
            return self.db_access[collection].update_one(query, {setdollar:change})
        else:
            self.logger.error("Database Not INIT Update_one")
            return None

    def update_many(self, collection, query, change, is_set="set"):
        """Update Many return status of update"""
        if self.status():
            self.logger.info("Modify Many collection: %s, query: %s, modify: %s, set: %s",\
                collection, query, change, is_set)
            setdollar = "$"+is_set
            return self.db_access[collection].update_many(query, {setdollar:change})
        else:
            self.logger.error("Database Not INIT Update_one")
            return None

    def insert(self, collection, element):
        """Insert return status of insert"""
        if self.status():
            self.logger.debug("Insert collection: %s, data: %s", collection, element)
            return self.db_access[collection].insert(element)
        else:
            self.logger.error("Database Not INIT Find")
            return None

    def delete_one(self, collection, element):
        """delete One return status of delete"""
        if self.status():
            self.logger.info("Remove collection: %s, data: %s", collection, element)
            return self.db_access[collection].delete_one(element)
        else:
            self.logger.error("Database Not INIT Find")
            return None

    def delete_many(self, collection, element):
        """delete return status of delete"""
        if self.status():
            self.logger.info("Remove collection: %s, data: %s", collection, element)
            return self.db_access[collection].delete_many(element)
        else:
            self.logger.error("Database Not INIT Find")
            return None

    def drop(self, collection):
        """Drop a collection return status of drop"""
        if self.status():
            self.logger.info("Drop collection: %s", collection)
            return self.db_access[collection].drop()
        else:
            self.logger.error("Database Not INIT Find")
            return None
