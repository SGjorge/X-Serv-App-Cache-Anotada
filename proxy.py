#!/usr/bin/python

import webapp
import urllib

class proxy(webapp.webApp):

	cache = {}

	def inserthello(self,contenido):
		pos1 = contenido.find("<body")
		pos2 = contenido.find(">",pos1)
		return contenido[:(pos2+1)] + "HOLA-" + contenido[(pos2+1):]

	def inserturloriginal(self,contenido,pag):
		pos1 = contenido.find("<body")
		pos2 = contenido.find(">",pos1)
		return contenido[:(pos2+1)] + "<a href='"  + pag  +"'>url original-</a>" + contenido[(pos2+1):]

	def insertrecargar(self,contenido,parsedRequest):
		pos1 = contenido.find("<body")
		pos2 = contenido.find(">",pos1)
		return contenido[:(pos2+1)] + "<a href='"  + "http://localhost:1234/" + parsedRequest  +"'>recargar-</a>" + "<br>" + contenido[(pos2+1):]


	def savecache(self, parsedRequest):
		pos1 = parsedRequest.find(".")
		pk = parsedRequest[:pos1]
		self.cache[pk] = "<a href='http://" + parsedRequest + "'>'http://'" + parsedRequest + "</a>"

	def insertcache(self,contenido):
		pos1 = contenido.find("<body")
		pos2 = contenido.find(">",pos1)
		return contenido[:(pos2+1)] + str(self.cache)+ "<br>" + contenido[(pos2+1):]

	def parse(self, request):
		try:
			url = str(request.split("/")[1][: -4])
			return url
		except:
			return None

	def process(self, parsedRequest):
		try:
			pag = urllib.urlopen("http://" + parsedRequest)
			self.savecache(parsedRequest)
			contenido = pag.read()
			contenido = self.insertcache(contenido)
			contenido = self.insertrecargar(contenido,parsedRequest)
			contenido = self.inserturloriginal(contenido,"http://" + parsedRequest)
			contenido = self.inserthello(contenido)
			return ("200 OK", "<html><body><h1>" + contenido + "</h1></body></html>")
		except IOError:
			return("400 Error", "")
if __name__ == "__main__":
	web = proxy("localhost", 1234)