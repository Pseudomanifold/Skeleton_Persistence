#!/usr/bin/env python3

import os
import re
import sys

coordinates = dict()

#
# Read in all coordinates. The result is a dictionary that maps a time
# step to a list of non-zero coordinates. It is now possible to analyse
# the lists by means of various set operations.
#

for filename in sys.argv[1:]:
    t = int( re.match(r'.*-(\d\d)\..*', os.path.basename(filename) ).group(1) )
    print("t = %02d" % t)

    coordinates[t] = list()
    with open(filename) as f:
        for line in f:
            (x,y) = [ int(x) for x in line.split() ]
            coordinates[t].append( (x,y) )
