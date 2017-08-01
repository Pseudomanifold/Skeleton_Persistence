# Persistence Concepts for 2D Skeleton Evolution Analysis

This repository contains code & data for our publication &ldquo;[Persistence Concepts for 2D
Skeleton Evolution Analysis](http://bastian.rieck.ru/research/TopoInVis2017_Skeletons.pdf)&rdquo;,
which was accepted for the conference [*Topology-Based Methods in Visualization
2017*](http://fj.ics.keio.ac.jp/topoinvis).

At present, the code is rather unstructured. Expect additional instructions soon.

## Quickstart

Our analysis always has the same basic steps:

- Extract skeletons (this is not done by the code in this repository!)
- Obtain bipartite matches
- Analyse those bipartite matches in order to obtain *consistent*
  creation times for every pixel in the skeletons
- Calculate persistence-based concepts, such as *age persistence*, from
  the analysed matches

To obtain the matches, use the `make_assignments` script:

    $ ./make_assignments.py Simulation/Simulation_??.txt

Copy the resulting files `Matches_*_*.txt` to another folder. Next up,
we process the matches:

    $ ./process_matches.py Simulation/Matches/Matches_*.txt

This will create a set of *directed* matches, which is required for the
subsequent analysis and propagation of creation times. The propagation
of creation times is achieved via the following:

    $ ./analyse_bipartite_matches_new.py --width 1500 --height 1000 Simulation/Matches/*.txt > Ages_simulation.txt

Note that the script requires that you supply the width and height of
the input data. This is necessary in order to figure out neighbourhoods
in the skeleton. Afterwards, use the `split_output.py` utility script
from [Aleph](https://submanifold.github.io/Aleph), available [in the repository of Aleph](https://github.com/Submanifold/Aleph/blob/master/utilities/split_output.py),
to split the output file into smaller files:

    $ ./split_output.py --start=2 --prefix=t Ages_simulation.txt

You should now have a *list* of files, each corresponding to a given
time step, with consistent creation times. As a last step, you can
create persistence diagrams by issuing the following command:

    $ ./make_persistence_diagrams.py --width 1000 --height 1500 --prefix=Simulation_ --path Simulation Ages_t??.txt

The `path` and `prefix` parameters are required so that the script knows
where to find the skeletons. This will place a set of files in `/tmp`:


    /tmp/t*_age_persistence.txt:                age persistence values on the skeleton (x,y,p), with p denoting the persistence
    /tmp/t*_branch_persistence.txt:             ditto for branch persistence
    /tmp/t*_growth_persistence.txt:             ditto for growth persistence
    /tmp/t*_segment_branch_persistence_max.txt  age persistence diagram (incorrectly named maybe)
    /tmp/t*_segment_branch_persistence_min.txt  branch persistence diagram 

From this, various statistics, such as the *vivacity* of a process, can
be calculated. This is not (yet) documented, but please take a look at
the `Makefile` and the other scripts for more details.

## Questions

Please contact the [corresponding author](https://github.com/Submanifold) for more information.
