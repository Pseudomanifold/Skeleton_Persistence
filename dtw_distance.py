#!/usr/bin/env python3
#
# Simple implementation of dynamic time warping for two curves. This
# follows the implementation given in
#
#   https://en.wikipedia.org/wiki/Dynamic_time_warping
#
# with the addition of making the distance functor configurable.
#
# Usage : dtw_distance.py FILES
# Output: matrix of distances

import sys

def load_series(filename):
    Y = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            t,y  = [float(x) for x in line.split()]
            Y.append(y)

    return Y

def dist_euclidean(x,y):
    return (x-y)**2

def dtw_distance(S, T, dist = dist_euclidean):
    n   = len(S)
    m   = len(T)
    DTW = dict()

    for i in range(n):
        DTW[ ( i,-1) ] = float('inf')

    for j in range(m):
        DTW[ (-1, j) ] = float('inf')

    DTW[ (-1,-1) ] = 0

    for i in range(n):
        for j in range(m):
            cost       = dist(S[i], T[j])
            DTW[(i,j)] = cost + min(DTW[ (i-1,j  ) ],\
                                    DTW[ (i  ,j-1) ],\
                                    DTW[ (i-1,j-1) ])

    return DTW[ (n-1,m-1) ]

data = dict()
for filename in sys.argv[1:]:
    data[filename] = load_series(filename)

files = sorted(data.keys())
for i in range(len(files)):
    Yi = data[files[i]]
    for j in range(i+1,len(files)):
        Yj = data[files[j]]
        print(files[i],files[j],dtw_distance(Yi,Yj))
