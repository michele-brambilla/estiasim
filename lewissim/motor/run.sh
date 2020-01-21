#!/usr/bin/env bash

lewis -a /home/estiasim/ -k lewissim motor -p "epics: {prefix: 'PSI-ESTIARND:MC-MCU-01:m1' }" >& m1.out &

lewis -a /home/estiasim/ -k lewissim motor -p "epics: {prefix: 'PSI-ESTIARND:MC-MCU-01:m2' }" >& m2.out &
