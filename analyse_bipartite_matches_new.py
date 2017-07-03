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
import statistics
import sys

import skeleton_to_segments as skel

""" Returns path to skeleton of a certain time step """
def makeSkeletonPath(filename, t):
    # Prefix for reading the skeleton file that corresponds to a given set
    # of matches.
    skeletonPrefix = "viscfing_1-"

    skeletonPath =   os.path.abspath(filename+"/../../") + "/"\
                   + skeletonPrefix                           \
                   + ("%02d" % t)                             \
                   + ".txt"

    return skeletonPath

backwardMatches = collections.defaultdict(list)
forwardMatches  = collections.defaultdict(list)

# Stores all creation times of pixels in the previous time step. This is
# necessary in order to correctly propagate time information throughout
# the growth process.
previousCreationTime = dict()

# Partitions pixels in the current time step according to how they can
# be assigned to pixels in the subsequent time step.
created    = set()
destroyed  = set()
persisting = set()
growth     = set()

filename = sys.argv[1]
t        = 0

"""
Propagates creation time information to the pixels of the next time
step. This is central for calculating 'skeleton persistence'.
"""
def propagateCreationTimeInformation():
    # This dictionary stores the creation time of a pixel in the
    # subsequent time step.
    #
    # The creation time is either coming from a pixel in the previous
    # time step or it is set to the current time step.
    creationTime = dict()

    for (c,d) in persisting:
        (a,b)                 = forwardMatches[ (c,d) ][0]
        creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ (a,b) ]

    for (c,d) in growth:
        if forwardMatches[ (c,d) ]:
            (a,b)                 = forwardMatches[ (c,d) ][0]
            creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ (a,b) ]
        else:
            # If no forward matches exist but the pixel is a growth
            # pixel, there is at most one potential backward match.
            for (a,b) in backwardMatches:
                if (c,d) in backwardMatches[ (a,b) ]:
                    creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ (a,b) ] + 1

    unmatched = collections.defaultdict(list)
    for (a,b) in backwardMatches:
        for (c,d) in backwardMatches[ (a,b) ]:
            if (c,d) not in creationTime:
                unmatched[ (c,d) ].append( (a,b) )
    
    for (c,d) in unmatched:
        for (a,b) in unmatched[(c,d)]:
            creationTime[ (c,d) ] = 1 if t == 1 else min([previousCreationTime[(a,b)] for (a,b) in unmatched[(c,d)]])

    newCreationTime = dict()
    for (c,d) in creationTime:
        age        = creationTime[(c,d)]
        neighbours = skel.validNeighbours(c,d) 
        ages       = [ creationTime[(c,d)] for (c,d) in neighbours if (c,d) in creationTime ]

        # If the creation time of neighbouring pixels differs from the
        # creation time of the current pixel, it is adjusted.
        #
        # This is not the smartest adjustment because it does not take
        # directions into account. However, it is at least balanced as
        # it requires only a moderately large number of growth pixels.
        #
        # TODO: evaluate what happens when age differences are being
        #       checked
        if len(ages) >= 2 and sum(ages) != age*len(ages):
            newCreationTime[ (c,d) ] = min(age, min(ages))

    for (c,d) in newCreationTime:
        creationTime[ (c,d) ] = newCreationTime[ (c,d) ]

    #for l in backwardMatches.values():
    #    for (c,d) in l:
    #        if (c,d) not in creationTime:
    #            creationTime[ (c,d) ] = t+1

    return creationTime

""" main """
for filename in sys.argv[1:]:
    with open(filename) as f:

        # Skip all files that do not contain directed matching information.
        # This makes it easier for me to process a whole directory.
        if "directed" not in filename:
            continue

        # Note that matches for t=55 correspond to finding a matching
        # between time steps t=54 and t=55. Hence the subtraction.
        t = int( re.match(r'.*_(\d\d)_.*', filename ).group(1) )
        t = t-1

        print("Processing %s..." % filename, file=sys.stderr)

        for line in f:
            (a,b,direction,c,d) = line.split() 
            (a,b,c,d)           = ( int(a), int(b), int(c), int(d) )

            # Pixel (c,d) has at least one match, induced by the current time step,
            # hence there is some structure that persists until that time step.
            if direction == "->":
                forwardMatches[ (c,d) ].append( (a,b) )

            # Pixel (a,b) has at least one match, induced by the subsequent time
            # step, hence there is some structure that persists until that time
            # step.
            elif direction == "<-":
                backwardMatches[ (a,b) ].append( (c,d) )

    #
    # Find one-to-one matches. As this task is symmetrical by nature, it
    # suffices to traverse one of the dictionaries.
    #
    numOneToOneMatches = 0
    persisting         = set()

    for (a,b) in sorted( backwardMatches.keys() ):
        partners = backwardMatches[ (a,b) ]
        if len(partners) == 1:
            (c,d) = partners[0]
            if len(forwardMatches[ (c,d) ]) == 1:
                (e,f) = forwardMatches[ (c,d) ][0]
                if (a,b) == (e,f):
                    numOneToOneMatches += 1
                    persisting.add( (c,d) )

    numMatches = 10000

    print("One-to-one matches: %d/%d (%.3f)" % (numOneToOneMatches, numMatches, numOneToOneMatches / numMatches), file=sys.stderr)

    #
    # Find one-to-many matches
    #
    numOneToManyMatches = 0
    growth              = set()

    for (a,b) in sorted( backwardMatches.keys() ):
        partners = backwardMatches[ (a,b) ]
        isSingle = True
        for partner in partners:
            if partner in forwardMatches:
                neighbours = forwardMatches[partner]
                if len(neighbours) == 1:
                    if neighbours[0] != (a,b):
                        isSingle = False

        if isSingle:
            numOneToManyMatches += 1
            for (c,d) in partners:
                growth.add( (c,d) )

    print("One-to-many matches: %d/%d (%.3f)" % (numOneToManyMatches, numMatches, numOneToOneMatches / numMatches), file=sys.stderr)

    creationTime         = propagateCreationTimeInformation()
    previousCreationTime = creationTime

    for (c,d) in creationTime:
        print( "%d\t%d\t%d" % (c,d, creationTime[ (c,d) ]) )

    print("\n")

    backwardMatches.clear()
    forwardMatches.clear()
