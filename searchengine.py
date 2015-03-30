# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 10:20:05 2015

@author: Albert.wang
"""
class crawler:
    def __init__(self,dbname):
        pass
    def __del__(self):
        pass
    def dbcommit(self):
        pass
    
    def getentryid(self,table,field,value,createnew=True):
        return None
    
    def separatewords(self, text):
        return None
        
    def isindexed(self,url):
        return False
    
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    
    def crawl(self,pages,depth=2):
        pass
    
    def createindextables(self):
        pass
    
import urllib2
from BeautifulSoup import *
from urlparse import urljoin

c = ""
url = 'http://10.80.16.229/browse/GATEWAY-3036'
try:
    c = urllib2.urlopen(url)
    contents = c.read()
    print contents[0:50]
except :
    print "open failed" 

ignorewords=set(['the','of','to','and','a','in','is','it'])

def crawl(self,pages,depth=2):
    for i in range(depth):
       newpages=set( )
       for page in pages:
           try:
               c=urllib2.urlopen(page)
           except:
            print "Could not open %s" % page
            continue
        soup=BeautifulSoup(c.read( ))
        self.addtoindex(page,soup)
    links=soup('a')
    for link in links:
        if ('href' in dict(link.attrs)):
            url=urljoin(page,link['href'])
            if url.find("'")!=-1: continue
            url=url.split('#')[0] # remove location portion
            if url[0:4]=='http' and not self.isindexed(url):
                newpages.add(url)
            linkText=self.gettextonly(link)
            self.addlinkref(page,url,linkText)
    self.dbcommit( )
    pages=newpages
