#!/usr/bin/env python3

from skimage.color      import rgb2gray
from skimage.filters    import threshold_otsu
from skimage.morphology import skeletonize
from skimage            import io

import sys

for filename in sys.argv[1:]:
    image    = io.imread(filename)
    image    = rgb2gray(image)
    binary   = image > threshold_otsu(image)
    skeleton = skeletonize(image)

    rows, columns = skeleton.shape

    for row in range(rows):
        for column in range(columns):
            if skeleton[row,column]:
                print(row,column)

