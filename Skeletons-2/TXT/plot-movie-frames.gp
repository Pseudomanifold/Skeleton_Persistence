do for [t = 02:84] {
  in  = sprintf('viscfing_1-%02d.txt', t)
  out = sprintf('viscfing_1-%02d.png', t)

  set key off

  set xrange [0:839]
  set yrange [0:396]

  set margins 0,0,0,0

  unset tics
  unset border

  set size ratio 0.5
  set terminal png background rgb 'white'

  set pointsize 0.25

  set output out

  plot in with points pt 7 lc rgb 'black' ps 0.8
}
