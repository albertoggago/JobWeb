from Logger import Logger
import json
import imaplib


#class for analize emails.
class MailAccess():

	_mailAccess = None

	def __init__(self,fileConfig):
		self.logger = Logger(self.__class__.__name__).get()
		configText = open(fileConfig,"r").read()
		config = json.loads(configText)

		self.logger.debug("acceso al Correo {0}".format(config["sslServer"]))
		self._mailAccess = imaplib.IMAP4_SSL(config["sslServer"])
		self.logger.debug("loggin correo: {0}".format(config["fromEmail"]))
		self._mailAccess.login(config["fromEmail"],config["pwdServer"])

	def status(self):
		return self._mailAccess

