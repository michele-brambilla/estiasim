lewis -a /home/estiasim -k lewissim selene_motor -p "epics: {prefix:
'SQ:AMOR:SEL2:MIRROR'}" >& /tmp/selene/mirror &

#for i in $(seq 1 6)
#do
#  lewis -a /home/estiasim -k lewissim selene_motor -p "epics: {prefix:
#  'SQ:AMOR:SEL2:L$i'}" >& /tmp/selene/l$i &
#done
