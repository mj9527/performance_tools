# coding=utf-8
import record_apple
import content_parser
import time_profile_parser
import sys
sys.path.append("..")
import base_utils
import stack_director
import unify_input_file


def start():
    # output_dir, prefix = base_utils.get_work_dir_and_prefix_with_config()
    # trace_file, ret = record_apple.record_apple_config(prefix)
    # if ret != 0:
    #     return
    #
    # print ('start parse content ', trace_file)
    # time_file = content_parser.export_schema(trace_file, 'time-profile', prefix)
    #
    # content_file = content_parser.export_content(trace_file, prefix)
    # schema_list = content_parser.parse_content(content_file)
    # content_parser.export_schema_list(trace_file, prefix, schema_list)

    #return

    prefix = '/Users/mjzheng/Downloads/ios_data/2021-06-17_21_30_39/2021-06-17_21_30_39'
    time_file = prefix + '_time-profile.xml'

    std_stack_list = time_profile_parser.parse_time_profile(time_file, prefix)
    #stack_file = prefix + '.stack'
    #unify_input_file.write_stack_file(std_stack_list, stack_file)
    stack_director.start_play(std_stack_list, prefix)


if __name__ == "__main__":
    start()
