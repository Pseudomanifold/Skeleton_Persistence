#!/usr/bin/env python3
#
# Calculates potential assignments between the skeletons of two
# different time steps. Assignments are made based on the nearest
# neighbour.

import os
import re
import sys

coordinates = dict()

""" Calculates the Euclidean distance between two pixels """
def distance( a,b,c,d ):
    return (a-c)**2 + (b-d)**2

#
# Read in all coordinates. The result is a dictionary that maps a time
# step to a list of non-zero coordinates. It is now possible to analyse
# the lists by means of various set operations.
#
for filename in sys.argv[1:]:
    t = int( re.match(r'.*-(\d\d)\..*', os.path.basename(filename) ).group(1) )
    print("Storing t = %02d..." % t)

    coordinates[t] = list()
    with open(filename) as f:
        for line in f:
            (x,y) = [ int(x) for x in line.split() ]
            coordinates[t].append( (x,y) )

#
# Calculate forward matches and backward matches. The result is a set of
# two graphs with directed edges.
#
for t in sorted( coordinates.keys() ):
    if t > 1:
        previous = coordinates[t-1]
        current  = coordinates[t]

        print("Processing t = %d" % t)

        forwardEdges  = set()
        backwardEdges = set()

        with open( ("/tmp/Matches_%02d_forward" % t) + ".txt", "w") as f:
            for (x,y) in previous:
                distances             = list( map( lambda ab: distance(x,y,ab[0],ab[1]), current ) )
                indexedDistances      = zip(distances, range(len(distances)))
                minDistance, minIndex = min(indexedDistances)
                a,b                   = coordinates[t][minIndex]
                print("%d\t%d\t%d\t%d" % (x,y,a,b), file=f)

                forwardEdges.add( ( x,y,a,b) )

        with open( ("/tmp/Matches_%02d_backward" % t) + ".txt", "w") as f:
            for (x,y) in current:
                distances             = list( map( lambda ab: distance(x,y,ab[0],ab[1]), previous ) )
                indexedDistances      = zip(distances, range(len(distances)))
                minDistance, minIndex = min(indexedDistances)
                a,b                   = coordinates[t-1][minIndex]
                print("%d\t%d\t%d\t%d" % (x,y,a,b), file=f)

                # Flip the edges: The first index should always refer to
                # the previous time step. This makes merging both edge
                # sets easier.
                backwardEdges.add( ( (a,b,x,y) ) )

        union = forwardEdges.union( backwardEdges )
        with open( ("/tmp/Matches_%02d_union" % t) + ".txt", "w") as f:
            for (a,b,c,d) in union:
                print("%d\t%d\t%d\t%d" % (a,b,c,d), file=f)
