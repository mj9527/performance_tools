#!/bin/sh

echo "record_linux.sh [pid] [duration]"

if [ ! -d "perf_data" ];then
   mkdir 'perf_data'
   cd 'perf_data'
fi

if [ ! -d "FlameGraph" ];then
   git clone https://github.com/brendangregg/FlameGraph
fi

pid=$1
duration=$2

filename=linux_time_$(date +%Y%m%d)_$(date +%H%M%S)
mkdir $filename
cd $filename

perf record -F 99 -a -g -p $pid -o $filename.data -- sleep $duration
perf script -i $filename.data > $filename.perf

../FlameGraph/stackcollapse-perf.pl $filename.perf > $filename.stack

../FlameGraph/flamegraph.pl $filename.stack > $filename.svg
