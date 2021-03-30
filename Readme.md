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
