#!/bin/sh

echo  $0 " [template] [pid] [duration] [device-uuid]"

if [ $# == 0 ]; then
    echo  $0 " [template] [pid] [duration] [device-uuid]"
    exit 1;
fi

template=$1
pid=$2
duration=$3
device=$4

if [ ! -d "perf_data" ];then
   mkdir 'perf_data'
   cd 'perf_data'
fi

if [ ! $device ]; then
    echo 'run mac'
    filename=mac_time_$(date +%Y%m%d)_$(date +%H%M%S)
    mkdir $filename
    cd $filename
    xcrun xctrace record --template 'Time Profiler' --attach $pid --output $filename.trace --time-limit $duration
else
    echo 'run ios'
    filename=ios_time_$(date +%Y%m%d)_$(date +%H%M%S)
    mkdir $filename
    cd $filename
    xcrun xctrace record --template 'Time Profiler' --attach $pid --device $device --output $filename.trace --time-limit $duration
fi
