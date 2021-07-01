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


def umdh_director(file_name, output_dir):
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    print 'all stack len ', len(std_stack_list)
    _, prefix = base_utils.get_work_dir_and_prefix(output_dir)
    stack_director.start_play(std_stack_list, prefix)


def instruments_director():
    _, prefix = base_utils.get_work_dir_and_prefix_with_config()
    trace_file, ret = record_apple.record_apple_config(prefix)
    if ret != 0:
        return

    print ('start parse content ', trace_file)
    time_file = content_parser.export_schema(trace_file, 'time-profile', prefix)

    # content_file = content_parser.export_content(trace_file, prefix)
    # schema_list = content_parser.parse_content(content_file)
    # content_parser.export_schema_list(trace_file, prefix, schema_list)

    # prefix = '/Users/mjzheng/Downloads/ios_data/2021-07-01_10_48_52/2021-07-01_10_48_52'
    # time_file = prefix + '_time-profile.xml'

    std_stack_list = time_profile_parser.parse_time_profile(time_file, prefix)
    stack_director.start_play(std_stack_list, prefix)


def unify_director(file_name, output_dir):
    lines = unify_input_file.read_std_flame_file(file_name)
    std_stack_list = unify_input_file.std_flame_to_std_stack(lines)
    _, prefix = base_utils.get_work_dir_and_prefix(output_dir)
    stack_director.start_play(std_stack_list, prefix)


def wpt_director():
    output_dir, csv_file, prefix = record_windows.record_export_with_config()
    # etl_file = "C:/Users/mjzheng/Documents/WPR Files/mjzheng-PC3.03-31-2021.19-28-35.etl"
    # prefix = setting.windows_output_dir + "12"
    # csv_file = record_windows.export_csv(setting.wpt_dir, etl_file, setting.windows_output_dir)

    json_file = prefix + '.json'
    etl_parser.csv_to_json(csv_file, json_file)

    flame_file = prefix + "_flame.html"
    sunburst_file = prefix + "_sunburst.html"
    stack_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    stack_graph.get_flamegrap_from_json(json_file, flame_file)
    return json_file


def chief_director():
    if setting.FILM_TYPE == 'win_memory':
        file_name = setting.WINDOWS_MEMORY_FILE
        output_dir = setting.WINDOW_MEMORY_OUTPUT_DIR
        umdh_director(file_name, output_dir)
    elif setting.FILM_TYPE == 'apple_cpu':
        instruments_director()
    elif setting.FILM_TYPE == 'std_stack':
        file_name = setting.STD_STACK_FILE
        output_dir = setting.STD_STACK_OUTPUT_DIR
        unify_director(file_name, output_dir)


if __name__ == "__main__":
    chief_director()
