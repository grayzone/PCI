# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:44:35 2015

@author: Albert.wang
"""

from math import log

my_data=[['slashdot','USA','yes',18,'None'],
['google','France','yes',23,'Premium'],
['digg','USA','yes',24,'Basic'],
['kiwitobes','France','yes',23,'Basic'],
['google','UK','no',21,'Premium'],
['(direct)','New Zealand','no',12,'None'],
['(direct)','UK','no',21,'Basic'],
['google','USA','no',24,'Premium'],
['slashdot','France','yes',19,'None'],
['digg','USA','no',18,'None'],
['google','UK','no',18,'None'],
['kiwitobes','UK','no',19,'None'],
['digg','New Zealand','yes',12,'Basic'],
['slashdot','UK','no',21,'None'],
['google','UK','yes',18,'Basic'],
['kiwitobes','France','yes',19,'Basic']]


class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb
        
def divideset(rows,column,value):
# Make a function that tells us if a row is in
# the first group (true) or the second group (false)
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value
    # Divide the rows into two sets and return them
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)
    
# Create counts of possible results (the last column of
# each row is the result)
def uniquecounts(rows):
    results={}
    for row in rows:
    # The result is the last column
        r=row[len(row)-1]
        if r not in results: results[r]=0
        results[r]+=1
    return results 
    
def giniimpurity(rows):
    total=len(rows)
    counts=uniquecounts(rows)
    imp=0
    for k1 in counts:
        p1=float(counts[k1])/total
        for k2 in counts:
            if k1==k2: continue
            p2=float(counts[k2])/total
            imp+=p1*p2
    return imp
    
def entropy(rows):

    log2=lambda x:log(x)/log(2)
    results=uniquecounts(rows)
    # Now calculate the entropy
    ent=0.0
    for r in results.keys( ):
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent

def buildtree(rows,scoref=entropy):
    if len(rows)==0: return decisionnode( )
    current_score=scoref(rows)
    # Set up some variables to track the best criteria
    best_gain=0.0
    best_criteria=None
    best_sets=None
    column_count=len(rows[0])-1
    for col in range(0,column_count):
    # Generate the list of different values in
    # this column
        column_values={}
        for row in rows:
            column_values[row[col]]=1
    # Now try dividing the rows up for each value
    # in this column
    for value in column_values.keys( ):
        (set1,set2)=divideset(rows,col,value)
    # Information gain
    p=float(len(set1))/len(rows)
    gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
    if gain>best_gain and len(set1)>0 and len(set2)>0:
        best_gain=gain
        best_criteria=(col,value)
        best_sets=(set1,set2)
    # Create the subbranches
    if best_gain>0:
        trueBranch=buildtree(best_sets[0])
        falseBranch=buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))   
   
def printtree(tree,indent=''):
# Is this a leaf node?
    if tree.results!=None:
        print str(tree.results)
    else:
    # Print the criteria
        print str(tree.col)+':'+str(tree.value)+'? '
        # Print the branches
        print indent+'T->',
        printtree(tree.tb,indent+' ')
        print indent+'F->',
        printtree(tree.fb,indent+' ')   
  
  
res =  divideset(my_data,2,'yes')
print res

print giniimpurity(my_data)
print entropy(my_data)
set1, set2 = divideset(my_data,2,'yes')
print set1
print set2
print entropy(set1)
print giniimpurity(set1)

tree =  buildtree(my_data)
printtree(tree)
