do for [t = 2:84] {
  in  = sprintf('Matches_%02d.txt', t)
  out = sprintf('Matches_%02d.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set size ratio 0.5
  set key off
  set terminal svg size 1000,1000
  set output out

  plot in using 1:2:($3-$1):($4-$2) with vectors
}
