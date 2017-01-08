#!/usr/bin/env python3
#
# Processes forward and backward matches between two time steps and converts
# them into one unified format.

import collections
import os
import re
import sys

filenames = sys.argv[1:]
steps     = collections.defaultdict(list)

for filename in filenames:
    if "union" in filename:
        continue

    t = int( re.match(r'.*_(\d\d)_.*', filename ).group(1) )
    steps[t].append( filename )

for t in sorted( steps.keys() ):
    output = "/tmp/Matches_%02d_directed.txt" % t
    with open(output, "w") as f:
        for filename in sorted(steps[t]):
            direction = " -> " if "forward" in filename else " <- "
            print(filename, direction)
            with open(filename) as g:
                for line in g:
                    (a,b,c,d) = [ int(x) for x in line.split() ]
                    print("%d\t%d%s%d\t%d" % (a,b, direction, c,d), file=f)
