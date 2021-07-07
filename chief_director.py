import setting
import base_utils
from stack_common import unify_input_file
from stack_common import stack_director
from stack_common import stack_graph
from windows_memory import umdh_file_parser
from ios_std import record_apple
from ios_std import content_parser
from ios_std import time_profile_parser
from windows import record_windows
from windows import etl_parser
from windows import csv_file_parser


def umdh_director(file_name, output_dir, prefix):
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    print 'all stack len ', len(std_stack_list)
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def instruments_director(output_dir, prefix):
    uuid = setting.DEVICE_UUID
    bundle_id = setting.APP_ID
    template = setting.PROFILER_SUB_TYPE
    interval = setting.RUN_TIME * 1000
    trace_file, ret = record_apple.record_apple_config(prefix, setting.SYSTEM_TYPE, uuid, bundle_id, template, interval)
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


def unify_director(file_name, output_dir, prefix):
    lines = unify_input_file.read_std_flame_file(file_name)
    std_stack_list = unify_input_file.std_flame_to_std_stack(lines)
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def wpt_director(output_dir, prefix):
    etl_file = prefix + '.etl'
    record_windows.record(setting.WPT_DIR, etl_file, setting.run_time)
    csv_file = record_windows.export_csv(setting.WPT_DIR, etl_file, output_dir)
    # etl_file = "C:/Users/mjzheng/Documents/WPR Files/mjzheng-PC3.03-31-2021.19-28-35.etl"
    # prefix = setting.windows_output_dir + "12"
    # csv_file = record_windows.export_csv(setting.wpt_dir, etl_file, setting.windows_output_dir)

    std_stack_list = csv_file_parser.parse_csv_file(csv_file, 'wemeetapp.exe')
    stack_director.start_play(std_stack_list, prefix, setting.PRIORITY_MODULE_LIST)


def chief_director():
    input_file = setting.PROFILER_INPUT_FILE
    output_dir = setting.SYSTEM_OUTPUT_DIR
    profiler_type = setting.PROFILER_TYPE
    system_type = setting.SYSTEM_TYPE
    output_dir, prefix = base_utils.get_work_dir_and_prefix(output_dir, system_type, profiler_type)
    if profiler_type == 'umdh':
        umdh_director(input_file, output_dir, prefix)
    elif profiler_type == 'instrument':
        instruments_director(output_dir, prefix)
    elif profiler_type == 'std_stack':
        unify_director(input_file, output_dir, prefix)
    elif profiler_type == 'wpt':
        wpt_director(output_dir, prefix)


if __name__ == "__main__":
    chief_director()
