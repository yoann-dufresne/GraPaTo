#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/2/2022

@author: francescoandreace
"""

#from platform import node
import sys
from numpy import uint8
from numpy import uint32

class Node:
    """ Nodes for GFA inspection """
    def __init__(self,len):
        self.in_edg = []
        self.out_edg = []
        self.length = uint32(len)
        self.depth = uint8(0)
        #self.sequence=""



class Graph:
    """ Graph for GFA inspection """
    def __init__(self):
        self.nodes = {}
    
    def addNode(self,name,seq):
        self.nodes[name] = Node(len(seq))

    def addEdge(self,first,firstOr,second,secondOr): 
        if firstOr == "+":
            self.nodes[first].out_edg.append(second)
        else:
            self.nodes[second].out_edg.append(first)
        if secondOr == "+":
            self.nodes[second].in_edg.append(first)
        else:
            self.nodes[first].in_edg.append(second)