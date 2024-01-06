# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 14:32:12 2024

@author: seanm
"""

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph


class Graph():
 
    def __init__(self, state):
        self.X = state["x"]+1
        self.Y = state["y"]+1
        self.edges = state["edges"]
        self.agents = state["agents"]
 
    #Returns the shortest path to (targetX,targetY) and the second vertex in the shortest path
    def solution(self,dist,prev,srcX,srcY, targetX,targetY):
        
       S = []
       u = [targetX,targetY]
       #Verify vertex is reachable
       if  prev[targetX,targetY] is None:
           return 1e7,[]
       if prev[u[0],u[1]] is not None or (u[0],u[1])==(srcX,srcY):         
           while u is not None :                     
               S.append(u)     
               u = prev[u[0],u[1]] 
       return dist[targetX,targetY],S[-2]        
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search not nearest vertex not in the
        # shortest path tree
        for vX in range(0,self.X,1):
            for vY in range(0,self.Y,1):
                if dist[vX,vY] < min and sptSet[vX,vY] == False:
                    min = dist[vX,vY]
                    min_index = vX,vY
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self,srcX,srcY,targetX,targetY):
 
        dist = ([0] * self.Y) * self.X
        dist[srcX,srcY] = 0
        prev = ([None] * self.Y) * self.X
        sptSet = ([False] * self.Y) * self.X
 
        for cX in range(0,self.X,1):
            for cY in range(0,self.Y,1):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
                uX,uY = self.minDistance(dist, sptSet)
                if (targetX,targetY) == (uX,uY):
                    return 
            # Put the minimum distance vertex in the
            # shortest path tree
                sptSet[uX,uY] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
                for vX in range(0,self.X,1):
                    for vY in range(0,self.Y,1):
                        for edge in self.edges :
                            for agent in self.agents:
                                if edge["type"]!="always blocked" and agent["location"]!=[vX,vY] and edge["from"]==[uX,uY] and edge["to"] ==[vX,vY] and  sptSet[vX,vY]==False and dist[vX,vY] > dist[uX,uY] + 1 :
                                    dist[vX,vY] = dist[uX,uY] + 1
                                    prev[vX,vY] = [uX,uY]
                                    
        return self.solution(prev,srcX,srcY, targetX,targetY)                         
                      