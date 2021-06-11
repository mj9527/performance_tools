# coding=utf-8

import sys
sys.path.append("..")
import setting
import memory_ui
import memory_file_parser


def get_stack_module(stack_module_list, define_module_list):
    stack_module = ""
    for module in stack_module_list:
        if module in define_module_list:
            stack_module = module
            break
    return stack_module


def get_first_valid_module(stack_module_list):
    stack_module = ""
    for module in stack_module_list:
        if module != '<no module>':
            stack_module = module
            break
    return stack_module


def get_module_alloc_size(thread_stack, module_to_size):
    stack_module_list = []
    for frame in thread_stack.frame_list:
        stack_module_list.append(frame.module)

    stack_module = get_stack_module(stack_module_list, setting.business_module_list)
    if stack_module == "":
        stack_module = get_stack_module(stack_module_list, setting.base_module_list)
    if stack_module == "":
        stack_module = get_first_valid_module(stack_module_list)

    if stack_module == '<no module>':
        print 'error'

    if stack_module == "":
        print ('not find business module', stack_module_list)

    if stack_module not in module_to_size:
        module_to_size[stack_module] = thread_stack.alloc_size
    else:
        old_size = module_to_size[stack_module]
        new_size = old_size + thread_stack.alloc_size
        module_to_size[stack_module] = new_size


def print_module_list(module_list):
    for module in module_list:
        print (module)


def print_module_to_size(module_to_size):
    total_sz = 0
    for key, value in module_to_size.items():
        total_sz += value
    print 'alloc size', total_sz / 1024 / 1024


def scan_stack_list(stack_list, output_dir):
    module_to_size = {}
    for thread_stack in stack_list:
        get_module_alloc_size(thread_stack, module_to_size)
    print_module_to_size(module_to_size)

    module_ls = sorted(module_to_size.items(), key=lambda kv: (kv[1], kv[0]))
    print_module_list(module_ls)

    memory_ui.show_memory_dic(module_to_size, output_dir)


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    stack_list = memory_file_parser.base_parser(file_name)
    scan_stack_list(stack_list, output_dir)
