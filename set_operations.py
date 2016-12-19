#!/usr/bin/env python3

import os
import re
import sys

coordinates = dict()


#
# Simple distance calculation between two pixels
#

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

for t in sorted( coordinates.keys() ):
    if t > 1:
        previous = set( coordinates[t-1] )
        current  = set( coordinates[t] )

        intersection        = current & previous
        difference          = current - previous 
        symmetricDifference = current ^ previous

        l1 = len(previous)
        l2 = len(current)
        l3 = len(intersection)
        l4 = len(difference)
        l5 = len(symmetricDifference)

        print("Average changes    : %f" % (l4/l2) )
        print("Average overlap    : %f" % (l3/min(l1,l2)))
        print("Average non-matches: %f" % (l5/(l1+l2)))

        with open( ("/tmp/Matches_%02d" % t) + ".txt", "w") as f:
            for (x,y) in previous:
                distances             = list( map( lambda ab: distance(x,y,ab[0],ab[1]), coordinates[t]) )
                indexedDistances      = zip(distances, range(len(distances)))
                minDistance, minIndex = min(indexedDistances)
                a,b                   = coordinates[t][minIndex]
                print("%d\t%d\t%d\t%d" % (x,y,a,b), file=f)
