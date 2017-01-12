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

""" Calculates the Euclidean distance between two pixels """
def distance( a,b,c,d ):
    return (a-c)**2 + (b-d)**2

""" Prints a set of pixels """
def printPixels(name, pixels, f):
    print("# %s" % name, file=f)
    if pixels:
        for (a,b) in pixels:
            print("%d\t%d" % (a,b), file=f)
    else:
        # Print a dummy pixel to ensure that gnuplot is able to display
        # the index correctly
        print("0\t0", file=f)
    print("\n", file=f)

"""
Updates a set of unmatched pixels. Traverses a skeleton file and checks whether
a match exists. If not, the pixel is added to a set.
"""
def findUnmatchedPixelsInSkeleton(matches, filename):
    unmatched = set()
    n         = 0
    with open(filename) as f:
        for line in f:
            (x,y) = [ int(a) for a in line.split() ]
            if (x,y) not in matches:
                unmatched.add( (x,y) )
            n += 1

    return unmatched, n

# Stores all pixels of the current time (t0) and the subsequent time
# step (t1). This is necessary to assign proper creation times.
pixelsT0 = set()
pixelsT1 = set()

# Stores which pixels have been matched by other pixels. The key is
# a pixel from the current time step, while the value contains all
# pixels from the subsequent time step that match said pixel.
matchedT0 = collections.defaultdict(list)
matchedT1 = collections.defaultdict(list)

# Stores all creation times of pixels in the previous time step. This is
# necessary in order to correctly propagate time information throughout
# the growth process.
previousCreationTime = dict()

# Partitions pixels in the current time step according to how they can
# be assigned to pixels in the subsequent time step.
persisting = set()
growth     = set()
decay      = set()

filename = sys.argv[1]
t        = 0

# FIXME: Debug flag for printing pixel classifications. Not sure whether
# I need this any more.
printClassifiedPixels = False

"""
Finds the partner of a pixel in the subsequent time step when that pixel
has no direct match.
"""
def findPartnersT0(pixel):
    (c,d)    = pixel
    partners = list()
    for (a,b) in sorted( matchedT0.keys() ):
        if (c,d) in matchedT0[ (a,b) ]:
            partners.append( (a,b) )

    return partners

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

    for (c,d) in pixelsT1:
        # For persisting pixels, we only have the opportunity to keep the
        # creation time.
        if (c,d) in persisting:
            partner               = matchedT1[ (c,d) ][0]
            creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ partner ]

        # For growth pixels, there is only a single partner in the
        # current time step, so we have to copy its creation time.
        elif (c,d) in growth:
            partners = matchedT1[ (c,d) ]

            # If the pixel has not been matched at all, search for
            # a partner in the current time step.
            if not partners:
                partners = findPartnersT0( (c,d) )

            partner               = partners[0]
            creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ partner ]
        # For decay pixels, there are multiple partners in the current
        # time step, so we use the oldest one.
        elif (c,d) in decay:
            partners              = matchedT1[ (c,d) ]
            times                 = [ previousCreationTime[ partner ] for partner in partners ]
            creationTime[ (c,d) ] = min(times)

        # Set the creation time of all other pixels to the subsequent time
        # step. Ideally, the amount of pixels treated like this should be
        # extremely small.
        else:
            creationTime[ (c,d) ] = t+1

    return creationTime

""" main """
for filename in sys.argv[1:]:
    with open(filename) as f:

        #
        # Cleanup
        #

        matchedT0.clear()
        matchedT1.clear()

        pixelsT0.clear()
        pixelsT1.clear()

        persisting.clear()
        growth.clear()
        decay.clear()

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

            # FIXME: Not sure whether I need the pixels from the current
            # time step as well, but it cannot hurt...
            pixelsT0.add( (a,b) )
            pixelsT1.add( (c,d) )

            # Pixel (c,d) has at least one match, induced by the current time step,
            # hence there is some structure that persists until that time step.
            if direction == "->":
                matchedT1[ (c,d) ].append( (a,b) )

            # Pixel (a,b) has at least one match, induced by the subsequent time
            # step, hence there is some structure that persists until that time
            # step.
            elif direction == "<-":
                matchedT0[ (a,b) ].append( (c,d) )

    #
    # Find one-to-one matches
    #

    numOneToOneMatches = 0

    for (a,b) in sorted( matchedT0.keys() ):
        partnersT1 = matchedT0[ (a,b) ] # All pixels in the subsequent time step
                                        # that match to the current pixel

        if len(partnersT1) == 1:
            (c,d)      = partnersT1[0]
            partnersT0 = matchedT1[ (c,d) ] # All pixels in the current time step
                                            # that match to the current pixel

            if len(partnersT0) == 1 and partnersT0[0] == (a,b):
                numOneToOneMatches += 1
                persisting.add( (c,d) )

    print("One-to-one matches: %d/%d (%.3f)" % (len(persisting), len(pixelsT1), len(persisting) / len(pixelsT1) ), file=sys.stderr)

    #
    # Find one-to-many matches: Multiple pixels in the subsequent time
    # step match the same pixel in the current time step. The pixel in
    # the current time step matches one of them.
    #

    for (a,b) in sorted( matchedT0.keys() ):
        partnersT1  = matchedT0[ (a,b) ]

        # If the pixel is matched by at most one other pixel, it cannot
        # be part of a true one-to-many matching.
        if len(partnersT1) <= 1:
            continue

        # Indicates that at most one single pixel in the current time
        # step matches the pixel in the subsequent time step.
        singleMatch = True

        for (c,d) in partnersT1:
            partnersT0 = matchedT1[ (c,d) ]

            # If there is a partner in the current time step it must by
            # necessity be the pixel (a,b).
            if len(partnersT0) == 1 and partnersT0[0] != (a,b):
                singleMatch = False
            elif len(partnersT0) > 1:
                singleMatch = False

        if singleMatch:
            growth.update( partnersT1 )

    print("One-to-many matches: %d/%d (%.3f)" % (len(growth), len(pixelsT1), len(growth) / len(pixelsT1) ), file=sys.stderr)

    #
    # Find many-to-one matches
    #

    numManyToOneMatches = 0

    for (c,d) in sorted( matchedT1.keys() ):
        partnersT0  = matchedT1[ (c,d) ]

        # If the pixel is matched by at most one other pixel, it cannot
        # be part of a true one-to-many matching.
        if len(partnersT0) <= 1:
            continue

        # Indicates that at most one single pixel in the subsequent time
        # step matches the pixel in the current time step.
        singleMatch = True

        for (a,b) in partnersT0:
            partnersT1 = matchedT0[ (a,b) ]

            # If there is a partner in the subsequent time step it must
            # by necessity be the pixel (c,d).
            if len(partnersT1) == 1 and partnersT1[0] != (c,d):
                singleMatch = False
            elif len(partnersT1) > 1:
                singleMatch = False

        if singleMatch:
            decay.add( (c,d ) )

    print("Many-to-one matches: %d/%d (%.3f)" % (len(decay), len(pixelsT1), len(decay) / len(pixelsT1) ), file=sys.stderr)

    irregularPixels = pixelsT1 - persisting - growth - decay

    assert len(irregularPixels) ==   len(pixelsT1)   \
                                   - len(persisting) \
                                   - len(growth)     \
                                   - len(decay)

    #
    # Print "classified" pixels
    #

    outputClassification = "/tmp/t%02d_classification.txt" % (t+1)

    with open(outputClassification, "w") as g:
        printPixels("Persisting", persisting, g)
        printPixels("Decay"     , decay     , g)
        printPixels("Growth"    , growth    , g)

    #
    # Load the skeleton of the current time step and of the previous time step. Use
    # this to determine structures that have been created (unmatched pixels in the
    # forward matching) or destroyed (unmatched pixels in the backward matching).
    #

    aSkeletonPath = makeSkeletonPath(filename,t  )
    bSkeletonPath = makeSkeletonPath(filename,t+1)

    #
    # Propagate creation time information to the pixels and, subsequently,
    # to the segments. Afterwards, let's check whether there are segments
    # for which an age can be determined.
    #

    creationTime = propagateCreationTimeInformation()

    # Stores age information about each segment
    if False:
        ages          = collections.defaultdict(list)
        segments      = skel.getSegments(bSkeletonPath)

        for index,segment in enumerate(segments):
            for pixel in segment:
                ages[index].append( creationTime.get( pixel, t+1) )

    outputAges = "/tmp/t%02d_ages.txt" % (t+1)

    with open(outputAges, "w") as g:
        for (x,y) in creationTime:
            print("%d\t%d\t%d" % (x,y, creationTime[ (x,y) ]), file=g)

    previousCreationTime = creationTime
