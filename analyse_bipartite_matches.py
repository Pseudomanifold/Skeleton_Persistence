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
import sys

""" Calculates the Euclidean distance between two pixels """
def distance( a,b,c,d ):
    return (a-c)**2 + (b-d)**2

# Stores matches for the current time step (a) and the subsequent time
# step (b). The key is a pixel tuple here, while the value stores all
# the corresponding matches.
#
# Note that both structures are by necessity _directed_.
aMatches = collections.defaultdict(list)
bMatches = collections.defaultdict(list)

numMatches = 0

with open(sys.argv[1]) as f:
    for line in f:
        (a,b,c,d) = [ int(x) for x in line.split() ]

        aMatches[ (a,b) ].append( (c,d) )
        bMatches[ (c,d) ].append( (a,b) )
        
        numMatches += 1

#
# Find one-to-one matches. As this task is symmetrical by nature, it
# suffices to traverse one of the dictionaries.
#

numOneToOneMatches = 0

for (a,b) in sorted( aMatches.keys() ):
    aPartners = aMatches[ (a,b) ]
    if len(aPartners) == 1:
        bPartners = bMatches[ aPartners[0] ]
        if len(bPartners) == 1:
            numOneToOneMatches += 1

print("One-to-one matches: %d/%d (%.3f)" % (numOneToOneMatches, numMatches, numOneToOneMatches / numMatches) )

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

print("One-to-many matches: %d/%d (%.3f)" % (numOneToManyMatches, numMatches, numOneToManyMatches / numMatches) )

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

print("Many-to-one matches: %d/%d (%.3f)" % (numManyToOneMatches, numMatches, numManyToOneMatches / numMatches) )

#
# Find many-to-many matches
#
