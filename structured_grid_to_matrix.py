#!/usr/bin/env python3

from PIL import Image

import numpy
import re
import sys

reDimensions = re.compile( r'DIMENSIONS\s+(\d+)\s+(\d+)\s+(\d+)' )
reSpacing    = re.compile( r'SPACING\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)' )
rePointData  = re.compile( r'POINT_DATA\s+(\d+)' )
reTableData  = re.compile( r'(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)' )

width  = 0
height = 0
depth  = 0

data = None # Contains matrix data
ii   = 0    # Current data index for filling matrix

with open( sys.argv[1] ) as f:
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

                data[iy][ix] = d[k]

Image.fromarray(data).convert('L').save( "/tmp/test.bmp" )
