load "/usr/share/gnuplot-colorbrewer/sequential/Reds.plt"

unset colorbox
unset key
unset tics
unset border

set lmargin 0.5
set bmargin 0.5
set tmargin 0.25
set rmargin 0

set xrange [0:800]
set yrange [0:400]

do for [t = 2:84] {

  set cbr [-t:0];

  in  = sprintf('t%02d_growth_persistence.txt', t)
  out = sprintf('t%02d_growth_persistence.png', t)

  set terminal png background rgb 'white' size 1000
  set output out

  plot in with points pt 7 lc rgb 'black' ps 1.25,\
       in using 1:2:3 with points palette pt 7
}
