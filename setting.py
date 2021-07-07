# coding=utf-8

DEVICE_UUID = '6daac09469e94a24a2fa1f684bcd57963fd29c25'  # mj-6s uuid
#DEVICE_UUID = 'dfd530239e7e340e3874371707fbc71b0a04efb9'  # ipad4
#DEVICE_UUID = '117E51DA-23F9-59D7-88DF-90A4F3F402F4'  #mac uuid

APP_ID = '腾讯会议'

SYSTEM_OUTPUT_DIR = '/Users/mjzheng/Downloads/performance_data'
#SYSTEM_OUTPUT_DIR = 'H:/mj_git/perf_data/'

SYSTEM_TYPE = 'ios'  #ios, mac, windows, linux

PROFILER_TYPE = 'std_stack'  # 'instrument', 'umdh', 'wpt', 'std_stack'
PROFILER_SUB_TYPE = 'Time Profiler'


#memory setting
#PROFILER_INPUT_FILE = '/Users/mjzheng/Downloads/memory/213_bak/6_5.txt'
PROFILER_INPUT_FILE = '/Users/mjzheng/Downloads/std_stack/sample1/36.txt'  # std_stack

# public
RUN_TIME = 60  # 测试时间单位s

SYMBOL_DIR = '/Users/mjzheng/Library/Developer/Xcode/DerivedData/WeMeetAppModules-fdaudevlzdviqxauhdkwveyajoft/Build/Products/Release-iphoneos/'
SYMBOL_DICT = {
    '/private/': SYMBOL_DIR,
    'System': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols',
    '/usr/lib': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols'
}

# windows setting
WPT_DIR = 'C:/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit/'


# MODULE
PRIORITY_MODULE_LIST = [
    ['wemeet_framework', 'wemeet_module_api', 'imsdk', 'xnn',
     'wemeetapp', 'wemeet_sdk', 'wemeet_app_sdk', 'wemeet',
     'libYTFaceTracker', 'xcast', 'wemeet_framework_common'],
    ['GF']
]

MODULE_TO_START_FUNC_LS = {
    'xcast': ['xc_cell_cycle_start', 'cycle_once', 'async_start', 'fire_event', 'task_run',
              'xc_signal_fire', 'xc_cell_fire_signal', 'thread_start', 'timer_node_run', 'timer_proc',
              'cycle_task', 'xc_thread_proc', 'worker_proc', 'uv_run', 'worker_thread_proc',
              'xcast_execute', 'xc_execute', 'xc_closure_run', 'do_start', 'anonymous'],
    'wemeet_sdk': ['_Do_call', 'lambda', 'operator()'],
}
TOP_FUNC_SIZE = 10
