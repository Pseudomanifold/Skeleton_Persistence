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

awk = sprintf("< awk '($1-$2)^2 <= %f {print $1, $2, $3}' %s", 10, in)

set lmargin 2
set bmargin 2
set tmargin 0
set rmargin 0

plot in with points pt 7 ps 1.0 lc rgb 'black',\
     awk with points pt 7 ps 1.0 lc rgb '#C41E3A',\
     x with l lc rgb 'black'


in  = 't69_segment_branch_persistence_min.txt'
out = 't69_branch_persistence_diagram.pdf'

awk = sprintf("< awk '($1-$2)^2 >= %f {print $1, $2, $3}' %s", 10, in)

plot in with points pt 7 ps 1.0 lc rgb 'black',\
     awk with points pt 7 ps 1.0 lc rgb '#C41E3A',\
     x with l lc rgb 'black'

#
# Skeletons
#

reset

in  = 't69_branch_age_persistence.txt'
out = 't69_branch_persistence.png'

set terminal png  background rgb 'white'
set output out

set xrange [0:680]
set yrange [0:396]

set size ratio 0.7
set pointsize 0.5

set cbr [0:5]
unset colorbox

set margins 0.1,0,0,0

unset tics
unset border
unset key

load "/usr/share/gnuplot-colorbrewer/sequential/Reds.plt"

#set pointsize 0.25

plot in with points pt 7 lc rgb 'black' ps 1.25,\
     in using 1:2:(abs($3)) with points palette pt 7


out = 't69_branch_persistence_filtered.png'
set output out

#awk = sprintf("< awk '($3) >= %f || $3 <= %f || $4 >= 1 {print $1, $2, $3}' %s", 0, -2, in)

awk = sprintf("< awk '$3 > -2 && $3 <= 2 {print $1, $2, $3}' %s", in)

plot awk with points pt 7 lc rgb 'black' ps 1.25,\
     awk using 1:2:(abs($3)) with points palette pt 7

out = 't69_branch_persistence_filtered_combined.png'
set output out

awk = sprintf("< awk '($3) >= %f || $3 <= %f || $4 >= 1 {print $1, $2, $3}' %s", 0, -2, in)

plot awk with points pt 7 lc rgb 'black' ps 1.25,\
     awk with points palette pt 7

out = 't69_age_persistence.png'
set output out

set cbr [0:20]

plot in with points pt 7 lc rgb 'black' ps 1.25,\
     in using 1:2:(abs($4)) with points palette pt 7

out = 't69_age_persistence_filtered.png'
set output out

awk = sprintf("< awk '$4 > 5 || $4 < -2 {print $1, $2, $4}' %s", in)

#plot awk with points pt 7 lc rgb 'black' ps 1.25,\

plot awk with points pt 7 lc rgb 'black' ps 1.25,\
     awk using 1:2:(abs($3)) with points palette pt 7

set output
