#subtitledownloader.py

import urllib,urllib2
from bs4 import BeautifulSoup
import sys
class TVSeries(object):
	'''get subtitle of tvseries'''
	l=[]
	language=[]
	download=[]
	def __init__(self,search):
		self.search = search
		self.searchseries()
		self.l = []
		self.language = []
		self.download = []

	def searchseries(self):
		self.url="http://www.addic7ed.com/search.php"
		print self.search
		#print self.language[0]
		self.values = {"search":self.search,"Submit":"Search"}
		self.data = urllib.urlencode(self.values)
		self.search_url = self.url+"?"+self.data
		self.response = urllib2.urlopen(self.search_url)
		self.page = self.response.read()
		#print self.page
		self.parseseriespage()

	def parseseriespage(self):
		self.soup = BeautifulSoup(self.page,"xml")
		for anchors in self.soup.find_all("a"):
			if anchors["href"].startswith("serie"):
				print anchors["href"]
				self.l.append(anchors["href"])
		print self.l[0]
		self.getdownloadpage()	
		
	def getdownloadpage(self):
		self.url = "http://www.addic7ed.com/"
		self.downloadpage_url = self.url+self.l[0]
		self.response = urllib2.urlopen(self.downloadpage_url)
		self.page = self.response.read()
		self.parsedownloadpage()

	def parsedownloadpage(self):
		self.soup = BeautifulSoup(self.page,"xml")
		for anchors in self.soup.find_all("a",attrs={"class":"buttonDownload"}):
			self.downloadsub_url = "http://www.addic7ed.com"+anchors["href"]	
			#print self.downloadsub_url
			self.download.append(self.downloadsub_url)
		for data in self.soup.find_all("td",attrs={"class":"language"}):
			self.language.append(''.join(data.findAll(text=True)))
		self.downloadsubtitle()	

	def downloadsubtitle(self):
		for i in range(0,len(self.download)):
			if self.language[i].startswith("English"):
				self.request = urllib2.Request(self.download[i],headers={"Referer":"http://www.addic7ed.com/"})
				self.response = urllib2.urlopen(self.request)
				self.page = self.response.read()
				#print self.page
				self.filename = self.search+".srt"
				with open(self.filename,"wb") as f:
					f.write(self.page)
				print "Successfully downloaded ",self.filename
				break	 			 		



if __name__=="__main__":
	i=1
	name = ""
	for arg in sys.argv:
		if i==1:
			i=i+1
			continue
		else:
			name = name+arg+" "	
	print name
	TVSeries(name)

