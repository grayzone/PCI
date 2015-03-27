# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:47:18 2015

@author: albert.wang
"""

from math import sqrt
import os

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
        
    if len(si) == 0: 
        return 0
            
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
        
    return 1/(1+sum_of_squares)
    
    
def sim_pearson(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
            
    n = len(si)
        
    if n == 0: 
        return 0
            
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])
    
    sum1sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2sq = sum([pow(prefs[person2][it], 2) for it in si])
    
    pSum = sum([prefs[person1][it]*prefs[person2][it] for it in si])
    
    num = pSum - (sum1*sum2/n)
    
    den = sqrt((sum1sq-pow(sum1, 2)/n)*(sum2sq-pow(sum2, 2)/n))
    
    if den == 0:
        return 0
        
    r = num/den
    
    return r
    
def sim_tanimoto(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
                
    return float(len(si))/float(len(prefs[person1]) + len(prefs[person2])-len(si))
    

def topMatches(prefs, person, n, similarity):
    scores = [(similarity(prefs, person,other), other) for other in prefs if other != person]
    
    scores.sort()
    scores.reverse()
    
    return scores[0:n]
    

def getRecommendations(prefs, person, similarity):
    totals = {}
    simSums = {}
    
    for other in prefs:
        if other == person:
            continue
        
        sim = similarity(prefs, person, other)
        if sim <=0:
            continue
        
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0 :
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                
                simSums.setdefault(item,0)
                simSums[item] += sim 
                
    rankings = [(total/simSums[item], item) for item,total in totals.items()]
        
    rankings.sort()
    rankings.reverse()
    return rankings
        
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            
            result[item][person] = prefs[person][item]
    
    return result
         

def calculateSimilarItems(prefs, n):
    result = {}
    
    itemPrefs = transformPrefs(prefs)
    
    c = 0
    
    for item in itemPrefs:
        c += 1
        if c%100 == 0:
            print "%d / %d" % (c,len(itemPrefs))
            
        scores = topMatches(itemPrefs, item, n, sim_distance)
        result[item] = scores
    
    return result
   
def getRecommendationItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {} 

    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            if item2 in userRatings:
                continue
            
            scores.setdefault(item2, 0)
            scores[item2] += similarity*rating
            
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
            
    rankings = [(score/totalSim[item], item) for item,score in scores.items()]
    rankings.sort()
    rankings.reverse()

    return rankings   
    
def loadMovieLens(path):
    movies = {}
    
    for line in open(path + '/u.item'):
        (id,title) = line.split('|')[0:2]
        movies[id] = title
        
    prefs = {}
    for line in open(path + '/u.data'):
        (user,movieid,rating,ts) = line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]] = float(rating)
        
    return prefs
        
    
print sim_distance(critics, 'Lisa Rose','Gene Seymour')
print sim_pearson(critics, 'Lisa Rose','Gene Seymour')
print sim_tanimoto(critics, 'Lisa Rose','Gene Seymour')
print topMatches(critics, 'Toby',3,sim_pearson)
print topMatches(critics, 'Toby',3,sim_distance)
print topMatches(critics, 'Toby',3,sim_tanimoto)
print getRecommendations(critics, 'Toby', sim_pearson)
print getRecommendations(critics, 'Toby', sim_distance)

movies =  transformPrefs(critics)
print topMatches(movies,'Superman Returns',5, sim_pearson)
print getRecommendations(movies, 'Just My Luck', sim_pearson)

itemSim =  calculateSimilarItems(critics, 10)
print getRecommendationItems(critics,itemSim,'Toby')

prefs =  loadMovieLens(os.getcwd() + '/data/movielens')
print getRecommendations(prefs, '87', sim_pearson)[0:30]

itemSim =  calculateSimilarItems(prefs, 50)
print getRecommendationItems(prefs,itemSim,'87')[0:30]