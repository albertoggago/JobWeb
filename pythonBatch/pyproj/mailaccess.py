#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Only a Class MailAccess"""

import imaplib
import email
from socket import gaierror

#class for analize emails.
class MailAccess(object):
    """ Create un access to Mail to read Emails and format Text"""

    _mail = None
    _config_param = None
    _logger = None

    def __init__(self, config):
        self._config_param = config.get_config_param()
        self._logger = config.get_logger(self.__class__.__name__)
        self.login()


    def login(self):
        """ do loggin using informaction of file configuration"""
        try:
            self._logger.debug("acceso al Correo %s",\
                              self._config_param.get("sslServer", "ERROR sslServer"))
            self._mail = imaplib.IMAP4_SSL(self._config_param.get("sslServer", ""))
            self._logger.info("loggin correo: %s", self._config_param.get("fromEmail", ""))
            self._mail.login(self._config_param.get("fromEmail", ""), \
                             self._config_param.get("pwdServer", ""))
            self._logger.info("conected Data Base")
            return True
        except imaplib.IMAP4.error:
            self._logger.error("error loggin eMail")
            return None
        except gaierror:
            self._logger.error("error loggin eMail")
            return None

    def logout(self):
        """loggoff of mail Server"""
        try:
            self._mail.logout()
            self._logger.info("eMail Stoped")
            return True
        except AttributeError:
            self._logger.error("Logout email")
            return None

    def status(self):
        """determine id mail server is connect or not"""
        if self._mail is None:
            return False
        try:
            result = self._mail.namespace()
            self._logger.debug("Status email: %s", result)
            return result[0] == "OK"
        except imaplib.IMAP4.error:
            self._logger.info("Email close or not correctly open")
            return False

    def search_mails(self, path_email):
        """finding emails and return cursor all emails"""
        try:
            self._logger.info("Search Mails")
            self._logger.debug("Access to mails of %s", path_email)
            self._mail.list()
            self._mail.select("inbox")
            return self._mail.search(None, "ALL")[1][0].split()
        except imaplib.IMAP4.readonly as error:
            self._logger.error("ReadOnly Access to mails: %s", error.args)
            return None
        except imaplib.IMAP4.abort as error:
            self._logger.error("Abort Access to mails: %s", error.args)
            return None
        except imaplib.IMAP4.error as error:
            self._logger.error("Error Access to mails: %s", error.args)
            return None
        else:
            self._logger.error("Error Access to mails, Undefined")
            return None

    def store(self, email_enter):
        """store information to Delete"""
        try:
            self._logger.info("Store email")
            self._mail.store(email_enter, '+FLAGS', '\\Deleted')
            return True
        except imaplib.IMAP4.readonly as error:
            self._logger.error("ReadOnly Access to mails: %s", error.args)
            return None
        except imaplib.IMAP4.abort as error:
            self._logger.error("Abort Access to mails:  %s", error.args)
            return None
        except imaplib.IMAP4.error as error:
            self._logger.error("Error Access to mails:  %s", error.args)
            return None
        else:
            self._logger.error("Error Access to mails, Undefined")
            return None

    def clean(self):
        """clean information of DELETED"""
        try:
            self._logger.info("Clean email")
            self._mail.expunge()
            self._mail.close()
            return True
        except imaplib.IMAP4.error:
            self._logger.error("Error Clean eMails")
            return None

    def get(self, emailenter):
        """Get string information of email"""
        try:
            self._logger.info("find mail")
            data = self._mail.fetch(emailenter, "(RFC822)")
            return email.message_from_string(data[1][0][1])
        except imaplib.IMAP4.error:
            self._logger.error("Error Get eMails")
            return None

