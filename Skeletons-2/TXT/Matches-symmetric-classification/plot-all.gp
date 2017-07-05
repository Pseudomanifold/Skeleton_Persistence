do for [t = 2:84] {
  in  = sprintf('t%02d_classification.txt', t)
  out = sprintf('t%02d_classification.svg', t)

  set xrange [0:800]
  set yrange [0:400]

  set size ratio 0.5
  set terminal svg background rgb 'white' size 1000,1000
  set output out

  set pointsize 0.1

  plot in index 0 with points pt 7 title "Persisting",\
       "" index 1 with points pt 7 title "Decay",\
       "" index 2 with points pt 7 title "Growth",\
       "" index 3 with points pt 7 title "Irregular"
}

