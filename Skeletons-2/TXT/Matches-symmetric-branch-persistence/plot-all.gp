do for [t = 2:84] {

  load "~/Local/gnuplot-colorbrewer/sequential/Greys.plt"
  set palette negative

  in  = sprintf('t%02d_segment_branch_persistence_min.txt', t)
  out = sprintf('t%02d_segment_branch_persistence_min.svg', t)

  set xrange [0:85]
  set yrange [0:85]

  set key off;

  set size square
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  plot in with points lc rgb 'black' pt 7 ps 1.25,\
       "" with points palette pt 7 ps 1.0,        \
        x with l lc rgb 'black'
}

do for [t = 2:84] {

  load "~/Local/gnuplot-colorbrewer/sequential/Greys.plt"
  set palette negative

  in  = sprintf('t%02d_segment_branch_persistence_mean.txt', t)
  out = sprintf('t%02d_segment_branch_persistence_mean.svg', t)

  set xrange [0:85]
  set yrange [0:85]

  set key off;

  set size square
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  plot in with points lc rgb 'black' pt 7 ps 1.25,\
       "" with points palette pt 7 ps 1.0,        \
        x with l lc rgb 'black'
}

do for [t = 2:84] {

  load "~/Local/gnuplot-colorbrewer/sequential/Greys.plt"
  set palette negative

  in  = sprintf('t%02d_segment_branch_persistence_max.txt', t)
  out = sprintf('t%02d_segment_branch_persistence_max.svg', t)

  set xrange [0:85]
  set yrange [0:85]

  set key off;

  set size square
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  plot in with points lc rgb 'black' pt 7 ps 1.25,\
       "" with points palette pt 7 ps 1.0,        \
        x with l lc rgb 'black'
}
