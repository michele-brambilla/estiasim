#!/usr/bin/env bash

lewis -a /Users/brambilla/work/estiasim -k lewissim motor -p "epics: {prefix: 'KM36:phytron:m1' }" >& phytron.log &
lewis -a /Users/brambilla/work/estiasim -k lewissim mdx5k -p "epics: {prefix: 'AE01:' }" >& power_supply.log &

