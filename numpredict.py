# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:22:18 2015

@author: Albert.wang
"""

from random import random,randint

import math

def wineprice(rating, age):
    peak_age = rating-50
    
    price = rating/2
    
    if age> peak_age:
        price = price *(5-(age-peak_age))
    else:
        price = price *(5*((age+1)/peak_age))
        
    if price <0:
        price = 0
        
    return price
    
def wineset1():
    rows=[]
    for i in range(300):
        rating = random()*50 + 50
        age = random()*50
        
        price = wineprice(rating,age)
        
        price *= (random()*0.4 + 0.8)
        
        rows.append({'input':(rating,age),'result':price})
        
    return rows
        
   
def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
        
    return math.sqrt(d)
   
def getdistance(data,vec1):
    distancelist = []
    for i in range(len(data)):
        vec2 = data[i]['input']
        distancelist.append((euclidean(vec1,vec2),i))
    distancelist.sort()
    return distancelist
    
    
def knnestimate(data,vec1,k=3):
    dlist = getdistance(data,vec1)
    avg = 0.0
    
    for i in range(k):
        idx = dlist[i][1]
        avg += data[idx]['result']
    avg = avg/k
        
    return avg

def inverseweight(dist,num=1.0,const=0.1):
    return num/(dist+const)
    
def subtractweight(dist,const=1.0):
    if dist>const:
        return 0
    else:
        return const-dist        
        
def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))
        
def weightedknn(data,vec1,k=5,weightf=gaussian):
    # Get distances
    dlist=getdistance(data,vec1)
    avg=0.0
    totalweight=0.0
    # Get weighted average
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg        

def dividedata(data,test=0.05):
    trainset=[]
    testset=[]
    for row in data:
        if random( )<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset
    
def testalgorithm(algf,trainset,testset):
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    return error/len(testset)
    
def wineset2( ):
    rows=[]
    for i in range(300):
        rating=random( )*50+50
        age=random( )*50
    aisle=float(randint(1,20))
    bottlesize=[375.0,750.0,1500.0,3000.0][randint(0,3)]
    price=wineprice(rating,age)
    price*=(bottlesize/750)
    price*=(random( )*0.9+0.2)
    rows.append({'input':(rating,age,aisle,bottlesize),'result':price})
    return rows

print wineprice(95.0,3.0)
print wineprice(95.0,8.0)
print wineprice(99.0,1.0)

data = wineset1()
print data[0]
print data[1]

print euclidean(data[0]['input'],data[1]['input'])

print knnestimate(data,(95.0,3.0))
print knnestimate(data,(99.0,3.0))
print knnestimate(data,(99.0,5.0))
print knnestimate(data,(99.0,5.0),1)

print subtractweight(0.1)
print inverseweight(0.1)

print weightedknn(data,(99.0,5.0))