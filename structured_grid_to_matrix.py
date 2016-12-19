#!/usr/bin/env python3

from PIL import Image

import numpy
import os
import re
import sys

reDimensions = re.compile( r'DIMENSIONS\s+(\d+)\s+(\d+)\s+(\d+)' )
reSpacing    = re.compile( r'SPACING\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)' )
rePointData  = re.compile( r'POINT_DATA\s+(\d+)' )
reTableData  = re.compile( r'(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)' )

for filename in sys.argv[1:]:
    with open( filename ) as f:
        width  = 0
        height = 0
        depth  = 0

        data = None # Contains matrix data
        ii   = 0    # Current data index for filling matrix

        # Stores only those coordinates (given as an x and y position)
        # that are nonzero. This permits to match adjacent time steps
        # in a very concise and sparse manner.
        nonZero = list()

        for line in f:
            if reDimensions.match(line):
                result = reDimensions.match(line)
                width  = int( result.group(1) )
                height = int( result.group(2) )
                depth  = int( result.group(3) )

                assert width * height * depth > 0, "Invalid dimensions"

                data = numpy.zeros( (height,width) )
            elif reSpacing.match(line):
                result = reSpacing.match(line)
                sx     = result.group(1)
                sy     = result.group(2)
                sz     = result.group(3)

                # TODO: I am ignoring the spacing, hence I am only
                # able to load uniform rectilinear grids.
                assert sx == sy and sy == sz, "Invalid spacing"
            elif rePointData.match(line):
                result = rePointData.match(line)
                num    = int( result.group(1) )

                assert num == width * height * depth, "Inconsistent dimensions"
            elif reTableData.match(line):
                result = reTableData.match(line) 
                d      = (u,v,w) = (
                                    float( result.group(1) ),
                                    float( result.group(2) ),
                                    float( result.group(3) )
                                   )

                for k in range(0,3):
                    ix     = ii % width
                    iy     = ii // width 
                    ii     = ii + 1

                    if d[k] > 0:
                        nonZero.append( (ix,iy) )

                    data[iy][ix] = d[k]

    outputCoordinates = "/tmp/"\
             + os.path.splitext( os.path.basename(filename) )[0]\
             + ".txt"

    with open(outputCoordinates, "w") as g:
        for (x,y) in nonZero:
            print("%d\t%d" % (x,y), file=g)

    outputImage =   "/tmp/"\
             + os.path.splitext( os.path.basename(filename) )[0]\
             + ".png"

    Image.fromarray(data).convert('L').save( outputImage )
