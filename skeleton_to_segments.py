#!/usr/bin/env python3
#
# Module for partitioning a skeleton into segments. A segment is defined
# by having at least one irregular end point, meaning that there is
# a node whose degree is != 2.

import collections

# FIXME: Make this configurable somewhere
width  = 839 
height = 396

"""
Union-find data structure for partitioning the graph into connected
components segments, which may then subsequently be partitioned into
individual segments.
"""
class UnionFind:
    def __init__(self, vertices):
        self.components = dict()

        for vertex in vertices:
            self.components[vertex] = vertex

    """ Parent access with path compression """
    def find(self, vertex):
        if self.components[vertex] == vertex:
            return vertex

        # Path compression
        else:
            self.components[vertex] = self.find( self.components[vertex] )
            return self.components[vertex]

    """ Provides merging functionality """
    def merge(self, u, v):
        cu = self.find(u)
        cv = self.find(v)

        self.components[cu] = cv

    """ Generator for all roots """
    def roots(self):
        for vertex in sorted( self.components.keys() ):
            if self.find(vertex) == vertex:
                yield vertex

    """ Gets all vertices of a specific connected component """
    def vertices(self, root):
        result = list()

        for vertex in self.components.keys():
            if self.find(vertex) == root:
                result.append( vertex )

        return sorted(result)

"""
Basic node class
"""
class Node:
    def __init__(self,x,y,i):
        self.x = x
        self.y = y
        self.i = i # Node ID


""" Checks whether a given pixel position is valid """
def valid(x,y):
    return x >= 0 and x < width and y >= 0 and y < height

"""
Returns all valid neighbours of a pixel. This function assumes a regular
8-neighbourhood for each pixel.
"""
def validNeighbours(x,y):
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

""" Partitions a skeleton into its segments """
def getSegments(filename, appendBranchVertices=True):
    with open(filename) as f:
        coordinates    = dict() # Maps a coordinate to an index
        indices        = dict() # Maps an index to a coordinate
        edges          = list()
        vertices       = set()
        degrees        = dict()
        neighbours     = collections.defaultdict(list)

        for index,line in enumerate(f):
            (x,y)                   = [ int(a) for a in line.split() ]
            coordinates [ (x,y) ]   = index
            indices[ index ]        = (x,y)

        #
        # Graph creation
        #

        for (x,y) in sorted( coordinates.keys() ):
            for (a,b) in validNeighbours(x,y):
                if (a,b) in coordinates:
                    u = coordinates[ (x,y) ]
                    v = coordinates[ (a,b) ]

                    vertices.add(u)
                    vertices.add(v)

                    if u < v:
                        degrees[u] = degrees.get(u, 0) + 1
                        degrees[v] = degrees.get(v, 0) + 1

                        edges.append( (u,v) )

                        # That's a rather wasteful way of permitting queries
                        # about the neighbours of vertices, but I shall use
                        # it later to extend all identified segments.
                        neighbours[u].append(v)
                        neighbours[v].append(u)

        
        #
        # Segment the graph
        #

        regularVertices  = [ vertex for vertex in vertices if degrees[vertex] <= 2 ]
        branchVertices   = [ vertex for vertex in vertices if degrees[vertex] > 2  ]
        partitionedEdges = [ (u,v) for (u,v) in edges if degrees[u] <= 2 and degrees[v] <= 2 ]
        branchEdges      = [ (u,v) for (u,v) in edges if degrees[u] > 2 or degrees[v] > 2 ]

        ufSegments = UnionFind(regularVertices)

        for (u,v) in partitionedEdges:
            ufSegments.merge(u,v)

        segments = dict( list() )

        for root in ufSegments.roots():
            segments[root] = ufSegments.vertices(root)

        # Append branch vertices to all matching segments
        if appendBranchVertices:
            for vertex in branchVertices:
                for neighbour in neighbours[vertex]:
                    if neighbour in regularVertices:
                        root = ufSegments.find(neighbour) 
                        segments[root].append(vertex)

        result = []

        for segment in segments.values():
            s = []
            for index in segment:
                s.append( indices[index] )

            result.append(s)

        return result, [ indices[u] for u in sorted(branchVertices) ]
