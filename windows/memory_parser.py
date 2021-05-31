# coding=utf-8
#import re
from enum import Enum


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


def parse_stack(thread_stack):
    print ('begin stack--------')
    print (thread_stack.first_line)
    print (thread_stack.second_line)
    words = thread_stack.first_line.split()
    alloc_size = int(words[1])
    print ("alloc size ", alloc_size)
    for frame in thread_stack.frames:
        print (frame)
    print ('end stack--------')


def scan_stack_list(stack_list):
    for thread_statck in stack_list:
        parse_stack(thread_statck)


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
    file_name = '/Users/mjzheng/Downloads/memory/6_5.txt'
    parse_memory(file_name)
