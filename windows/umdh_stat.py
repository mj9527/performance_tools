# coding=utf-8

import sys
sys.path.append("..")
import setting
import umdh_pie
import umdh_file_parser
import datetime


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


def get_module_alloc_size(std_stack, module_to_size):
    stack_module_list = []
    for frame in std_stack.frame_list:
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
        module_to_size[stack_module] = std_stack.weight
    else:
        old_size = module_to_size[stack_module]
        new_size = old_size + std_stack.weight
        module_to_size[stack_module] = new_size


def print_module_list(module_list):
    for module in module_list:
        print (module)


def print_module_to_size(module_to_size):
    total_sz = 0
    for key, value in module_to_size.items():
        total_sz += value
    print 'alloc size', total_sz / 1024 / 1024


def statistics_stack_list(std_stack_list, prefix):
    module_to_size = {}
    module_to_func_list = {}
    for std_stack in std_stack_list:
        get_module_alloc_size(std_stack, module_to_size)
        get_module_fun_list(std_stack, module_to_func_list)
    printf_module_func_list(module_to_func_list, prefix)
    #print_module_to_size(module_to_size)

    module_ls = sorted(module_to_size.items(), key=lambda kv: (kv[1], kv[0]))
    print_module_list(module_ls)

    umdh_pie.show_memory_dic(module_to_size, prefix)


def get_module_fun_list(std_stack, module_to_func_list):
    for frame in std_stack.frame_list:
        if frame.module not in module_to_func_list:
            module_to_func_list[frame.module] = [frame.func_name]
        else:
            func_list = module_to_func_list[frame.module]
            if frame.func_name not in func_list:
                func_list.append(frame.func_name)


def printf_module_func_list(module_to_func_list, prefix):
    file_name = prefix + '_func_list.txt'
    with open(file_name, "w") as f:
        for module, func_list in module_to_func_list.items():
            func_list.sort()
            for func in func_list:
                line = module + ' ' + func + '\n'
                f.write(line)
        f.close()


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time
    statistics_stack_list(std_stack_list, prefix)
