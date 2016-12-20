#!/usr/bin/env python3

import math
import numpy
import os
import sys

def distance( a,b,c,d ):
    return math.sqrt( (a-c)**2 + (b-d)**2 )

for filename in sys.argv[1:]:
    name      = os.path.basename(filename)
    distances = list()

    with open(filename) as f:
        for line in f:
            (a,b,c,d) = [ float(x) for x in line.split() ]
            distances.append( distance(a,b,c,d) )

    print("Processed %s:" % filename )
    print("  Minimum distance: %f" % min( distances ) )
    print("  Mean distance   : %f" % numpy.mean( distances ) )
    print("  Median distance : %f" % numpy.median( distances ) )
    print("  Maximum distance: %f" % max( distances ) )
    print("  Quantile <= 2   : %f" % ( len( [ x for x in distances if x <= 2 ] ) / len(distances) ) )
