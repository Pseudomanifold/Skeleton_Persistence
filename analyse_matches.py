#!/usr/bin/env python3

from collections import defaultdict

import math
import numpy
import os
import sys

threshold = 2.0

def distance( a,b,c,d ):
    return math.sqrt( (a-c)**2 + (b-d)**2 )

for filename in sys.argv[1:]:
    name      = os.path.splitext( os.path.basename(filename) )[0]
    distances = list()
    matches   = defaultdict(list)

    with open(filename) as f:
        for line in f:
            (a,b,c,d) = [ int(x) for x in line.split() ]
            matches[ (c,d) ].append( (a,b) )
            distances.append( distance(a,b,c,d) )

    print("Processed %s:" % filename )
    print("  Minimum distance: %f" % min( distances ) )
    print("  Mean distance   : %f" % numpy.mean( distances ) )
    print("  Median distance : %f" % numpy.median( distances ) )
    print("  Maximum distance: %f" % max( distances ) )
    print("  Quantile <= 2   : %f" % ( len( [ x for x in distances if x <= 2 ] ) / len(distances) ) )

    # Sort potential assignments based on their distance to the source
    # point. Afterwards, only the first entry is used to denote all of
    # the greedy matches.
    for c,d in sorted( matches.keys() ):
        matches[(c,d)] = sorted( matches[(c,d)], key = lambda ab : distance(c,d,ab[0], ab[1] ) )

    #
    # Greedy matches
    #
    with open("/tmp/" + name + "_matched.txt", "w") as f:
        for c,d in sorted( matches.keys() ):
            a,b = matches[(c,d)][0]
            print("%d\t%d\t%d\t%d" % (a,b,c,d ), file=f)

    #
    # Unmatched
    #
    with open("/tmp/" + name + "_unmatched.txt", "w") as f:
        for c,d in sorted( matches.keys() ):
            nonMatches = matches[(c,d)][1:]
            for a,b in nonMatches:
                print("%d\t%d" % (a,b), file=f)
