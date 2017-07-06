#!/usr/bin/env python3
#
# Takes a set of pixel images tagged with ages and calculates all
# derived persistence-based concepts for them.

import argparse
import collections
import os
import re
import statistics
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

print("Assuming a shape of (%d,%d)" % (skel.width, skel.height), file=sys.stderr)

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

""" Stores a persistence diagram. """
def storePersistenceDiagram(name, persistenceDiagram):
    filename = "/tmp/t%02d_%s.txt" % (t+1, name)
    with open(filename, "w") as f:
        for p,count in persistenceDiagram.most_common():
            (x,y) = p

            # The corresponding branch point creation time must not be
            # higher than the segment age. These inconsistencies occur
            # sometimes; the lazy way to handle them requires changing
            # the branch creation time.
            #
            # If we apply some neighbour-based smoothing in the future
            # these points will automatically disappear.
            if x > y:
                pass

            print("%d\t%d\t%d" % (x,y,count), file=f)


""" main """
for filename in arguments.FILES:
    with open(filename) as f:
        print("Processing %s..." % filename)

        # Note that matches for t=55 correspond to finding a matching
        # between time steps t=54 and t=55. Hence the subtraction.
        t = int( re.match(r'.*_t(\d\d).*', filename ).group(1) )
        t = t-1

        skeletonPath             = makeSkeletonPath(filename,t+1)
        segments, branchVertices = skel.getSegments(skeletonPath, appendBranchVertices=True)
        ages                     = collections.defaultdict(list)

        # Read the creation times of pixels. If this information is
        # available, any other information can be derived from it.
        creationTime = dict()
        for line in f:
            if line.rstrip():
                x,y,time            = [int(a) for a in line.split()]
                creationTime[(x,y)] = time

        for index,segment in enumerate(segments):
            for pixel in segment:
                # Do not consider branch vertices for determining creation
                # times. Else, the propagation of ages along segments will
                # not work correctly.
                if pixel not in branchVertices:
                    ages[index].append( creationTime[pixel] )

        outputSegmentAges              = "/tmp/t%02d_segment_ages.txt" % (t+1)
        outputSegmentBranchPersistence = "/tmp/t%02d_branch_persistence.txt" % (t+1)
        outputSegmentAgePersistence    = "/tmp/t%02d_age_persistence.txt" % (t+1)
        outputSegmentGrowthPersistence = "/tmp/t%02d_growth_persistence.txt" % (t+1)

        pdBranchPersistenceMin  = collections.Counter()
        pdBranchPersistenceMean = collections.Counter()
        pdBranchPersistenceMax  = collections.Counter()

        numIsolatedSegments     = 0

        with open(outputSegmentAges,     "w")          as g,\
             open(outputSegmentBranchPersistence, "w") as h,\
             open(outputSegmentAgePersistence, "w")    as i,\
             open(outputSegmentGrowthPersistence, "w") as j:
            for index,segment in enumerate(segments):
                branchCreationTime      = 1000

                segmentCreationTimeMin  = min(ages[index])
                segmentCreationTimeMean = statistics.mean(ages[index])
                segmentCreationTimeMax  = max(ages[index])

                for (x,y) in segment:

                    print("%d\t%d\t%d" % (x,y,segmentCreationTimeMin), file=g)
                    if (x,y) in branchVertices:
                        branchCreationTime = min(branchCreationTime, creationTime[ (x,y) ])

                for (x,y) in segment:
                    mode = min(ages[index])
                    #try:
                    #    mode = statistics.mode( ages[index] )
                    #except statistics.StatisticsError:
                    #    mode = statistics.mean( ages[index] )

                    branchPersistence = abs(mode - branchCreationTime)
                    agePersistence    = abs(segmentCreationTimeMax - branchCreationTime)
                    growthPersistence = abs(segmentCreationTimeMax - (t+1))
                    print("%d\t%d\t%d" % (x,y,branchPersistence), file=h)
                    print("%d\t%d\t%d" % (x,y,agePersistence),    file=i)
                    print("%d\t%d\t%d" % (x,y,growthPersistence), file=j)

                # If no branch point exists, the segment is isolated. This
                # may be interesting for some applications.
                if branchCreationTime == 1000:
                    numIsolatedSegments += 1

                # Increase multiplicity of all points
                pdBranchPersistenceMin[  (branchCreationTime, segmentCreationTimeMin) ] += 1
                pdBranchPersistenceMean[ (branchCreationTime, segmentCreationTimeMean) ] += 1
                pdBranchPersistenceMax[  (branchCreationTime, segmentCreationTimeMax) ] += 1

        # Store persistence diagram along with multiplicities
        storePersistenceDiagram( "segment_branch_persistence_min" , pdBranchPersistenceMin )
        storePersistenceDiagram( "segment_branch_persistence_mean", pdBranchPersistenceMean )
        storePersistenceDiagram( "segment_branch_persistence_max" , pdBranchPersistenceMax )

