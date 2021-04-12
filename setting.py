# coding=utf-8

# public
run_time = 10  # 测试时间单位s
template = 'Time Profiler'

# ios setting
ios_uuid = '6daac09469e94a24a2fa1f684bcd57963fd29c25'  # iOS被测主机udid 没有则不填
ios_app_bundle_id = 'com.tencent.meeting'
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

symbol_dir = '/Users/mjzheng/Library/Developer/Xcode/DerivedData/WeMeetApp-gdodaklaxocfarhhyqkxxdenrbft/Build/Products/Release-iphoneos/'

#module_file = '/Users/mjzheng/Downloads/ios_data/2021-04-08_17_23_22/20210408172529188_ori.crash'

module_file = '/Users/mjzheng/Downloads/ios_data/2021-04-12_10_26_28/20210412102753038_ori.crash'

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
