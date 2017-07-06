set xrange [0:839]
set yrange [0:396]

set margins 0,0,0,0
set size ratio 0.5

unset border
unset key
unset tics
unset colorbox

set terminal png size 1000,520 background rgb 'white'

set output "Skeleton_glyph.png"
plot "viscfing_1-42.txt" with points pt 7 lc rgb 'black'

load "/usr/share/gnuplot-colorbrewer/sequential/Reds.plt"

set pointsize 0.5

set output "Skeleton_ages_glyph.png"
plot "Matches-symmetric-pixel-ages-new/Ages_t42.txt" with points pt 7 lc rgb 'black' ps 1.25,\
     ""                                              with points palette pt 7 
