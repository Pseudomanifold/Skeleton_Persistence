do for [t = 2:84] {

  PREVIOUS = "#C41E3A"
  CURRENT  = "#4682B4"

  in_forward  = sprintf('Matches_%02d_forward.txt', t)
  in_backward = sprintf('Matches_%02d_backward.txt', t)
  out         = sprintf('Matches_%02d_directed_excerpt.svg', t)

  set xrange [375:400]
  set yrange [330:350]

  unset tics
  unset border
  set key off
  set terminal svg background rgb 'white' size 1000,1000

  set output out

  #plot in_forward  using 1:2:($3-$1):($4-$2) with vectors lw 0.1,\
  #     in_backward using 1:2:($3-$1):($2-$2) with vectors lw 0.1

  set pointsize 3

  #plot in_forward  using 1:2:($3-$1):($4-$2) with vectors lw 0.1,\
  #     in_backward using 1:2:($3-$1):($4-$2) with vectors lw 0.1
  
  plot in_forward  using 1:2 with points lc rgb PREVIOUS lw 1 pt 2 title "Previous",\
       in_backward using 1:2 with points lc rgb CURRENT lw 1 pt 6 title "Current",\
       in_forward  using 1:2:($3-$1):($4-$2) with vectors size 0.5,45 fixed lc rgb 'black' lw 2 notitle,\
       in_backward using 1:2:($3-$1):($4-$2) with vectors size 0.5,45 fixed lc rgb 'black' lw 2 notitle,\

}
