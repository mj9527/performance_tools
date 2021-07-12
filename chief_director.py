import setting
import time
import base_utils
from stack_common import unify_input_file
from stack_common import stack_director
from windows_memory import umdh_file_parser
from ios_std import record_apple
from ios_std import content_parser
from ios_std import time_profile_parser
from windows import record_windows
from windows import csv_file_parser
from windows_memory import record_umdh
from simpleperf import analyze_cpu_usage


def umdh_director(file_name, prefix):
    if file_name == '':
        interval = setting.RUN_TIME
        file_name = record_umdh.record_interval(prefix, interval)
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    print 'all stack len ', len(std_stack_list)
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def instruments_director(prefix, system_type):
    uuid = setting.DEVICE_UUID
    bundle_id = setting.APP_ID
    template = setting.PROFILER_SUB_TYPE
    interval = setting.RUN_TIME * 1000
    trace_file, ret = record_apple.record_apple_config(prefix, system_type, uuid, bundle_id, template, interval)
    if ret != 0:
        return

    print ('start parse content ', trace_file)
    time_file = content_parser.export_schema(trace_file, 'time-profile', prefix)

    # content_file = content_parser.export_content(trace_file, prefix)
    # schema_list = content_parser.parse_content(content_file)
    # content_parser.export_schema_list(trace_file, prefix, schema_list)

    # prefix = '/Users/mjzheng/Downloads/ios_data/2021-07-01_10_48_52/2021-07-01_10_48_52'
    # time_file = prefix + '_time-profile.xml'

    std_stack_list = time_profile_parser.parse_time_profile(time_file, prefix, setting.SYMBOL_DICT)
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def unify_director(file_name, prefix):
    lines = unify_input_file.read_std_flame_file(file_name)
    std_stack_list = unify_input_file.std_flame_to_std_stack(lines)
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def wpt_director(output_dir, prefix):
    etl_file = prefix + '.etl'
    wpt_dir = setting.WPT_DIR
    interval = setting.RUN_TIME
    app_id = setting.APP_ID
    record_windows.record(wpt_dir, etl_file, interval)
    csv_file = record_windows.export_csv(wpt_dir, etl_file, output_dir)

    #csv_file = '/Users/mjzheng/Documents/mj_git/performance_tools/sample/CPU_Usage_(Sampled)_Utilization_by_Process,_Thread,_Stack.csv'
    std_stack_list = csv_file_parser.parse_csv_file(csv_file, app_id)
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def simple_perf_director(device_id, ndk_path, app_name, symbol_path, cap_time_sec):
    if not analyze_cpu_usage.copy_symbols_and_simpleperf_to_device(device_id, ndk_path, app_name, symbol_path):
        raise Exception("dump json file error!")

    time.sleep(10)

    json_file = "temp.json"
    analyze_cpu_usage.record_perfdata(app_name, json_file, device_id, cap_time_sec)


def chief_director():
    input_file = setting.PROFILER_INPUT_FILE
    output_dir = setting.SYSTEM_OUTPUT_DIR
    profiler_type = setting.PROFILER_TYPE
    system_type = setting.SYSTEM_TYPE
    output_dir, prefix = base_utils.get_work_dir_and_prefix(output_dir, profiler_type)
    if profiler_type == 'umdh':
        umdh_director(input_file, prefix)
    elif profiler_type == 'instrument':
        instruments_director(prefix, system_type)
    elif profiler_type == 'std_stack':
        unify_director(input_file, prefix)
    elif profiler_type == 'wpt':
        wpt_director(output_dir, prefix)
    elif profiler_type == 'simple_perf':
        device_id = 'fc107f89'
        ndk_path = '/Users/mjzheng/Library/Android/sdk/ndk/21.3.6528147'
        app_name = 'com.tencent.wemeet.app'
        sym_path = '/Users/mjzheng/Documents/meeting_android/app/app/Android/src/app/thirdparty/wmp/build/intermediates/merged_native_libs/debug/out/lib'
        simple_perf_director(device_id, ndk_path, app_name, sym_path, 10)


if __name__ == "__main__":
    chief_director()
