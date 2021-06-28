# coding=utf-8
import sys
sys.path.append("../")

import setting
from stack_common import stack_director
import umdh_file_parser
import base_utils


def umdh_stack_parser(file_name, output_dir):
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    print 'all stack len ', len(std_stack_list)
    _, prefix = base_utils.get_work_dir_and_prefix(output_dir)
    stack_director.start_play(std_stack_list, prefix)


if __name__ == "__main__":
    file_name = setting.WINDOWS_MEMORY_FILE
    output_dir = setting.WINDOW_MEMORY_OUTPUT_DIR
    umdh_stack_parser(file_name, output_dir)
