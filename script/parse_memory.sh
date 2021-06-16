#!/bin/sh

echo "parse_memory.sh [file_name]"

filename=memory_$(date +%Y%m%d)_$(date +%H%M%S)
mkdir $filename
cd $filename

input_file=$1
cp ../$input_file $filename.perf

../FlameGraph/stackcollapse.pl $filename.perf > $filename.stack

../FlameGraph/flamegraph.pl --color=mem $filename.stack > $filename.svg
