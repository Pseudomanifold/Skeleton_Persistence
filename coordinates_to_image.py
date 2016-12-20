#!/usr/bin/env python3

from collections import defaultdict
from skimage     import measure

import matplotlib.pyplot as plt

import numpy
import os
import sys

width  = 839
height = 396

for filename in sys.argv[1:]:
    name      = os.path.splitext( os.path.basename(filename) )[0]
    image = numpy.zeros( (height,width) )
    
    with open(filename) as f:
        for line in f:
            (x,y)       = [ int(a) for a in line.split()[0:2] ]
            image[y][x] = 1

    labels       = measure.label( image, background=0 )
    nrows, ncols = labels.shape

    components = defaultdict(list)

    #
    # Separate connected components
    #
    for y in range(nrows):
        for x in range(ncols):
            component = labels[y][x]
            if component > 0:
                components[component].append( (x,y) )

    #
    # Stored connected components
    #
    with open("/tmp/" + name + "_components.txt", "w") as f:
        for component in sorted( components.keys() ):
            for (x,y) in components[component]:
                print("%d\t%d" % (x,y), file=f)
            print("\n", file=f)
