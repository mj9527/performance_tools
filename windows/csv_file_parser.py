# coding=utf-8
import csv
import base_def


def get_proc_data(file_name, proc_name):
    proc_lines = []
    try:
        lines = csv.reader(open(file_name, 'r'))
    except IOError:
        print("read csv error")
        return proc_lines

    for line in lines:
        if proc_name in line[0]:
            proc_lines.append(line)
    return proc_lines


def translate_std_stack(lines):
    std_stack_list = []
    for line in lines:
        weight = line[4]
        stack_trace = line[2]
        stack_frame_list = stack_trace.split('/')
        frame_list = []
        for index, frame in enumerate(stack_frame_list):
            parts = frame.split('!')
            module = parts[0].strip()
            func_name = parts[1].strip()
            address = func_name
            info = base_def.FrameInfo(index, address, func_name, module, weight)
            frame_list.append(info)
        std_stack = base_def.StackInfo(frame_list, weight)
        std_stack_list.append(std_stack)
    return std_stack_list


def parse_csv_file(file_name, proc_name):
    lines = get_proc_data(file_name, proc_name)
    return translate_std_stack(lines)



