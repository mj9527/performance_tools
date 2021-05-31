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
        return name
    return ""


# def get_all_module_list(frames, module_list):
#     for frame in frames:
#         name = get_moudle_name(frame)
#         if name not in module_list:
#             module_list.append(name)

def find_str(str):
    for item in setting.business_list:
        if item.startswith(str):
            print ('find....')


def parse_stack(thread_stack, module_list):
    #print ('begin stack--------')
    words = thread_stack.first_line.split()
    alloc_size = int(words[1])
    print ("alloc size ", alloc_size)
    #get_all_module_list(thread_stack.frames, module_list)
    current_list = []
    found = False
    for frame in thread_stack.frames:
        name = get_moudle_name(frame)
        if name not in module_list:
            module_list.append(name)
        name = name.strip()
        #print (name)
        #find_str(name)
        if name in setting.business_list:
            #print ('found')
            found = True
            break
        current_list.append(name)
    if not found:
        print ('not find business module', current_list)

    #print ('end stack--------')


def scan_stack_list(stack_list):
    module_list = []
    for thread_stack in stack_list:
        parse_stack(thread_stack, module_list)
    for module in module_list:
        print (module)
   # print (module_list)


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
