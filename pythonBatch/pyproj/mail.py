#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" file include class ReadAndAnalyse """

import re
import imaplib
import datetime
from email.header import decode_header
import base64


class Mail(object):
    """ Class for read and analize information, combine class"""
    _logger = None
    _mongo_db_access = None
    _mail_json = None

    def __init__(self, config, mongodbaccess, msg):
        self._logger = config.get_logger(self.__class__.__name__)
        self._mongo_db_access = mongodbaccess
        self._mail_json = self.compose_mail_json(msg)

    def compose_mail_json(self, msg):
        """Compose information from email return a json with from, subject,texto,urls, datetime"""
        correo = {}
        try:
            correo["From"] = msg.get_all("from", [])[0]
            correo["Subject"] = self.decode_header(msg)
            texto = self.get_body_mail(msg)
            texto = re.sub("=\r\n", "", texto)
            urls_all = []
            urls = re.findall(\
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                   texto)
            for url in urls:
                urls_all.append(url)

            correo["texto"] = texto
            correo["urls"] = urls_all
            correo["datetime"] = datetime.datetime.now()

            return correo
        except imaplib.IMAP4.error:
            self._logger.error("Error compose Mails")
            return None

    def decode_header(self, msg):
        """decode header with base64 or not"""
        try:
            return decode_header(msg.get_all("Subject", [])[0])[0][0]
        except imaplib.IMAP4.error:
            self._logger.error("Error DecodeHeader eMails")
            return None

    def get_body_mail(self, msg):
        """GEt body of mail"""
        texto = ""
        for part in msg.walk():
            texto += " " + self.decode_text(part, msg['Content-Transfer-Encoding'])
        return texto

    def decode_text(self, part, encode):
        """ Decode text to base64 if s base64"""
        self._logger.debug("Decode_text")
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        if (ctype == 'text/plain' or ctype == 'text/html') and 'attachment' not in cdispo:
            payload = part.get_payload()
            texto = base64.decodestring(payload) if encode == "base64" else payload
        else:
            self._logger.warn("Text without information to process")
            texto = ""
        return texto

    def is_ok(self):
        """ determine if process """
        return self._mail_json is not None

    def get_control(self):
        """ get control """
        if self.is_ok():
            return self._mail_json.get("control", "")

    def get_urls(self):
        """ get url """
        if self.is_ok():
            return self._mail_json.get("urls", "")

    def get_datetime(self):
        """ get datetime """
        if self.is_ok():
            return self._mail_json.get("datetime", "")

    def save_mail(self):
        "save in database "
        self._mongo_db_access.insert("correo", self._mail_json)
