#!/usr/bin/env python3

from skimage import measure

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

    labels = measure.label( image, background=0 )

    plt.imshow(labels, cmap='Set1')
    plt.show()
