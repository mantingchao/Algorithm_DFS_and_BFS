# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 22:03:22 2020

@author: Manting
"""
import numpy as np
import heapq as hq
import time
# job[release time,processing time]
jobs=[[0,6],
      [2,2],
      [2,3],
      [6,2],
      [7,5],
      [9,2]]

# jobs=[[0,6],[2,2]]
#%%
def makespans(seq):
    schedule = np.zeros(len(seq))
    schedule[0] = seq[0][0]+seq[0][1]
    for i in range(1,len(seq)): 
        if schedule[i-1] >= seq[i][0] :#前一個大於release time
            schedule[i] = schedule[i-1] + seq[i][1]
        else:
            schedule[i] = seq[i][0]  + seq[i][1]
    return schedule[-1]

#%% Pure Enumerate
tmp=100
best_seq_m1=[]
all_permutation =[]
from itertools import permutations
for i in permutations([0,1,2,3,4,5],6):
    all_permutation.append(i)
    
for i in range(len(all_permutation)):
    s1=[]
    for j in range(len(all_permutation[i])):
        s1.append(jobs[all_permutation[i][j]])
    Cmax = makespans(s1)
    # print(s1)
    if Cmax <= tmp:
        tmp = Cmax
        best_seq_m1.append(s1)

print("best Cmax:",tmp)
print("best sequent:",best_seq_m1)
    
#%% Depth First Search
def DFS(lst): 
    tmp = 100
    # best_seq=[]
    if len(lst) == 0: 
        return []
    if len(lst) == 1: 
        return [lst] 
    l = []
    
      
    for i in range(len(lst)): 
       m = lst[i] 
       # print("nonono",m)
       remLst = lst[:i] + lst[i+1:] 
       # print('haha',remLst)
       
       for p in DFS(remLst):
           c_max_list=[]
           l.append([m] + p)
           c_max_list.append([l[-1],makespans(l[-1])])
           # print(c_max_list)
           if len(l[-1]) == 6:
               # print(l[-1])
               Cmax = makespans(l[-1])
               
               if Cmax < tmp:
                   tmp = Cmax
                   # best_seq = l[-1]        
                   # print("DFS best sequence:",best_seq)
                   print("DFS Minimum Cmax:",tmp)         
    return l#,tmp,best_seq

# all_list,best_Cmax,best_seq =  permutation(jobs)  
Best = 100
s = time.time() 
all_list =  DFS(jobs)   
for i in all_list:
    if makespans(i) < Best:
        Best = makespans(i)
e = time.time()

print('DFS Best Cmax', Best, 'DFS Best run time:', e-s)
#%% Best First Search

#return all branch of head
def without(head, job):
    jobc = job.copy()
    if(type(head[0]) == int):
        jobc.remove(head)
        return jobc
    
    for i in head:
        jobc.remove(i)
    
    return jobc

def BestFS(job):

    heaplst = []
    res = []
    for i in job:
        hq.heappush(heaplst, (makespans([i]), [i]))
    
    while(heaplst != []):
        
        head = hq.heappop(heaplst)[1]
        # print(head)
        for i in without(head, job):
            headc = head.copy()
            headc.append(i)
            hq.heappush(heaplst, (makespans(headc), headc))
            headc = head.copy()
        
        if(len(head) == len(job)):
            res.append(head)              
        if(heaplst == []):
            break
    
    return res
#%%
Best = 100
s = time.time()
for i in BestFS(jobs):
    if(makespans(i) < Best):
        Best = makespans(i)
e = time.time()

print('BFS best Cmax', Best, 'BFS Best run time:', e-s)



