# coding=utf-8
import datetime
import os


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False


def get_work_dir_and_prefix(root_dir, system_type, profiler_type):
    if profiler_type == 'std_stack':
        origin_dir = root_dir + '/' + profiler_type + '/'
    else:
        origin_dir = root_dir + '/' + system_type + '/' + profiler_type + '/'
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    output_dir = origin_dir + current_time + '/'
    mkdir(output_dir)
    prefix = output_dir + current_time
    return output_dir, prefix


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
