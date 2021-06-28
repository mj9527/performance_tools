# coding=utf-8
import sys
sys.path.append("..")
import record_apple
import content_parser
import time_profile_parser
import base_utils
from stack_common import stack_director
from stack_common import unify_input_file


def start():
    _, prefix = base_utils.get_work_dir_and_prefix_with_config()
    trace_file, ret = record_apple.record_apple_config(prefix)
    if ret != 0:
        return

    print ('start parse content ', trace_file)
    time_file = content_parser.export_schema(trace_file, 'time-profile', prefix)

    # content_file = content_parser.export_content(trace_file, prefix)
    # schema_list = content_parser.parse_content(content_file)
    # content_parser.export_schema_list(trace_file, prefix, schema_list)

    # prefix = '/Users/mjzheng/Downloads/ios_data/2021-06-18_12_44_23/2021-06-18_12_44_23'
    # time_file = prefix + '_time-profile.xml'

    std_stack_list = time_profile_parser.parse_time_profile(time_file, prefix)
    stack_director.start_play(std_stack_list, prefix)


if __name__ == "__main__":
    start()
