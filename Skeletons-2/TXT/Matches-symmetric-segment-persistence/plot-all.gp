do for [t = 2:84] {

  load "~/Local/gnuplot-colorbrewer/sequential/Greys.plt"

  in  = sprintf('t%02d_segment_persistence.txt', t)
  out = sprintf('t%02d_segment_persistence.svg', t)

  set xrange [0:85]
  set yrange [0:85]

  set key off;

  set size square
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  set pointsize 1.0

  plot in with points palette pt 7 lc rgb black, x with l lc rgb 'black'
}

