# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:30:56 2015

@author: albert.wang
"""

import feedparser
import re
import os
import types

def getwordcounts(url):
    d = {}
    wc = {}
    try:
        d = feedparser.parse(url)
    except:
        print "failed to parse the url."
        return "",wc
        
    if type(d) is types.NoneType:
        print "d"
        
    if type(d.feed) is types.NoneType:
        print "yes"
        
    if type(d.feed.title) is types.NoneType:
        print "title"
    
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word] += 1
       
    return d.feed.title, wc
    
def getwords(html):
    txt = re.compile(r'<[^>]+>').sub('',html)
    
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    
    return [word.lower() for word in words if word != '']
    
apcount = {}
wordcounts = {}

feedlist=[line for line in file(os.getcwd() + "/data/feed/feedlist.txt")]
for feedurl in feedlist:
    title,wc = getwordcounts(feedurl)
    wordcounts[title] =wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count > 1 :
            apcount[word] += 1
            

wordlist = []
for w,bc in apcount.items():
    frac = float(bc)/len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

print wordlist   

    