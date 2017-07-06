do for [t=0:82] {
  out = sprintf("/tmp/Frame_%02d.png", t)

  set key off
  set output out

  set xrange [0:839]
  set yrange [0:396]

  set cbr [1:84]

  set margins 0,0,0,0

  unset tics
  unset border

  set size ratio 0.5
  set terminal png background rgb 'white'

  set pointsize 0.25

  plot "Ages_new.txt" index t with points palette pt 7 ps 0.8
}
