# coding=utf-8
#import re
from enum import Enum
import sys
sys.path.append("..")
import base_utils
import setting


class StackStatus(Enum):
    INVALID = 0
    FIRST_LINE = 1
    SECOND_LINE = 2
    FIRST_CRLF = 3
    FRAMES = 4
    FINISH_CRLF = 5


class ThreadStack:
    def __init__(self):
        self.first_line = ""
        self.second_line = ""
        self.frames = []


def get_moudle_name(frame):
    index = frame.find('!')
    if index != -1:
        name = frame[0:index]
        name = name.strip()
        return name
    return ""


# def get_all_module_list(frames, module_list):
#     for frame in frames:
#         name = get_moudle_name(frame)
#         if name not in module_list:
#             module_list.append(name)

#
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


def parse_stack(thread_stack, global_module_list, module_to_size):
    #print ('begin stack--------')
    words = thread_stack.first_line.split()
    alloc_size = int(words[1])
    #print ("alloc size ", alloc_size)

    stack_module_list = []
    for frame in thread_stack.frames[::-1]: # reversed scan
        name = get_moudle_name(frame)
        stack_module_list.append(name)
        if name not in global_module_list:
            global_module_list.append(name)
        #print (name)
    # get belong module by priority
    stack_module = get_stack_module(stack_module_list, setting.business_module_list)
    if stack_module == "" :
        stack_module = get_stack_module(stack_module_list, setting.base_module_list)
    if stack_module == "":
        stack_module = get_first_valid_module(stack_module_list)

    if stack_module == '<no module>':
        print 'error'

    if stack_module not in module_to_size:
        module_to_size[stack_module] = alloc_size
    else:
        old_size = module_to_size[stack_module]
        new_size = old_size + alloc_size
        module_to_size[stack_module] = new_size
        # if stack_module == 'xcast':
        #     print ('oldsize ', old_size, 'newSize ', new_size)

    if stack_module == "":
        print ('not find business module', stack_module_list)


def print_module_list(module_list):
    for module in module_list:
        print (module)


def print_module_to_size(module_to_size):
    for key, value in module_to_size.items():
        print key, ':', value


def print_module_size(module_ls):
    for module in module_ls:
        print module


def scan_stack_list(stack_list):
    global_module_list = []
    module_to_size = {}
    for thread_stack in stack_list:
        parse_stack(thread_stack, global_module_list, module_to_size)

    #print_module_to_size(module_to_size)
    module_ls = sorted(module_to_size.items(), key=lambda kv: (kv[1], kv[0]))
    print_module_size(module_ls)



def parse_memory(file_name):
    f = open(file_name)
    line = f.readline()
    stack_list = []
    status = StackStatus.INVALID
    while line:
        if status == StackStatus.INVALID:
            if line.startswith('+'):
                status = StackStatus.FIRST_LINE
                continue
        elif status == StackStatus.FIRST_LINE:
            thread_stack = ThreadStack()
            thread_stack.first_line = line
            status = StackStatus.SECOND_LINE
        elif status == StackStatus.SECOND_LINE:
            if line.startswith('+'):
                thread_stack.second_line = line
                status = StackStatus.FIRST_CRLF
        elif status == StackStatus.FIRST_CRLF:
            if line == '\r\n':
                status = StackStatus.FRAMES
        elif status == StackStatus.FRAMES:
            if line == '\r\n':
                status = StackStatus.FINISH_CRLF
                continue
            else:
                thread_stack.frames.append(line)
        elif status == StackStatus.FINISH_CRLF:
            stack_list.append(thread_stack)
            status = StackStatus.INVALID

        line = f.readline()
    f.close()
    scan_stack_list(stack_list)


if __name__ == "__main__":
    file_name = '/Users/mjzheng/Downloads/memory/diff.txt'
    parse_memory(file_name)
