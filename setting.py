# coding=utf-8

DEVICE_UUID = ''  # get according system_type, valid in apple os
APP_ID = '腾讯会议'

SYSTEM_OUTPUT_DIR = '/Users/mjzheng/Downloads/performance_data'
#SYSTEM_OUTPUT_DIR = 'H:/mj_git/perf_data/'

SYSTEM_TYPE = 'ios'  #ios, mac, windows, linux

PROFILER_TYPE = 'instrument'  # 'instrument', 'umdh', 'wpt', 'std_stack'
PROFILER_SUB_TYPE = 'Time Profiler'


#memory setting
#PROFILER_INPUT_FILE = '/Users/mjzheng/Documents/mj_git/performance_tools/sample/CPU_Usage_(Sampled)_Utilization_by_Process,_Thread,_Stack.csv'  # std_stack
PROFILER_INPUT_FILE = '/Users/mjzheng/Documents/mj_git/performance_tools/sample/udmh_wemeet_sample.txt'

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
