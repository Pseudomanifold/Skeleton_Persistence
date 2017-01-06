#!/usr/bin/env python3
#
# Analyses the result of the bipartite matching between adjacent time
# steps. There are numerous interesting cases here:
#
#   1) One-to-one matches: There is exactly one match between two
#      coordinates in the data. This is the most regular match we
#      may hope for. It indicates that a pixel continues to exist
#      in the next time-step.
#
#   2) One-to-many matches: This indicates that a structure is created
#      in the subsequent time step.
#
#   3) Many-to-one matches: This indicates that a structure is destroyed
#      in the current time step.

import collections
import re
import os
import sys

import skeleton_to_segments as skel

# Prefix for reading the skeleton file that corresponds to a given set
# of matches.
skeletonPrefix = "viscfing_1-"

""" Calculates the Euclidean distance between two pixels """
def distance( a,b,c,d ):
    return (a-c)**2 + (b-d)**2

""" Prints a set of pixels """
def printPixels(pixels):
    for (a,b) in pixels:
        print("%d\t%d" % (a,b))
    print("\n")

# Stores matches for the current time step (a) and the subsequent time
# step (b). The key is a pixel tuple here, while the value stores all
# the corresponding matches.
#
# Note that both structures are by necessity _directed_.
aMatches = collections.defaultdict(list)
bMatches = collections.defaultdict(list)

allEdges       = set()
oneToOneEdges  = set()
oneToManyEdges = set()
manyToOneEdges = set()

# Partitions pixels in the current time step according to how they can
# be assigned to pixels in the subsequent time step.
created    = set()
destroyed  = set()
persisting = set()

filename = sys.argv[1]
t        = 0

with open(filename) as f:

    # Note that matches for t=55 correspond to finding a matching
    # between time steps t=54 and t=55. Hence the subtraction.
    t = int( re.match(r'.*_(\d\d)_.*', filename ).group(1) )
    t = t-1

    for line in f:
        (a,b,c,d) = [ int(x) for x in line.split() ]

        aMatches[ (a,b) ].append( (c,d) )
        bMatches[ (c,d) ].append( (a,b) )

        allEdges.add( (a,b,c,d) )

numMatches = len(allEdges)

#
# Find one-to-one matches. As this task is symmetrical by nature, it
# suffices to traverse one of the dictionaries.
#

numOneToOneMatches = 0

for (a,b) in sorted( aMatches.keys() ):
    aPartners = aMatches[ (a,b) ]
    if len(aPartners) == 1:
        (c,d)     = aPartners[0]
        bPartners = bMatches[ (c,d) ]

        if len(bPartners) == 1:
            numOneToOneMatches += 1
            oneToOneEdges.add( (a,b,c,d) )

            persisting.add( (a,b) )

print("One-to-one matches: %d/%d (%.3f)" % (numOneToOneMatches, numMatches, numOneToOneMatches / numMatches), file=sys.stderr)

#
# Find one-to-many matches
#

numOneToManyMatches = 0

for (a,b) in sorted( aMatches.keys() ):
    matches = aMatches[ (a,b) ]
    if len(matches) > 1:
        singleMatch = True
        for (c,d) in matches:
            if len( bMatches[ (c,d) ] ) != 1:
                singleMatch = False
                break
        if singleMatch:
            numOneToManyMatches += len(matches)

            for (c,d) in matches:
                oneToManyEdges.add( (a,b,c,d) )

            created.add( (a,b) )

print("One-to-many matches: %d/%d (%.3f)" % (numOneToManyMatches, numMatches, numOneToManyMatches / numMatches), file=sys.stderr)

#
# Find many-to-one matches
#

numManyToOneMatches = 0

for (c,d) in sorted( bMatches.keys() ):
    matches = bMatches[ (c,d) ]
    if len(matches) > 1:
        singleMatch = True
        for (a,b) in matches:
            if len( aMatches[ (a,b) ] ) != 1:
                singleMatch = False
                break
        if singleMatch:
            numManyToOneMatches += len(matches)

            for (a,b) in matches:
                manyToOneEdges.add( (a,b,c,d) )
                destroyed.add( (a,b) )

print("Many-to-one matches: %d/%d (%.3f)" % (numManyToOneMatches, numMatches, numManyToOneMatches / numMatches), file=sys.stderr)

#
# Irregular edges
#

irregularEdges = allEdges - oneToOneEdges - oneToManyEdges - manyToOneEdges

print("Irregular matches: %d/%d (%.3f)" % (len(irregularEdges), numMatches, len(irregularEdges) / numMatches), file=sys.stderr)

#
# Print "classified" pixels
#

printPixels(persisting)
printPixels(created)
printPixels(destroyed)

#
# Load the corresponding skeleton and extend the information to its
# segments
#

skeletonPath =   os.path.abspath(filename+"/../../") + "/"\
               + skeletonPrefix                           \
               + ("%02d" % t)                             \
               + ".txt"

segments               = skel.getSegments(skeletonPath)
pixelToSegment         = dict()
mappedPixelsPerSegment = dict()

for index,segment in enumerate(segments):
    for pixel in segment:
        pixelToSegment[pixel]         = index
        mappedPixelsPerSegment[index] = mappedPixelsPerSegment.get(index, 0) + 1

for index in sorted(mappedPixelsPerSegment.keys()):
    numPixels       = len(segments[index])
    numMappedPixels = mappedPixelsPerSegment[index]
    print("Ratio of mapped pixels = %.3f" % (numMappedPixels / numPixels), file=sys.stderr)
