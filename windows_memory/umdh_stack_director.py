# coding=utf-8
import sys
sys.path.append("../")

import setting
from stack_common import stack_director
import umdh_file_parser
import datetime
import umdh_stat


def binary_search(std_stack_list, start_index, end_index):
    print 'binary ', len(std_stack_list), start_index, end_index,  (start_index+end_index)/2, '.....'
    return std_stack_list[start_index:end_index]


def search(std_stack_list):
    start_index = 1
    end_index = 2  # 2 4 9 19 38 77 154 309 618 1237 2475 9901
    std_stack_list = binary_search(std_stack_list, start_index, end_index)
    std_stack = std_stack_list[0]
    print 'wrong stack len ', len(std_stack.frame_list)
    end_frame_index = 5
    search_frame(std_stack, end_frame_index)
    return std_stack_list


def search_frame(std_stack, end_index):
    for index, frame in enumerate(std_stack.frame_list):
        if index >= end_index:
            frame.func_name = '345'


def umdh_stack_parser(file_name, output_dir):
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    print 'all stack len ', len(std_stack_list)

    #std_stack_list = search(std_stack_list)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time
    std_stack_list = stack_director.start_play(std_stack_list, prefix)
    umdh_stat.statistics_stack_list(std_stack_list, prefix)


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    umdh_stack_parser(file_name, output_dir)
