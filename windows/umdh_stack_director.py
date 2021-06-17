# coding=utf-8
import sys
sys.path.append("../")

import setting
import stack_director
import umdh_file_parser
import datetime


def umdh_stack_parser(file_name, output_dir):
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time
    stack_director.start_play(std_stack_list, prefix)


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    umdh_stack_parser(file_name, output_dir)
