do for [t = 2:84] {
  in_forward  = sprintf('Matches_%02d_forward.txt', t)
  in_backward = sprintf('Matches_%02d_backward.txt', t)
  out         = sprintf('Matches_%02d_directed.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set size ratio 0.5
  #set key off
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  #plot in_forward  using 1:2:($3-$1):($4-$2) with vectors lw 0.1,\
  #     in_backward using 1:2:($3-$1):($2-$2) with vectors lw 0.1

  set pointsize 0.1

  #plot in_forward  using 1:2:($3-$1):($4-$2) with vectors lw 0.1,\
  #     in_backward using 1:2:($3-$1):($4-$2) with vectors lw 0.1
  
  plot in_forward  using 1:2 with points lw 0.1 title "Previous",\
       in_backward using 1:2 with points lw 0.1 title "Current",\
       in_forward  using 1:2:($3-$1):($4-$2) with vectors size 0.5,45 fixed lc rgb 'black' lw 0.1 notitle,\
       in_backward using 1:2:($3-$1):($4-$2) with vectors size 0.5,45 fixed lc rgb 'black' lw 0.1 notitle,\

}
