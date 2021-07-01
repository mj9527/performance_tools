import sys
sys.path.append("..")
import base_def
import setting
import base_utils

import unify_input_file
import stack_director


def unify_director(file_name, output_dir):
    lines = unify_input_file.read_std_flame_file(file_name)
    std_stack_list = std_flame_to_std_stack(lines)
    _, prefix = base_utils.get_work_dir_and_prefix(output_dir)
    stack_director.start_play(std_stack_list, prefix)


def std_flame_to_std_stack(lines):
    std_stack_list = []
    for _, line in enumerate(lines):
        pos = line.rfind(' ')
        if pos == -1:
            print 'unexecpt error ', line
            continue
        weight = line[pos+1:]
        weight = float(trim_special(weight))
        str_frame = line[:pos]
        func_list = str_frame.split(';')
        frame_list = []
        for index, func_name in enumerate(func_list):
            if func_name == '':
                continue
            address = func_name
            module = ''
            info = base_def.FrameInfo(index, address, func_name, module, weight)
            frame_list.append(info)
        std_stack = base_def.StackInfo(frame_list, weight)
        std_stack_list.append(std_stack)
    return std_stack_list


def trim_special(line):
    line = line.strip()
    line = line.replace('\n', '')
    return line


if __name__ == "__main__":
    file_name = setting.STD_STACK_FILE
    output_dir = setting.STD_STACK_OUTPUT_DIR
    unify_director(file_name, output_dir)
