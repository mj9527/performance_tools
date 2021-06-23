# coding=utf-8

# public
run_time = 60  # 测试时间单位s
os_type = 'ios'
#os_type = 'windows'

# apple public
template = 'Time Profiler'
#template = 'Leaks'

# ios_std setting
# mj-6s
ios_uuid = '6daac09469e94a24a2fa1f684bcd57963fd29c25'  # iOS被测主机udid 没有则不填

# ipad
#ios_uuid = 'dfd530239e7e340e3874371707fbc71b0a04efb9'  # iOS被测主机udid 没有则不填

ios_app_bundle_id = 'com.tencent.meeting'
ios_output_dir = '/Users/mjzheng/Downloads/ios_data/'
symbol_dir = '/Users/mjzheng/Downloads/2.12.3.400/'
symbol_parse = 1


symbol_dict = {
    # 'xnn': symbol_dir,
    # 'WeMeetApp': symbol_dir,
    # 'wemeet_app_sdk': symbol_dir,
    # 'WeMeet': symbol_dir,
    # 'xcast': symbol_dir,
    # 'wemeet_base': symbol_dir,
    '/private/': symbol_dir,
    'System': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols',
    #Developer/usr/lib/libBacktraceRecording.dylib
    #/usr/lib/system/introspection/libdispatch.dylib
    '/usr/lib': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols'
}


# mac setting
mac_uuid = '117E51DA-23F9-59D7-88DF-90A4F3F402F4'
mac_app_bundle_id = '腾讯会议'
mac_output_dir = '/Users/mjzheng/Downloads/mac_data/'


# windows setting
# windows_output_dir = 'H:\\mj_git\\perf_data\\'
# wpt_dir = 'C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\'
windows_output_dir = 'H:/mj_git/perf_data/'
wpt_dir = 'C:/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit/'

#memory setting
input_memory_file = '//Users/mjzheng/Downloads/memory/213_bak/diff.txt'
output_memory_dir = '/Users/mjzheng/Downloads/memory/213_bak/'
business_module_list = ['wemeet_framework', 'wemeet_module_api', 'imsdk', 'xnn', 'wemeetapp', 'wemeet_sdk', 'wemeet_app_sdk', 'wemeet', 'libYTFaceTracker', 'xcast', 'wemeet_framework_common']
base_module_list = ['GF']

priority_module_list = [
    ['libYTFaceTracker', 'xcast', 'imsdk', 'imsdk'],
    ['wemeet_framework', 'wemeet_module_api', 'wemeetapp', 'wemeet_sdk', 'wemeet_app_sdk', 'wemeet', 'wemeet_framework_common'],
    ['GF']
]

module_to_start_func_ls = {
    'xcast': ['xc_cell_cycle_start', 'cycle_once', 'async_start', 'fire_event', 'task_run',
              'xc_signal_fire', 'xc_cell_fire_signal', 'thread_start', 'timer_node_run', 'timer_proc',
              'cycle_task', 'xc_thread_proc', 'worker_proc', 'uv_run', 'worker_thread_proc',
              'xcast_execute', 'xc_execute', 'xc_closure_run', 'do_start', 'anonymous'],
    'wemeet_sdk': ['_Do_call', 'lambda', 'operator()'],
}
top_func_size = 10



