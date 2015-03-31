# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:04:34 2015

@author: Albert.wang
"""
import os

import pylab

class matchrow:
    def __init__(self,row,allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row)-1)]
        else:
            self.data = row[0:len(row)-1]
        self.match = int(row[len(row)-1])
        
def loadmatch(f, allnum=False):
    rows = []
    for line in file(f):
        rows.append(matchrow(line.split(','),allnum))
    return rows
    
def plotagematches(rows):
    xdm,ydm = [r.data[0] for r in rows if r.match==1],[r.data[1] for r in rows if r.match==1]    
    xdn,ydn = [r.data[0] for r in rows if r.match==0],[r.data[1] for r in rows if r.match==0]
    
    pylab.plot(xdm,ydm,"go")
    pylab.plot(xdn,ydn,"ro")
    
    pylab.show()
    
    
agesonly = loadmatch(os.getcwd() + '/data/matchmaker/agesonly.csv',allnum=True)
plotagematches(agesonly)

"""
for item in agesonly:
    print item.data
    print item.match
"""

matchmaker = loadmatch(os.getcwd() + "/data/matchmaker/matchmaker.csv")

"""
for item in matchmaker:
    print item.data
    print item.match
"""

