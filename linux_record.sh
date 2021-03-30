#!/bin/sh

echo "record.sh [pid] [duraation]"


if [ ! -d "FlameGraph" ];then
   git clone https://github.com/brendangregg/FlameGraph
fi


filename=$(date +%Y%m%d)_$(date +%H%M%S)
mkdir $filename
cd $filename

perf record -F 99 -a -g -p $1 -o $filename.data -- sleep $2
perf script -i $filename.data > $filename.perf

../FlameGraph/stackcollapse-perf.pl $filename.perf > $filename.stack


../FlameGraph/flamegraph.pl $filename.stack > $filename.svg
