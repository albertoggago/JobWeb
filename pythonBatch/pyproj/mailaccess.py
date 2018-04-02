#!/usr/bin/env pythoObjectn

""" Only a Class MailAccess"""

import json
import imaplib
import email
from email.header import decode_header
import re
import datetime
import base64
from pyproj.logger import Logger

#class for analize emails.
class MailAccess(object):
    """ Create un access to Mail to read Emails and format Text"""

    _mail = None

    def __init__(self, fileConfig, levelLog):
        self.logger = Logger(self.__class__.__name__, levelLog).get()
        config_text = open(fileConfig, "r").read()
        self._config = json.loads(config_text)
        self.login()

    def login(self):
        """ do loggin using informaction of file configuration"""
        try:
            self.logger.debug("acceso al Correo %s", self._config["sslServer"])
            self._mail = imaplib.IMAP4_SSL(self._config["sslServer"])
            self.logger.info("loggin correo: %s", self._config["fromEmail"])
            self._mail.login(self._config["fromEmail"], self._config["pwdServer"])
            self.logger.info("conected Data Base")
            return True
        except imaplib.IMAP4.error:
            self.logger.error("error loggin eMail")
            return None

    def logout(self):
        """loggoff of mail Server"""
        try:
            self._mail.logout()
            self.logger.info("eMail Stoped")
            return True
        except AttributeError:
            self.logger.error("Logout email")
            return None

    def status(self):
        """determine id mail server is connect or not"""
        try:
            result = self._mail.namespace()
            self.logger.debug("Status email: %s", result)
            return result[0] == "OK"
        except imaplib.IMAP4.error:
            self.logger.info("Email close or not correctly open")
            return False

    def search_mails(self, path_email):
        """finding emails and return cursor all emails"""
        try:
            self.logger.info("Search Mails")
            self.logger.debug("Access to mails of %s", path_email)
            self._mail.list()
            self._mail.select("inbox")
            return self._mail.search(None, "ALL")[1][0].split()
        except imaplib.IMAP4.readonly as error:
            self.logger.error("ReadOnly Access to mails: %s", error.args)
            return None
        except imaplib.IMAP4.abort as error:
            self.logger.error("Abort Access to mails: %s", error.args)
            return None
        except imaplib.IMAP4.error as error:
            self.logger.error("Error Access to mails: %s", error.args)
            return None
        else:
            self.logger.error("Error Access to mails, Undefined")
            return None

    def store(self, email_enter):
        """store information to Delete"""
        try:
            self.logger.info("Store email")
            self._mail.store(email_enter, '+FLAGS', '\\Deleted')
            return True
        except imaplib.IMAP4.readonly as error:
            self.logger.error("ReadOnly Access to mails: %s", error.args)
            return None
        except imaplib.IMAP4.abort as error:
            self.logger.error("Abort Access to mails:  %s", error.args)
            return None
        except imaplib.IMAP4.error as error:
            self.logger.error("Error Access to mails:  %s", error.args)
            return None
        else:
            self.logger.error("Error Access to mails, Undefined")
            return None

    def clean(self):
        """clean information of DELETED"""
        try:
            self.logger.info("Clean email")
            self._mail.expunge()
            self._mail.close()
            return True
        except imaplib.IMAP4.error:
            self.logger.error("Error Clean eMails")
            return None

    def get(self, emailenter):
        """Get string information of email"""
        try:
            self.logger.info("find mail")
            data = self._mail.fetch(emailenter, "(RFC822)")
            return email.message_from_string(data[1][0][1])
        except imaplib.IMAP4.error:
            self.logger.error("Error Get eMails")
            return None

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
            self.logger.error("Error compose Mails")
            return None

    def decode_header(self, msg):
        """decode header with base64 or not"""
        try:
            return decode_header(msg.get_all("Subject", [])[0])[0][0]
        except imaplib.IMAP4.error:
            self.logger.error("Error DecodeHeader eMails")
            return None

    def get_body_mail(self, msg):
        """GEt body of mail"""
        texto = ""
        for part in msg.walk():
            texto += " " + self.decode_text(part, msg['Content-Transfer-Encoding'])
        return texto

    def decode_text(self, part, encode):
        """ Decode text to base64 if s base64"""
        self.logger.debug("Decode_text")
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        if (ctype == 'text/plain' or ctype == 'text/html') and 'attachment' not in cdispo:
            payload = part.get_payload()
            texto = base64.decodestring(payload) if encode == "base64" else payload
            return texto
        else:
            self.logger.warn("Text without information to process")
            return ""
