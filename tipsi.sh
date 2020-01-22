#!/usr/bin/env bash

activate lewis
source $HOME/epics.sh

lewis -a /Users/brambilla/work/estiasim -k lewissim motor -p "epics: {prefix: 'KM36:phytron:m1' }" >& phytron.log &
lewis -a /Users/brambilla/work/estiasim -k lewissim mdx5k -p "epics: {prefix: 'AE01:' }" >& power_supply.log &
lewis -a /Users/brambilla/work/estiasim -k lewissim wago -p "stream: {bind_address: 0.0.0.0, port: 9999}" >& wago.log &