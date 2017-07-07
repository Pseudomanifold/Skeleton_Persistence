#!/usr/bin/env python3

import re
import sys

for filename in sys.argv[1:]:
    print("Processing %s..." % filename, file=sys.stderr)
    with open(filename) as f:
        t = int( re.match(r'.*t(\d\d).*', filename ).group(1) )

        num_pixels        = 0
        num_active_pixels = 0

        for line in f:
            line       = line.rstrip()
            x,y,g      = [ int(a) for a in line.split() ]
            num_pixels = num_pixels + 1

            # TODO: range (?)
            if g >= -10:
                num_active_pixels = num_active_pixels + 1

        print("%02d %f" % (t, num_active_pixels / num_pixels ))
