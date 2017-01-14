do for [t = 02:84] {
  load "YlOrRd.plt"
  set palette negative

  in  = sprintf('t%02d_branch_persistence.txt', t)
  out = sprintf('t%02d_branch_persistence.png', t)

  set key off

  set xrange [0:839]
  set yrange [0:396]

  set margins 0,0,0,0

  unset tics
  unset border

  set size ratio 0.5
  set terminal png background rgb 'white'

  set pointsize 0.25

  set cbr  [1:t]
  set output out

  plot in with points pt 7 lc rgb 'black' ps 0.8,\
       in with points palette pt 7 ps 0.75
}
