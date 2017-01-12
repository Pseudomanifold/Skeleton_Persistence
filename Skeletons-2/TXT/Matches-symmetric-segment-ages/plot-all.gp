do for [t = 2:84] {
  in  = sprintf('t%02d_segment_ages.txt', t)
  out = sprintf('t%02d_segment_ages.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set cbr [1:84]

  set key off
  set size ratio 0.5
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  set pointsize 0.5

  plot in with points palette pt 7
}

