#!/usr/bin/env python3

import argparse
import collections
import os
import re
import sys

import skeleton_to_segments as skel

parser = argparse.ArgumentParser()
parser.add_argument('--width' , type=int, default=839)
parser.add_argument('--height', type=int, default=396)
parser.add_argument('--prefix', type=str, default="viscfing_1-")
parser.add_argument('--path'  , type=str, default="./Skeletons-2/TXT/")
parser.add_argument('FILES', nargs='+')

arguments = parser.parse_args()

skel.width  = arguments.width
skel.height = arguments.height

""" Returns path to skeleton of a certain time step """
def makeSkeletonPath(filename, t):
    # Prefix for reading the skeleton file that corresponds to a given set
    # of matches.
    skeletonPrefix = arguments.prefix

    skeletonPath =   os.path.abspath(arguments.path) + "/"\
                   + skeletonPrefix                       \
                   + ("%02d" % t)                         \
                   + ".txt"

    return skeletonPath

for filename in arguments.FILES:
    print("Processing %s..." % filename, file=sys.stderr)
    with open(filename) as f:
        t = int( re.match(r'.*t(\d\d).*', filename ).group(1) )

        skeletonPath             = makeSkeletonPath(filename,t+1)
        segments, branchVertices = skel.getSegments(skeletonPath, appendBranchVertices=True)
        num_pixels               = 0
        num_active_pixels        = 0
        num_segments             = len(segments)
        num_active_segments      = 0
        growth_values            = collections.defaultdict(list)

        for line in f:
            line                 = line.rstrip()
            x,y,g                = [ int(a) for a in line.split() ]
            num_pixels           = num_pixels + 1
            growth_values[(x,y)] = g

            # TODO: range (?)
            if g >= -10:
                num_active_pixels = num_active_pixels + 1

        for index,segment in enumerate(segments):
            growth = []
            for pixel in segment:
                if pixel not in branchVertices:
                    if growth_values[pixel]:
                        growth.append( growth_values[pixel] )

            # TODO: range (?)
            if growth and min(growth) >= -10:
                num_active_segments = num_active_segments + 1

        print("%02d %f %f" % (t, num_active_pixels / num_pixels, num_active_segments / num_segments ))
