do for [t = 02:84] {
  in1 = sprintf('viscfing_1-%02d.txt', t-1)
  in2 = sprintf('viscfing_1-%02d.txt', t  )
  out = sprintf('Differences/viscfing_1-%02d.png', t  )

  set key off

  set xrange [0:839]
  set yrange [0:396]

  set margins 0,0,0,0

  unset tics
  unset border

  set size ratio 0.5
  set terminal pngcairo size 1000,500 background rgb 'white'

  set output out

  plot in1 with points pt 7 ps 2.0 lc rgb 'gray',\
       in2 with points pt 7 ps 0.5 lc rgb '#C41E3A'

  set output

  call = sprintf("mogrify %s -trim +repage", out)
  system(call)
}
