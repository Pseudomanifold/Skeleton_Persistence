do for [t = 2:84] {
  load "/usr/share/gnuplot-colorbrewer/sequential/Reds.plt"

  in  = sprintf('t%02d_branch_persistence.txt', t)
  out = sprintf('Branch_persistence_t%02d.png', t)

  set xrange [0:800]
  set yrange [0:400]

  set cbr [0:3]

  unset border
  unset tics

  set key off
  set size ratio 0.5
  set terminal png background rgb 'white' size 1000,500
  set output out

  set margin 0,0,0,0

  set pointsize 0.5

  plot in using 1:2:3 with points lc rgb 'black' pt 7 ps 1.25,\
       in using 1:2:3 with points palette pt 7

  awk = sprintf("< awk '$3 <= %f {print $1, $2, $3}' %s", 0, in)
  out = sprintf('Branch_persistence_filtered_t%02d.png', t)

  set output out

  plot awk using 1:2:3 with points lc rgb 'black' pt 7 ps 1.25,\
       awk using 1:2:3 with points palette pt 7

}
