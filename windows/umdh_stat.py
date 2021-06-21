# coding=utf-8

import sys
sys.path.append("..")
import setting
import umdh_pie
import umdh_file_parser
import datetime
import unify_input_file


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
    frame = get_stack_module(std_stack, setting.business_module_list)
    if frame is None:
        frame = get_stack_module(std_stack, setting.base_module_list)
    if frame is None:
        frame = get_first_valid_module(std_stack)
    return frame


def get_module_alloc_size(std_stack, module_to_size):
    frame = get_valid_stack_module(std_stack)
    if frame is None:
        print 'error...........'
        return

    stack_module = frame.module
    if stack_module == '<no module>':
        print 'error'

    if stack_module == "":
        print ('not find business module')

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
        get_module_start_func(std_stack, module_to_func_list)
    print_moduel_start_func(module_to_func_list)
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


def match_func(func_name, block_list):
    for block_func in block_list:
        if func_name.find(block_func) != -1:
            return True
    return False


def get_valid_func_module(std_stack, module):
    if module not in setting.module_start_func:
        return None
    block_list = setting.module_start_func[module]
    if len(block_list) == 0:
        return None
    for frame in std_stack.frame_list:
        if frame.module == module and not match_func(frame.func_name, block_list):
            return frame
    return None


def get_module_start_func(std_stack, module_to_func_list):
    frame = get_valid_stack_module(std_stack)
    if frame is None:
        print 'error...........'
        return

    stack_module = frame.module
    if stack_module == '<no module>':
        print 'error'

    if stack_module == "":
        print ('not find business module')

    func_name = frame.func_name
    func_frame = get_valid_func_module(std_stack, stack_module)
    if func_frame is not None:
        func_name = func_frame.func_name

    if stack_module not in module_to_func_list:
        func_to_dict = {func_name: std_stack.weight}
        module_to_func_list[stack_module] = func_to_dict
    else:
        func_to_dict = module_to_func_list[stack_module]
        if func_name not in func_to_dict:
            func_to_dict[func_name] = std_stack.weight
        else:
            total_weight = func_to_dict[func_name]
            total_weight += std_stack.weight
            func_to_dict[func_name] = total_weight


def print_moduel_start_func(module_to_func_list):
    for module, func_dict in module_to_func_list.items():
        func_ls = sorted(func_dict.items(), key=lambda kv: (kv[1], kv[0]))
        func_ls = func_ls[::-1]
        for func in func_ls:
            if module == 'xcast':
                print module, func


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    std_stack_list = umdh_file_parser.get_std_stack_list(file_name)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time
    top_file = prefix + '_top.txt'
    unify_input_file.write_stack_file(std_stack_list, top_file)
    statistics_stack_list(std_stack_list, prefix)
    # block_list = setting.module_start_func['xcast']
    # func_name = 'fire_event+48'
    # if not match_func(func_name, block_list):
    #     print 'no found'
    # else:
    #     print 'found'
