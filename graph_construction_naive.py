#!/usr/bin/env python3

import sys

coordinates = set()

width  = 839 
height = 396

class Node:
    def __init__(self,x,y,i):
        self.x = x
        self.y = y
        self.i = i # Node ID

def valid(x,y):
    return x >= 0 and x < width and y >= 0 and y < height

def neighbours(x,y):
    offset = [
        ( 0,-1),
        (+1,-1),
        (+1, 0),
        (+1,+1),
        ( 0,+1),
        (-1,+1),
        (-1, 0),
        (-1,-1)
    ]

    return list( filter( lambda x : valid(x[0],x[1]), [ (x+ox,y+oy) for (ox,oy) in offset ] ) )

with open(sys.argv[1]) as f:
    coordinates    = dict()
    edges          = list()

    for index,line in enumerate(f):
        (x,y)                   = [ int(a) for a in line.split() ]
        coordinates [ (x,y) ]   = index

    for (x,y) in sorted( coordinates.keys() ):
        for (a,b) in neighbours(x,y):
            if (a,b) in coordinates:
                u = coordinates[ (x,y) ]
                v = coordinates[ (a,b) ]

                if u < v:
                    edges.append( (u,v) )
