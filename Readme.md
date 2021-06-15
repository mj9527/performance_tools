# linux 火焰图生成工具
./record_linux.sh [pid] [duraation]

# ios 性能生成工具

./record_apple.sh [template] [device-uuid] [pid] [duration]

## 性能
./record_apple.sh  'Time Profiler' 5651 8000ms 6daac09469e94a24a2fa1f684bcd57963fd29c25 

## 内存
./record_apple.sh  'Leaks' 6daac09469e94a24a2fa1f684bcd57963fd29c25 5651 600s

## 电量
./record_apple.sh  'Energy Log' 6daac09469e94a24a2fa1f684bcd57963fd29c25 5651 600s


# 通用配置
os_type : 设置捕获操作系统类型
run_time : 采集时间

# windows 性能生成工具
1. windows_output_dir，设置捕获文件输出目录
2. wpt_dir, 设置wpt安装目录
3. 运行python windows_director.py


# 内存火焰图
../FlameGraph/stackcollapse.pl $filename.perf > $filename.stack

../FlameGraph/flamegraph.pl --color=mem $filename.stack > $filename.svg