# coding=utf-8

import sys
sys.path.append("..")
import setting
import stack_pie
import base_utils


def get_stack_module(std_stack, define_module_list):
    for frame in std_stack.frame_list:
        if frame.module in define_module_list:
            return frame
    return None


def get_first_valid_module(std_stack):
    for frame in std_stack.frame_list:
        if frame.module != '<no module>':
            return frame
    return None


def get_valid_stack_module(std_stack):
    frame = get_stack_module(std_stack, setting.BUSINESS_MODULE_LIST)
    if frame is None:
        frame = get_stack_module(std_stack, setting.BASE_MODULE_LIST)
    if frame is None:
        frame = get_first_valid_module(std_stack)
    return frame


def get_module_alloc_size(std_stack, module_to_size):
    frame = get_valid_stack_module(std_stack)
    if frame is None:
        print 'unexpect error : failed to get module frame'
        return

    stack_module = frame.module
    if stack_module == '<no module>' or stack_module == "":
        print 'unexpect error : failed to get module name'
        return

    if stack_module not in module_to_size:
        module_to_size[stack_module] = std_stack.weight
    else:
        module_to_size[stack_module] += std_stack.weight


def print_module_alloc_size(module_to_size, prefix):
    module_ls = sorted(module_to_size.items(), key=lambda kv: (kv[1], kv[0]))
    module_ls = module_ls[::-1]
    file_name = prefix + '_module_size_desc.txt'
    with open(file_name, "w") as f:
        for module in module_ls:
            f.write(str(module[0]) + '\t' + str(module[1]) + '\n')
            #print 'module alloc size: ', module


def statistics_module_size(std_stack_list, prefix):
    module_to_size = {}
    for std_stack in std_stack_list:
        get_module_alloc_size(std_stack, module_to_size)
    print_module_alloc_size(module_to_size, prefix)
    stack_pie.show_kv_pie(module_to_size, prefix)


def statistics_stack_list(std_stack_list, prefix):
    statistics_module_size(std_stack_list, prefix)
    statistics_start_func_size(std_stack_list, prefix)


def statistics_start_func_size(std_stack_list, prefix):
    module_to_func_dict = {}
    for std_stack in std_stack_list:
        get_start_func_size(std_stack, module_to_func_dict)
    tmp_dict = merge_func(module_to_func_dict)
    print_start_func_size(tmp_dict, prefix)


def get_start_func_size(std_stack, module_to_func_dict):
    origin_frame = get_valid_stack_module(std_stack)
    if origin_frame is None:
        print 'unexpect error : failed to get module frame'
        return

    stack_module = origin_frame.module
    if stack_module == '<no module>' or stack_module == "":
        print 'unexpect error : failed to get module name'
        return

    adjust_frame = get_valid_start_func(std_stack, stack_module)
    if adjust_frame is None:
        adjust_frame = origin_frame

    func_name = adjust_frame.func_name
    if stack_module not in module_to_func_dict:
        func_to_weight = {func_name: std_stack.weight}
        module_to_func_dict[stack_module] = func_to_weight
    else:
        func_to_weight = module_to_func_dict[stack_module]
        if func_name not in func_to_weight:
            func_to_weight[func_name] = std_stack.weight
        else:
            func_to_weight[func_name] += std_stack.weight


def print_start_func_size(module_to_func_list, prefix):
    module_dir = prefix + '/module/'
    base_utils.mkdir(module_dir)
    for module, func_dict in module_to_func_list.items():
        module_prefix = module_dir + module
        func_dict_ret = merge_top_func(module, func_dict)
        stack_pie.show_kv_pie(func_dict_ret, module_prefix)


def merge_top_func(module, func_dict):
    func_ls = sorted(func_dict.items(), key=lambda kv: (kv[1], kv[0]))
    func_ls = func_ls[::-1]
    func_dict_ret = {}
    for index, func in enumerate(func_ls):
        print module, func
        if index <= setting.TOP_FUNC_SIZE:
            func_dict_ret[func[0]] = func[1]
        else:
            if 'other' not in func_dict_ret:
                func_dict_ret['other'] = func[1]
            else:
                func_dict_ret['other'] += func[1]
    return func_dict_ret


def merge_func(module_to_func_list):
    tmp_dict = {}
    for module, func_dict in module_to_func_list.items():
        for func, weight in func_dict.items():
            parts = func.split('+')
            func_name = parts[0]
            #print func_name
            if module not in tmp_dict:
                func_to_weight = {func_name: weight}
                tmp_dict[module] = func_to_weight
            else:
                func_to_weight = tmp_dict[module]
                if func_name not in func_to_weight:
                    func_to_weight[func_name] = weight
                else:
                    func_to_weight[func_name] += weight
    return tmp_dict


def get_valid_start_func(std_stack, module):
    if module not in setting.MODULE_TO_START_FUNC_LS:
        return None
    block_list = setting.MODULE_TO_START_FUNC_LS[module]
    if block_list is None or len(block_list) == 0:
        return None
    for frame in std_stack.frame_list:
        if frame.module == module and not match_func(frame.func_name, block_list):
            return frame
    return None


def match_func(func_name, block_list):
    for block_func in block_list:
        if func_name.find(block_func) != -1:
            return True
    return False


# def get_module_fun_list(std_stack, module_to_func_list):
#     for frame in std_stack.frame_list:
#         if frame.module not in module_to_func_list:
#             module_to_func_list[frame.module] = [frame.func_name]
#         else:
#             func_list = module_to_func_list[frame.module]
#             if frame.func_name not in func_list:
#                 func_list.append(frame.func_name)
#
#
# def printf_module_func_list(module_to_func_list, prefix):
#     file_name = prefix + '_func_list.txt'
#     with open(file_name, "w") as f:
#         for module, func_list in module_to_func_list.items():
#             func_list.sort()
#             for func in func_list:
#                 line = module + ' ' + func + '\n'
#                 f.write(line)
#         f.close()
if __name__ == "__main__":
    print 'umdh stat'
