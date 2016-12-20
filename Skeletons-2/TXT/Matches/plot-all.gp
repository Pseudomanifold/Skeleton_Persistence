do for [t = 2:84] {
  in  = sprintf('Matches_%02d.txt', t)
  out = sprintf('Matches_%02d.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set size ratio 0.5
  set key off
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  plot in using 1:2:($3-$1):($4-$2) with vectors
}

do for [t = 2:84] {
  in1 = sprintf('Matches_%02d_matched.txt',    t)
  in2 = sprintf('Matches_%02d_unmatched.txt', t)
  out = sprintf('Matches_%02d_decomposition.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set size ratio 0.5
  set terminal svg background rgb 'white' size 1000,1000
  set key inside
  set output out

  set pointsize 0.5

  plot in1 using 1:2 w p pt 7 title "t_{i-1}",\
       in1 using 3:4 w p pt 7 title "t_{i}",\
       in1 using 1:2:($3-$1):($4-$2) with vectors title "Greedy",\
       in2 using 1:2 w p pt 7 title "Unmatched"
}

do for [t = 2:84] {
  in  = sprintf('Matches_%02d_matched.txt', t)
  out = sprintf('Matches_%02d_matched.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set size ratio 0.5
  set terminal svg background rgb 'white' size 1000,1000
  set key off
  set output out

  set pointsize 0.5

  plot in using 1:2 w p pt 7,\
       in using 3:4 w p pt 7,\
       in using 1:2:($3-$1):($4-$2) with vectors,\
}
