load "/usr/share/gnuplot-colorbrewer/sequential/Reds.plt"

in  = 't69_segment_branch_persistence_max.txt'
out = 't69_age_persistence_diagram.pdf'

set xrange [0:85]
set yrange [0:85]

set key off;
set border 3
set tics nomirror

set size square
set terminal pdf font "Times New Roman" background rgb 'white' size 10cm,10cm
set output out

set lmargin 2
set bmargin 2
set tmargin 0
set rmargin 0

plot in with points pt 7 ps 1.0 lc rgb 'black',\
     x with l lc rgb 'black'


in  = 't69_segment_branch_persistence_min.txt'
out = 't69_branch_persistence_diagram.pdf'

plot in with points pt 7 ps 1.0 lc rgb 'black',\
     x with l lc rgb 'black'
