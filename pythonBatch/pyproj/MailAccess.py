from Logger import Logger
import json
import imaplib
import email
from email.header import decode_header
import re
import datetime


#class for analize emails.
class MailAccess():

	_mail = None

	def __init__(self,fileConfig):
		self.logger = Logger(self.__class__.__name__).get()
		configText = open(fileConfig,"r").read()
		self._config = json.loads(configText)
		self.login()

	def login(self):
		try:
			self.logger.debug("acceso al Correo {0}".format(self._config["sslServer"]))
			self._mail = imaplib.IMAP4_SSL(self._config["sslServer"])
			self.logger.info("loggin correo: {0}".format(self._config["fromEmail"]))
			self._mail.login(self._config["fromEmail"],self._config["pwdServer"])
			self.logger.info("conected Data Base")
			return True
		except imaplib.IMAP4.error:
			self.logger.error("error loggin eMail")
			return None

	def logout(self):
		try:
			self._mail.logout()
			self.logger.info("eMail Stoped")
			return True
		except AttributeError:
			self.logger.error("Logout email")
			return None

	def status(self):
		try:
			result = self._mail.namespace()
			self.logger.debug("Status email: {0}".format(result))
			return result[0]=="OK"
		except:
			self.logger.info("Email close or not correctly open")
			return False
		

			 
	def searchMails(self,pathEmail):
		try:
			self.logger.info("Search Mails")
			self.logger.debug("Access to mails of {0}".format(pathEmail))
			self._mail.list()
			self._mail.select("inbox")
			return self._mail.search(None, "ALL")[1][0].split()
		except imaplib.IMAP4.error as e:
			self.logger.error("Error Access to mails: {0}".format(e.args))
			return None
		except imaplib.IMAP4.abort as e:
			self.logger.error("Abort Access to mails: {0}".format(e.args))
			return None
		except imaplib.IMAP4.readonly as e:
			self.logger.error("ReadOnly Access to mails: {0}".format(e.args))
			return None
		else:
			self.logger.error("Error Access to mails, Undefined")
			return None
			
	def store(self, emailEnter):
		try:
			self.logger.info("Store email")
			self._mail.store(emailEnter, '+FLAGS', '\\Deleted')
			return True
		except imaplib.IMAP4.error as e:
			self.logger.error("Error Access to mails: {0}".format(e.args))
			return None
		except imaplib.IMAP4.abort as e:
			self.logger.error("Abort Access to mails: {0}".format(e.args))
			return None
		except imaplib.IMAP4.readonly as se:
			self.logger.error("ReadOnly Access to mails: {0}".format(e.args))
			return None
		else:
			self.logger.error("Error Access to mails, Undefined")
			return None

	def clean(self):
		try:
			self.logger.info("Clean email")
			self._mail.expunge()
			self._mail.close()
			return True
		except:
			self.logger.error("Error Clean eMails")
			return None

	def get(self, emailenter):
 		try:
			self.logger.info("find mail")
			data =  self._mail.fetch(emailenter, "(RFC822)")
			return email.message_from_string(data[1][0][1])
		except:
			self.logger.error("Error Get eMails")
			return None
	
	def composeMailJson(self,msg):
		correo = {}
		try:
			correo["From"]    = msg.get_all("from",[])[0]
			correo["Subject"] = self.decodeHeader(msg)
			texto = self.getBodyMail(msg)
			texto = re.sub("=\r\n","",texto)
			urlsAll = []
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
			for x in urls:
				urlsAll.append(x)
			
			correo["texto"]=texto
			correo["urls"]=urlsAll
			correo["datetime"]=datetime.datetime.now()
		
			return correo
		except:
			self.logger.error("Error compose Mails")
			return None

	def decodeHeader(self,msg):
 		try:
			return decode_header(msg.get_all("Subject",[])[0])[0][0]
		except:
			self.logger.error("Error DecodeHeader eMails")
			return None

	def getBodyMail (self, msg):
		texto = ""
		for part in msg.walk():
			texto += " " + self.decodeText(part,msg['Content-Transfer-Encoding'])
		return texto
				
	def decodeText (self,part,encode):
		ctype = part.get_content_type()
		cdispo = str(part.get('Content-Disposition'))
		if (ctype == 'text/plain' or ctype == 'text/html' ) and 'attachment' not in cdispo:
			texto = base64.decodestring(texto) if encode =="base64" else part.get_payload()
			return texto
		else:
			self.logger.warn("Text without information to process")
			return ""
