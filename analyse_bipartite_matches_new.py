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
def printPixels(pixels):
    for (a,b) in pixels:
        print("%d\t%d" % (a,b))
    print("\n")

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

# Stores matches for the current time step (a) and the subsequent time
# step (b). The key is a pixel tuple here, while the value stores all
# the corresponding matches.
#
# Note that both structures are by necessity _directed_.
aMatches = collections.defaultdict(list)
bMatches = collections.defaultdict(list)

backwardMatches = collections.defaultdict(list)
forwardMatches  = collections.defaultdict(list)

# Stores all pixels in the current time step (a) that have a match in the
# subsequent time step. Note that this means that they have been found in
# the backward matching step. 
aHaveMatch = set()
bHaveMatch = set()

allEdges       = set()
oneToOneEdges  = set()
oneToManyEdges = set()
manyToOneEdges = set()

# Stores all creation times of pixels in the previous time step. This is
# necessary in order to correctly propagate time information throughout
# the growth process.
previousCreationTime = dict()

# Partitions pixels in the current time step according to how they can
# be assigned to pixels in the subsequent time step.
created    = set()
destroyed  = set()
persisting = set()

filename = sys.argv[1]
t        = 0

# FIXME: Debug flag for printing pixel classifications. Not sure whether
# I need this any more.
printClassifiedPixels = False

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
        partner               = forwardMatches[ (c,d) ][0]
        creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ partner ]

    for (c,d) in forwardMatches.keys():
        if (c,d) not in creationTime:
            creationTime[ (c,d) ] = t+1

    #for (c,d) in created:
    #    partner               = bMatches[ (c,d) ][0]
    #    creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ partner ]

    #for (c,d) in destroyed:
    #    creationTimes = [1]
    #    if t != 1:
    #        creationTimes = [ previousCreationTime[ (x,y) ] for (x,y) in bMatches[ (c,d) ] ]

    #    print( len(creationTimes), file=sys.stderr )
    #    creationTime[ (c,d) ] = min(creationTimes)

    #for (c,d) in bMatches:
    #    if (c,d) not in creationTime:
    #        creationTime[ (c,d) ] = t+1

    #for (a,b,c,d) in allEdges:
    #    # Unambiguous case: There is an exact match between two pixels,
    #    # so we just the previous creation time again.
    #    if (a,b,c,d) in oneToOneEdges:
    #        creationTime[ (c,d) ] = 1 if t == 1 else previousCreationTime[ (a,b) ]
    #    # One-to-many matching: One pixel with a known creation time has
    #    # been matched to multiple pixels with unknown creation times.
    #    #
    #    # FIXME: Not sure whether this is correct.
    #    elif (a,b,c,d) in oneToManyEdges:
    #        # Bailing out for now and treating the pixel as a new pixel. This
    #        # is probably the right way here.
    #        creationTime[ (c,d) ] = t+1

    #    # Many-to-one matching: A pixel in the subsequent time step has many
    #    # progenitors in the current time step. Here we have a choice between
    #    # choosing some creation time from the set of all creation times.
    #    elif (a,b,c,d) in manyToOneEdges:
    #        creationTimes         = [ previousCreationTime[ (x,y) ] for (x,y) in bMatches[ (c,d) ] ]
    #        creationTime[ (c,d) ] = min(creationTimes)

    #    # Irregular edges: No clear assignment possible to one time step. Here,
    #    # a majority vote of all possible creation times makes sense.
    #    elif (a,b,c,d) in irregularEdges:
    #        # FIXME: Does it make sense to go further here by jumping into the
    #        # first set, collect all matches in the second set, collect their
    #        # matches, and so on, until the process converges?
    #        if t == 1:
    #            creationTimes = [ 1 ] * len( bMatches[ (c,d) ] )
    #        else:
    #            creationTimes = [ previousCreationTime[ (x,y) ] for (x,y) in bMatches[ (c,d) ] ]
    #        creationTime[ (c,d) ] = max( creationTimes )
    #    else:
    #        creationTime[ (c,d) ] = t+1

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
                bHaveMatch.add( (c,d) )
                aMatches[ (a,b) ].append( (c,d) )
                forwardMatches[ (c,d) ].append( (a,b) )

            # Pixel (a,b) has at least one match, induced by the subsequent time
            # step, hence there is some structure that persists until that time
            # step.
            elif direction == "<-":
                aHaveMatch.add( (a,b) )
                bMatches[ (c,d) ].append( (a,b) ) 
                backwardMatches[ (a,b) ].append( (c,d) )

            allEdges.add( (a,b,c,d) )

    numMatches = len(allEdges)

    #
    # Find one-to-one matches. As this task is symmetrical by nature, it
    # suffices to traverse one of the dictionaries.
    #
    numOneToOneMatches = 0

    for (a,b) in sorted( backwardMatches.keys() ):
        partners = backwardMatches[ (a,b) ]
        if len(partners) == 1:
            (c,d) = partners[0]
            if len(forwardMatches[ (c,d) ]) == 1:
                numOneToOneMatches += 1
                persisting.add( (c,d) )

        #aPartners = aMatches[ (a,b) ]
        #if len(aPartners) == 1:
        #    (c,d)     = aPartners[0]
        #    bPartners = bMatches[ (c,d) ]

        #    if len(bPartners) == 1:
        #        numOneToOneMatches += 1
        #        oneToOneEdges.add( (a,b,c,d) )

        #        persisting.add( (c,d) )

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

                created.add( (c,d) )

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

                destroyed.add( (c,d) )

    print("Many-to-one matches: %d/%d (%.3f)" % (numManyToOneMatches, numMatches, numManyToOneMatches / numMatches), file=sys.stderr)

    #
    # Irregular edges
    #

    irregularEdges = allEdges - oneToOneEdges - oneToManyEdges - manyToOneEdges

    print("Irregular matches: %d/%d (%.3f)" % (len(irregularEdges), numMatches, len(irregularEdges) / numMatches), file=sys.stderr)

    #
    # Print "classified" pixels
    #

    if printClassifiedPixels:
        printPixels(persisting)
        printPixels(created)
        printPixels(destroyed)

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
    segments     = skel.getSegments(bSkeletonPath)

    # Stores age information about each segment
    ages          = collections.defaultdict(list)

    for index,segment in enumerate(segments):
        for pixel in segment:
            ages[index].append( creationTime.get( pixel, t+1) )

    print( "# t = %d" % t )

    for index in sorted( ages.keys() ):
        j = 0
        for (x,y) in segments[index]:
            print("%d\t%d\t%d" % (x,y, ages[index][j]))
            j += 1

    print("\n\n")

    previousCreationTime = creationTime

    # Cleanup for the next time step. This could possibly be solved more
    # elegantly, I guess.
    allEdges       = set()
    oneToOneEdges  = set()
    oneToManyEdges = set()
    manyToOneEdges = set()

    aMatches.clear()
    bMatches.clear()

    persisting.clear()
    created.clear()
