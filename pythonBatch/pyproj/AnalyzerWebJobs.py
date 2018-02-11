#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import datetime

#import string
#from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from selenium import webdriver

#own classes
from Logger import Logger


class AnalyzerWebJobs:

	config = None
	logger = None
	driver = None

	def __init__(self,config,visible):
		self.logger    = Logger(self.__class__.__name__).get()
		self.config    = config
		
		if not visible:
			display = Display(visible=0, size=(1024, 768))
			display.start()
		self.driver = webdriver.Chrome()

	def analyze(self,correoUrl):
		print correoUrl
		print self.config
		self.driver.get(correoUrl["url"])

		print self.driver
		
		#determinate page
		#finding data
		#review correct page
		#build information
		return {} 

	def closeSelenium(self):
		self.driver.close()



	
	def pending(self, correoUrl):
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

			self.mongoDBAccess.update_one("correoUrl",{"_id":idCorreoUrl},{"control":control,"pagina":pagina})

	def saveInformacion (self, correoUrl):
		if not (titulo=="" or donde == "" or summary == "" or fecha =="" or company == ""):
			actualiza = {}
			actualiza["urlOk"]=urlOk
			actualiza["titulo"]=titulo
			actualiza["donde"]=donde
			actualiza["summary"]=summary
			actualiza["fecha"]=fecha
			actualiza["company"]=company

			self.mongoDBAccess.update_one("correoUrl",{"_id":correoUrl},actualiza)
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



#review code
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
