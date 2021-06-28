# coding=utf-8

# public
RUN_TIME = 60  # 测试时间单位s
OS_TYPE = 'osx'

# apple public
INSTRUMENT_TEMPLATE = 'Time Profiler'

# ios_std setting
IOS_UUID = '6daac09469e94a24a2fa1f684bcd57963fd29c25'  # mj-6s uuid
#IOS_UUID = 'dfd530239e7e340e3874371707fbc71b0a04efb9'  # ipad4

IOS_BUNDLE_ID = '腾讯会议'
IOS_OUTPUT_DIR = '/Users/mjzheng/Downloads/ios_data/'

MAC_UUID = '117E51DA-23F9-59D7-88DF-90A4F3F402F4'
MAC_BUNDLE_ID = '腾讯会议'
MAC_OUTPUT_DIR = '/Users/mjzheng/Downloads/mac_data/'

SYMBOL_DIR = '/Users/mjzheng/Downloads/2.12.3.400/'
SYMBOL_PARSE = 1
SYMBOL_DICT = {
    '/private/': SYMBOL_DIR,
    'System': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols',
    '/usr/lib': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols'
}

# windows setting
WINDOWS_OUTPUT_DIR = 'H:/mj_git/perf_data/'
WPT_DIR = 'C:/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit/'

#memory setting
WINDOWS_MEMORY_FILE = '//Users/mjzheng/Downloads/memory/213_bak/diff.txt'
WINDOW_MEMORY_OUTPUT_DIR = '/Users/mjzheng/Downloads/memory/213_bak/'


# MODULE
BUSINESS_MODULE_LIST = ['wemeet_framework', 'wemeet_module_api', 'imsdk', 'xnn',
                        'wemeetapp', 'wemeet_sdk', 'wemeet_app_sdk', 'wemeet',
                        'libYTFaceTracker', 'xcast', 'wemeet_framework_common']
BASE_MODULE_LIST = ['GF']

PRIORITY_MODULE_LIST = [
    ['libYTFaceTracker', 'xcast', 'imsdk', 'imsdk'],
    ['wemeet_framework', 'wemeet_module_api', 'wemeetapp',
     'wemeet_sdk', 'wemeet_app_sdk', 'wemeet', 'wemeet_framework_common'],
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


