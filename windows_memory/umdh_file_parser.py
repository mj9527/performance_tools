# coding=utf-8
from enum import Enum
import sys
sys.path.append("..")
import setting
import base_def


class StackStatus(Enum):
    INVALID = 0
    FIRST_LINE = 1
    SECOND_LINE = 2
    FIRST_CRLF = 3
    FRAMES = 4
    FINISH_CRLF = 5
    MODULE_BEGIG = 6
    MODULE_END = 7


class ThreadStack:
    def __init__(self):
        self.first_line = ""
        self.second_line = ""
        self.frames = []


class ModuleInfo:
    def __init__(self):
        self.start_address = 0x0
        self.end_address = 0x0
        self.sz = 0
        self.name = ""


# 模块列表解析
def parse_module(file_name):
    print 'read file', file_name
    f = open(file_name)
    line = f.readline()
    status = StackStatus.INVALID
    total_sz = 0
    while line:
        if status == StackStatus.INVALID:
            if line.startswith('//'):
                status = StackStatus.MODULE_BEGIG
        elif status == StackStatus.MODULE_BEGIG:
            if line.startswith('//'):
                status = StackStatus.MODULE_END
                break
            if line.find('DBGHELP:') != -1:
                words = line.split()
                info = ModuleInfo()
                info.name = words[2]
                p = words[0].split('-')
                info.start_address = p[0]
                start = int(info.start_address, 16)
                info.end_address = p[1]
                end = int(info.end_address, 16)
                info.sz = end - start
                total_sz += info.sz
                #print info.start_address, info.end_address, info.sz, info.name
        elif status == StackStatus.MODULE_END:
            break
        line = f.readline()
    print 'total size', total_sz / 1024 / 1024
    f.close()


def get_std_stack_list(file_name):
    stack_list = get_stack_list_from_file(file_name)
    std_stack_list = preproccess_stack(stack_list)
    return std_stack_list


def trim_line(line):
    line = line.strip()
    line = line.replace('\r\n', '')
    #print line
    return line


def get_stack_list_from_file(file_name):
    f = open(file_name)
    line = f.readline()
    stack_list = []
    status = StackStatus.INVALID
    thread_id = 0
    while line:
        if status == StackStatus.INVALID:
            if line.startswith('+'):
                status = StackStatus.FIRST_LINE
                continue
        elif status == StackStatus.FIRST_LINE:
            thread_stack = ThreadStack()
            thread_stack.first_line = trim_line(line)
            thread_id += 1
            thread_stack.thread_id = thread_id
            status = StackStatus.SECOND_LINE
        elif status == StackStatus.SECOND_LINE:
            if line.startswith('+'):
                thread_stack.second_line = trim_line(line)
                status = StackStatus.FIRST_CRLF
        elif status == StackStatus.FIRST_CRLF:
            if line == '\r\n':
                status = StackStatus.FRAMES
        elif status == StackStatus.FRAMES:
            if line == '\r\n':
                status = StackStatus.FINISH_CRLF
                continue
            else:
                line = trim_line(line)
                thread_stack.frames.append(line)
        elif status == StackStatus.FINISH_CRLF:
            stack_list.append(thread_stack)
            status = StackStatus.INVALID

        line = f.readline()
    f.close()
    return stack_list


def get_func_name(func_info):
    pos = func_info.find(' (')
    if pos != -1:
        func_name = func_info[0:pos]
    else:
        func_name = func_info
    func_name.strip()
    # if func_name.find('"') != -1:
    #     func_name = func_name.replace('"', '')
    #     print 'find 1 ...................... ', func_name
    # if func_name.find('?') != -1:
    #     print 'find 2 ...................... ', func_name
    #     func_name = func_name.replace('?', '')
    #     print 'find 2 end ...................... ', func_name
    # if func_name.find(u'\u0001') != -1:
    #     print 'find XXXX', func_name
    #     func_name = func_name.replace(u'\u0001', '')
    # if func_name.find('`') != -1:
    #     print 'find 3...................... ', func_name
    #     func_name = func_name.replace('`', '')
    # if func_name.find("'") != -1:
    #     func_name = func_name.replace("'", '')
    # if func_name.find('\\') != -1:
    #     func_name = func_name.replace('\\', '')
    return func_name


def preproccess_stack(stack_list):
    std_stack_list = []
    for thread_stack in stack_list:
        parts = thread_stack.first_line.split()
        weight = int(parts[1])
        frame_list = []
        for index, frame in enumerate(thread_stack.frames[::-1]):
            parts = frame.split('!')
            module = parts[0].strip()
            #func_info = parts[1].split(' ')
            #func_name = func_info[0]
            func_name = get_func_name(parts[1])
            address = func_name
            info = base_def.FrameInfo(index, address, func_name, module, weight)
            frame_list.append(info)
        std_stack = base_def.StackInfo(frame_list, weight)
        std_stack_list.append(std_stack)
    return std_stack_list


if __name__ == "__main__":
    file_name = setting.WINDOWS_MEMORY_FILE
    output_dir = setting.WINDOW_MEMORY_OUTPUT_DIR
    get_std_stack_list(file_name)
