from Logger import Logger
import json
import imaplib
import email
from email.header import decode_header
import re

#class for analize emails.
class MailAccess():

	_mail = None
	status = False

	def __init__(self,fileConfig):
		self.logger = Logger(self.__class__.__name__).get()
		configText = open(fileConfig,"r").read()
		self._config = json.loads(configText)
		self.login()

			 
	def searchMails(self,pathEmail):
		if self.status:
			self.logger.error("Access to mails of {0}".format(pathEmail))
			self._mail.list()
			self._mail.select("inbox")
			return self._mail.search(None,"ALL")[1][0].split()
		else:
			self.logger.error("eMail Stoped")
			return None
			
	def searchMails(self,pathEmail):
		if self.status:
			self.logger.error("Access to mails of {0}".format(pathEmail))
			self._mail.list()
			self._mail.select("inbox")
			return self._mail.search(None,"ALL")[1][0].split()
		else:
			self.logger.error("eMail Stoped")
			return None

	def login(self):
		if self.status:
			self.logger.error("eMail already Open")
			return None
		else:
			try:
				self.logger.debug("acceso al Correo {0}".format(self._config["sslServer"]))
				self._mail = imaplib.IMAP4_SSL(self._config["sslServer"])
				self.logger.debug("loggin correo: {0}".format(self._config["fromEmail"]))
				self._mail.login(self._config["fromEmail"],self._config["pwdServer"])
				self.status = True
				return True
			except imaplib.IMAP4.error:
				self.logger.error("error loggin eMail")
				self.status = False
				return None

	def store(self, emailEnter):
		if self.status:
			self.logger.error("Store email")
			self._mail.store(emailEnter, '+FLAGS', '\\Deleted')
			self.status = False
			return True
		else:
			self.logger.error("eMail Stoped")
			return None

	def logout(self):
		if self.status:
			self.logger.error("Logout email")
			self._mail.logout()
			self.status = False
			return True
		else:
			self.logger.error("eMail Stoped")
			return None

	def clean(self):
		if self.status:
			self.logger.error("Clean email")
			self._mail.expunge()
			self._mail.close()
			return True
		else:
			self.logger.error("eMail Stoped")
			return None

	def get(self, emailenter):
		if self.status:
			self.logger.error("find mail")
			data =  self._mail.fetch(emailenter, "(RFC822)")
			return email.message_from_string(data[1][0][1])
			
		else:
			self.logger.error("eMail Stoped")
			return None

	def decodeHeader(self,msg):
		return decode_header(msg.get_all("Subject",[])[0])[0][0]


	def composeMailJson(self,msg):
		correo = {}
		correo["From"]    = msg.get_all("from",[])[0]
		correo["Subject"] = self.decodeHeader(msg) 

		texto = ""
		for part in msg.walk():
			ctype = part.get_content_type()
			cdispo = str(part.get('Content-Disposition'))
			if (ctype == 'text/plain' or ctype == 'text/html' )and 'attachment' not in cdispo:
				enc = msg['Content-Transfer-Encoding']
				texto = texto+" "+part.get_payload()
				if enc =="base64":
					texto = base64.decodestring(texto)
		texto = re.sub("=\r\n","",texto)
		urlsAll = []
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
		for x in urls:
			urlsAll.append(x)
		correo["texto"]=texto
		correo["urls"]=urlsAll
		return correo
