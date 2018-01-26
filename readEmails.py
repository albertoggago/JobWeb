#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

from pymongo import MongoClient

import imaplib
import email
from email.header import decode_header
import re
import ipgetter
from email.mime.text import MIMEText
import smtplib

from pyvirtualdisplay import Display
from selenium import webdriver

#from lxml import html
#from lxml import etree
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
#import requests
#import string
#import nltk
#from nltk.collocations import *
#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
#from nltk.corpus import brown
#from nltk.probability import FreqDist
#import unicodedata
#import base64 

def recursivo (x):
	print x
	if not(x.text is None):
		print x.text.encode('utf-8')
	for z in x:
		recursivo(z)

def fechaDecreciente (datosFecha):
	datosFecha = datosFecha.lower()
	listaDF = datosFecha.split()
	listaDFN = [int(s) for s in datosFecha.split() if s.isdigit()]
	if len(listaDFN)>0:
		numeroDF = listaDFN[0]
	else:
		numeroDF = 0
	fecha = datetime.datetime.now()
	if ('dias' in listaDF or 'días' in listaDF or 'dia' in listaDF or 'día' in listaDF or 'day' in listaDF or 'days' in listaDF):
		numeroDelta = datetime.timedelta(days=numeroDF)
		fecha = fecha - numeroDelta
	elif ('mes' in listaDF or 'meses' in listaDF or 'month' in listaDF or 'months' in listaDF ):
		numeroDelta = datetime.timedelta(months=numeroDF)
		fecha = fecha - numeroDelta
	return fecha



def analizador (driver,secuencia=[{"tipo":"class","elemento":"xx"}],split=None, salida={"tipo":"text","initText":None}, vision=0):
	#split={"text"="-","n"=0}
	try:
	#fase localizador
		if vision==1:
			print "+++++++++++++++++++++++++++++++++++++++++++"
			print "                   modo Visual "
			print "+++++++++++++++++++++++++++++++++++++++++++"
		if vision==1:
			print "+ secuencia: {0}".format(secuencia)
			print "+ split:     {0}".format(split)
			print "+ salida:    {0}".format(salida)
			print "+++++++++++++++++++++++++++++++++++++++++++"
		driverTemp=driver 
		for ele in secuencia:
			if ele["tipo"] == "class":
				driverTemp = driverTemp.find_element_by_class_name(ele["elemento"])
			elif ele["tipo"] == "tag":
				driverTemp = driverTemp.find_element_by_tag_name(ele["elemento"])
		driverTemp = driverTemp.text.encode("utf-8")
		if vision==1:
			print "+ Despues de driver: {0}".format(driverTemp)
			print "+++++++++++++++++++++++++++++++++++++++++++"
	#fase split				
		if (split == None):
			splitTemp = driverTemp
		else:
			dataTemp = driverTemp.split(split["text"])

			if vision==1:
				print "+ Paso Split: {0}".format(dataTemp)
				print "+++++++++++++++++++++++++++++++++++++++++++"

			if split["initText"]== None:
				pos = 0
			else:
				pos = dataTemp.index(split["initText"])
			if len(dataTemp)> (split["n"]+pos):
				splitTemp = dataTemp[split["n"]+pos]
			else:
				splitTemp = ""
		if vision==1:
			print "+ Despues de split: {0}".format(splitTemp)
			print "+++++++++++++++++++++++++++++++++++++++++++"

	#fase salida
		if salida["tipo"]=="text":
			salida = splitTemp
		elif salida["tipo"]=="fecha-dif":
			salida = fechaDecreciente(splitTemp)
		elif salida["tipo"]=="fecha":
			if splitTemp =="":
				salida = datetime.datetime.now()
			else:
				salida = datetime.datetime.strptime(splitTemp,salida["formato"])

		if vision==1:
			print "+++++++++++++++++++++++++++++++++++++++++++"
			print "SALIDA: //{0}//".format(salida)
			print "+++++++++++++++++++++++++++++++++++++++++++"
		return salida
	except NoSuchElementException as e:
		print "+++++++++++++++++++++++++++++++++++++++++++"
		print "         ERROR: {0}".format(e)
		print "+++++++++++++++++++++++++++++++++++++++++++"

		return ""




class Posiciones:

	visible = False

	def __init__(self,name,visible):
		#client = MongoClient('localhost:27017', ssl=True, ssl_ca_certs='/home/alberto/datos/ssl/mongodb.pem', ssl_match_hostname=False)  
  		#client.the_database.authenticate("posiciones","posicionesX",source="admin")
  		url =  'mongodb://posiciones:1984ZuloPase@'
  		url += 'cluster0-shard-00-00-wapx6.mongodb.net:27017,'
  		url += 'cluster0-shard-00-01-wapx6.mongodb.net:27017,'
  		url += 'cluster0-shard-00-02-wapx6.mongodb.net:27017/'
  		url += 'posiciones?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
  		client = MongoClient(url)

  		
  		self.db = client[name]
  		self.param = self.db.correoUrl.find_one()

  		self.visible = visible
  		if self.param == None:
			print "base de datos parada o param no inicializado"
		else:
			print "-- INFO -- Conexion a base de datos OK"

	def buscar_elementos(self):
		#ojo ya borra solo
		#self.db.correo.remove()				
		print "-- INFO -- BUSCAR_CORREOS"
		sumaCorreos = 0;
		fromEmail = 'albertoggagocurro@albertoggago.es'
		sslServer = 'albertoggago.es'
		pwdServer= 'Gemaxana1973#'
		mail = imaplib.IMAP4_SSL(sslServer)
		mail.login(fromEmail,pwdServer)
		mail.list()
		mail.select("inbox")
		lista = mail.search(None,"ALL")[1][0].split()
		for ele in lista:
			correo = {}
			data = mail.fetch(ele, "(RFC822)")
			#print data[1][0][1]
			msg = email.message_from_string(data[1][0][1])
			msgFrom = msg.get_all("from",[])
			correo["From"]=msgFrom[0]
			subject = decode_header(msg.get_all("Subject",[])[0])[0][0]
			correo["Subject"]=subject
			urlsAll = []
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
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
			for x in urls:
				urlsAll.append(x)
			correo["texto"]=texto
			correo["urls"]=urlsAll
			correo["datetime"]=datetime.datetime.now()
			self.db.correo.insert(correo)
			sumaCorreos += 1			
			mail.store(ele, '+FLAGS', '\\Deleted')
		#mail.expunge()
		#mail.close()
 		mail.logout()
 		print "-- INFO -- Correos Leidos: {0:d}".format(sumaCorreos)
 		#parte dos recogemos la IP de la maquina y la enviamos por correo
 		IP = ipgetter.myip()
 		#print IP
 		ipOld = self.db.varios.find_one({"clave":"IP"})
 		if (ipOld["valor"]!=IP):
 			print IP
 			smtp_ssl_host = 'mail.albertoggago.es'
			smtp_ssl_port = 465
			username = fromEmail
			password = pwdServer
			sender = fromEmail
			targets = ['albertoggago@gmail.com']
			msg = MIMEText('IP: http://'+IP+":3000")
			msg['Subject'] = 'Nueva IP: '+IP
			msg['From'] = sender
			msg['To'] = ', '.join(targets)

			server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
			#server.set_debuglevel(2)
			server.login(username, password)
			server.sendmail(sender, targets, msg.as_string())
			#print msg.as_string()
			server.quit()
			self.db.varios.update_one({"clave":"IP"},{"$set":{'valor':IP}})

 			
			
	def buscar_urls(self):
		#ojo ya borra solo
		print "-- INFO -- BUSCAR_URLS"
		#self.db.correoUrl.remove()				
		#self.db.correo.update({},{"$unset":{"control":""}})
		sumaUrls = 0
		datos = self.db.correo.find({"control":{"$exists":0}},{"urls":1,"_id":1})
		for ele in datos:
			idCorreo = ele["_id"]
			for url in ele["urls"]:
				elemento = {}
				elemento["idCorreo"]= idCorreo
				elemento["url"]= url
				elemento["isSended"]= False
				elemento["decision"]= ""
				elemento["datetime"]=datetime.datetime.now()
				#buscar url
				buscarURL = self.db.correoUrl.find_one({"url":url})
				if buscarURL == None:
					self.db.correoUrl.insert(elemento)
				else:
					if self.visible!=1:
						print "no guardamos: {0}".format(url)
			self.db.correo.update_one({"_id":idCorreo},{"$set":{"control":"DONE"}})
			sumaUrls +=1
		print "-- INFO -- URLS Leidas: {0:d}".format(sumaUrls)
					
				
	def analizar_url2(self):
		#ojo ya borra solo
		print "-- INFO -- ANALIZAR_URL_2"
		#self.db.correoUrl.update_many({},{"$unset":{"control":""}})
		#self.db.correoUrl.update_many({"pagina":"recruitireland"},{"$unset":{"control":""}})
		self.db.correoUrl.update_many({"control":"ERROR"},{"$unset":{"control":""}})
		self.db.correoUrl.update_many({"control":""},{"$unset":{"control":""}})
		sumaUrl2 = 0
		sumaUrl2Ok = 0
		datos = self.db.correoUrl.find({"control":{"$exists":0},"url":{"$exists":1}})												
		if not self.visible:
			display = Display(visible=0, size=(1024, 768))
			display.start()
		driver = webdriver.Chrome()
		for ele in datos:
			idCorreoUrl = ele["_id"]
			urlOk = ""
			control= ""
			pagina= ""
			url = ele["url"]
			ver = self.visible

			if ("linkedin" in url ):
				pagina = "linkedin"
				urlOk = url
				driver.get(urlOk)

				if ver==1:
					print "***** PAGINA: {0}".format(pagina)
					print "***** URL: {0}".format(urlOk)
				
				titulo  = analizador(driver, secuencia=[{"tipo":"class","elemento":"title"}], vision=ver)
				donde   = analizador(driver, secuencia=[{"tipo":"class","elemento":"location"}], vision=ver)
				summary = analizador(driver, secuencia=[{"tipo":"class","elemento":"summary"}], vision=ver)
				fecha   = analizador(driver, secuencia=[{"tipo":"class","elemento":"posted"}], salida={"tipo":"fecha-dif"}, vision=ver)
				company = analizador(driver, secuencia=[{"tipo":"class","elemento":"company"}], vision=ver)

				if titulo in ["Destaca en lo que haces","Consultor - Científico de Datos - Scrum Master"]:
					titulo = ""

				if (company == "") and not (titulo ==""):
					company = "<NO DEFINIDA>"


				control = self.guardarInformacion(pagina,idCorreoUrl, urlOk, titulo,donde,summary, fecha, company)
				if control=="CORPUS":
					sumaUrl2Ok +=1


			if ("irishjobs" in url):
				pagina = "irishjob"
				urlOk = url[:url.find("=")]
				driver.get(urlOk)

				if ver==1:
					print "***** PAGINA: {0}".format(pagina)
					print "***** URL: {0}".format(urlOk)


				titulo  = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-description"},{"tipo":"tag","elemento":"h1"}], vision=ver)
				company = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-description"},{"tipo":"tag","elemento":"h2"}], vision=ver)
				donde   = analizador(driver, secuencia=[{"tipo":"class","elemento":"location"}], vision=ver)
 				if (titulo=="" and company == "" and donde == ""):
					summary = ""
				else:
					summary = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-details"}], vision=ver)

				if company == "":
					company = titulo


				if (titulo=="" and company == "" and donde == "" and summary==""):
					fecha = ""
				else:
					fecha   = analizador(driver, \
						      secuencia=[{"tipo":"class","elemento":"updated-time"}],split={"text":" ","n":1,"initText":None},\
					    	  salida={"tipo":"fecha","formato":"%d/%m/%Y"}, vision=ver)

				control = self.guardarInformacion(pagina,idCorreoUrl, urlOk, titulo,donde,summary, fecha, company)
				if control=="CORPUS":
					sumaUrl2Ok +=1


			if ("recruitireland" in url):
				pagina = "recruitireland"
				urlOk =string.replace(url,"=2E",".")
				urlOk =string.replace(urlOk,"=3D","=")
				driver.get(urlOk)

				if ver==1:
					print "***** PAGINA: {0}".format(pagina)
					print "***** URL: {0}".format(urlOk)

				titulo  = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-header"}],split={"text":"\n","n":0,"initText":None}, vision=ver)
				if  titulo =="THIS JOB HAS BEEN REMOVED BY THE ADVERTISER." :
					titulo  = ""
					company = ""
					donde   = ""
					summary = ""
					fecha   = ""
				else:
					donde   = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-info"}],\
					          split={"text":"\n","n":1,"initText":"Location:"}, vision=ver)
					summary = analizador(driver, secuencia=[{"tipo":"class","elemento":"generic-text"}], vision=ver)
					fecha   = analizador(driver, \
						      secuencia=[{"tipo":"class","elemento":"job-info"}],split={"text":"\n","n":1,"initText":"Posted on:"},\
						      salida={"tipo":"fecha","formato":"%d-%b-%Y"}, vision=ver)
					if (titulo == "" and donde == "" and summary == "" and fecha == ""):
						company = ""
					else:
						company = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-owner-description"},{"tipo":"tag","elemento":"a"}], vision=ver)

				control = self.guardarInformacion(pagina,idCorreoUrl, urlOk, titulo,donde,summary, fecha, company)

				if control=="CORPUS":
					sumaUrl2Ok +=1

			if ".jobs.ie" in url:
				pagina = "jobs.ie"
				urlOk =string.replace(url,"=3D","=")
				driver.get(urlOk)
				if ver==1:
					print "***** PAGINA: {0}".format(pagina)
					print "***** URL: {0}".format(urlOk)
				titulo  = analizador(driver, secuencia=[{"tipo":"class","elemento":"padding"},{"tipo":"tag","elemento":"h1"}],\
					                split={"text":"\xe2\x80\x93","initText":None,"n":0}, vision=ver)
				company = analizador(driver, secuencia=[{"tipo":"class","elemento":"sidebar"},{"tipo":"class","elemento":"acc-panel"}],\
									split={"text":"\n","initText":None,"n":1}, vision=ver)
				donde   = analizador(driver, secuencia=[{"tipo":"class","elemento":"c1"}],\
					                split={"text":"\n","initText":None,"n":1}, vision=ver)
				summary = analizador(driver, secuencia=[{"tipo":"class","elemento":"job-description"}], vision=ver)
				fecha   = analizador(driver, \
					      secuencia=[{"tipo":"class","elemento":"c2"}],split={"text":"\n","n":3,"initText":None},\
					      salida={"tipo":"fecha","formato":"%d-%m-%Y"}, vision=ver)
				
				control = self.guardarInformacion(pagina,idCorreoUrl, urlOk, titulo,donde,summary, fecha, company)
				if control=="CORPUS":
					sumaUrl2Ok +=1




			if ".monster." in url:					
				pagina = "monster.ie"
				urlOk =string.replace(url,"=3D","=")
				driver.get(urlOk)
				if ver==1:
					print "***** PAGINA: {0}".format(pagina)
					print "***** URL: {0}".format(urlOk)
				titulo  = analizador(driver, secuencia=[{"tipo":"class","elemento":"title"}],split={"text":" - ","n":0,"initText":None}, vision=ver)
				if (titulo=="Does your CV pass the 6-second test?") or ("visualizaciones" in titulo):
					titulo  = ""
					company = ""
					donde   = ""
					summary = ""
					fecha   = ""
				else:

					company = analizador(driver, secuencia=[{"tipo":"class","elemento":"title"}],split={"text":" - ","n":1,"initText":None}, vision=ver)
					donde   = analizador(driver, secuencia=[{"tipo":"class","elemento":"subtitle"}], vision=ver)
					summary = analizador(driver, secuencia=[{"tipo":"class","elemento":"details-content"}], vision=ver)
					fecha = analizador(driver, secuencia=[{"tipo":"class","elemento":"mux-job-summary"}],\
					                                    split={"text":"\n","n":1,"initText":"Posted"},
					                                    salida={"tipo":"fecha-dif"}, vision=ver)


				control = self.guardarInformacion(pagina,idCorreoUrl, urlOk, titulo,donde,summary, fecha, company)
				if control=="CORPUS":
					sumaUrl2Ok +=1


			#proceso OTRO
			lista = ["saongroup","mailchimp","www.w3.org",".png","123.ie",".jpg","hero.ie","www.facebook.com","twitter.com",\
			         "plus.google.com","youtube.com","maps.google.com","awstrack.me",".gif","/logos/","www.albertoggago.es",\
			         "register-cv","login","jobs-alerts","logs11.xiti.com","emltrk.com","www.w3c.org","www.lectiva.com", \
			         "infojobs","monster.secure.force.com","caliber","computerfutures","vodafone.ie","profitsflow","citywonders",\
			         "googleusercontent","googleapis"]
			otroInd = False
			for ele in lista:
				if ele in url:
					otroInd = True
			if otroInd:
				control = "OTRO"
				pagina ="N/D"



			if (control==""):
				if pagina == "":
					pagina ="N/D"
				if urlOk =="":
					urlOk = url
				print "** ERROR************************************************************************" 
				print "URL ERRONEA: "+urlOk
				print "** ERROR************************************************************************" 
				control = "ERROR"

			sumaUrl2 +=1

			self.db.correoUrl.update_one({"_id":idCorreoUrl},{"$set":{"control":control,"pagina":pagina}})
		print "-- INFO -- URLs Analizadas : {0:d}, procesadas OK: {1:d}".format(sumaUrl2,sumaUrl2Ok)
		driver.close()

	def guardarInformacion (self, pagina,correoUrl, urlOk, titulo,donde,summary, fecha, company):
		if not (titulo=="" or donde == "" or summary == "" or fecha =="" or company == ""):
			actualiza = {}
			actualiza["urlOk"]=urlOk
			actualiza["titulo"]=titulo
			actualiza["donde"]=donde
			actualiza["summary"]=summary
			actualiza["fecha"]=fecha
			actualiza["company"]=company

			self.db.correoUrl.update_one({"_id":correoUrl},{"$set":actualiza})
			return "CORPUS"
		elif (titulo=="" and donde == "" and summary == "" and fecha =="" and company == ""):
			print "++++++++++++++++++++++++++++++++++++++"
			print "               SEARCH "
			print "++++++++++++++++++++++++++++++++++++++"
			print "urlOk  :  //{0}".format(urlOk)
			return "SEARCH"
		else: 
			print "**********************************"
			print "               ERROR "
			print "**********************************"
			print "pagina  {0}".format(pagina)
			print "**********************************"
			print "urlOk  :  //{0}".format(urlOk)
			print "titulo :  //{0}//".format(titulo)
			print "donde  :  //{0}//".format(donde)
			print "summary:  //{0}//".format(summary[:20])
			print "fecha  :  //{0}//".format(fecha)
			print "company:  //{0}//".format(company)
			print "**********************************"
			return "ERROR"

if __name__ == '__main__':
	param_visible = True if len(sys.argv)>1 else False
	print "## INFO ## Inicio: {0}".format(datetime.datetime.now())
	posiciones = Posiciones("posiciones",param_visible)
	posiciones.buscar_elementos()
	posiciones.buscar_urls()
	posiciones.analizar_url2()
	print "## INFO ## fin: {0}".format(datetime.datetime.now())

