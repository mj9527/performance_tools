# coding=utf-8

# public
run_time = 600  # 测试时间单位s
template = 'Time Profiler'

# ios setting
ios_uuid = '6daac09469e94a24a2fa1f684bcd57963fd29c25'  # iOS被测主机udid 没有则不填
ios_app_bundle_id= 'com.tencent.meeting'
ios_output_dir = '/Users/mjzheng/Downloads/ios_data/'

# mac setting
mac_uuid = '117E51DA-23F9-59D7-88DF-90A4F3F402F4'
mac_app_bundle_id = '腾讯会议'
mac_output_dir = '/Users/mjzheng/Downloads/mac_data/'

# windows setting
# windows_output_dir = 'H:\\mj_git\\perf_data\\'
# wpt_dir = 'C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\'


windows_output_dir = 'H:/mj_git/perf_data/'
wpt_dir = 'C:/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit/'

apple_type='ios'

symbol_dict = {
    'xnn': '',
    'WeMeetApp': '',
    'wemeet_app_sdk': '',
    'WeMeet': '',
    'xcast': '',
    'wemeet_base': '',
    'System': '/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols'
}



