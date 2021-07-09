# -*- coding: utf-8 -*-
PREFIX_TOTAL_COUNT = "Event count: "
DATA_HEAD = ['Children', 'Self', 'Command', 'Pid', 'Tid', 'Shared', 'Object', 'Symbol']
functions = {}
CallStacks = []
JSON_INDENT = 2


class ThreadInfo:
    def __init__(self, tid, tname):
        self.tid = tid
        self.tname = tname
        self.functions = None


class FrameInfo:
    def __init__(self, name, indent, weight, self_weight):
        self.indent = indent
        self.name = name
        self.weight = weight
        self.self_weight = self_weight
        self.module = "unknown"
        self.children = []


class FuncInfo:
    def __init__(self, weight, self_weight, module):
        self.weight = weight
        self.self_weight = self_weight
        self.module = module


class LineInfo:
    def __init__(self, elements):
        self.children = to_float(elements[0].strip("%"))
        self.self = to_float(elements[1].strip("%"))
        self.tname = elements[2]
        self.pid = elements[3]
        self.tid = elements[4]
        self.module = elements[5]
        self.funcname = elements[6]


def get_line_info(line):
    elements = list(filter(None, replace_return(line).split("  ")))
    if len(elements) < 7:
        return None

    for index in range(len(elements)):
        elements[index] = elements[index].strip()

    if elements[0].find('%') != -1 and elements[0].find('%') != -1:
        if len(elements) == 8:
            elements[6] = elements[6] + " " + elements[7]
            elements.pop()

        return LineInfo(elements)

    return None


def cluster_functions(input_file):
    data_begin = False
    while True:
        line = input_file.readline()
        if not line:
            break

        data_info = list(filter(None, replace_return(line).split(" ")))
        if not data_begin:
            if data_info == DATA_HEAD:
                data_begin = True

            continue

        data_info = get_line_info(line)
        if not data_info:
            break

        module = data_info.module[data_info.module.rfind('/') + 1:]
        if data_info.tid not in functions.keys():
            functions[data_info.tid] = ThreadInfo(data_info.tid, data_info.tname)
            functions[data_info.tid].functions = {}

        functions[data_info.tid].functions[data_info.funcname] = module


def replace_return(text):
    text = text.replace('\r', '')
    text = text.replace('\n', '')
    return text


def to_float(str_float):
    try:
        value = float(str_float)
        return value
    except ValueError:
        return -1.0


def get_thread_name(pid, tid, tname):
    if pid == tid:
        return "MainThread"

    if "do_audio_preprocess_filter" in functions[tid].functions.keys():
        return "AudioPreprocessThread"

    if "xc_codec_video_decode" in functions[tid].functions.keys():
        return "VideoDecodeThread"

    if "on_push_audio_play_data(xc_cell_s*, unsigned int*)" in functions[tid].functions.keys():
        return "AudioRecvAndDecodeThread"

    if "uv__udp_io" in functions[tid].functions.keys():
        return "UDPThread"

    func = "AudioLsqa::XNNAudioLsqa::DoLsqa(void*, unsigned char*, int, int, unsigned int, unsigned int, unsigned int)"
    if func in functions[tid].functions.keys():
        return "AudioLsqa"

    if "android::AudioTrack::processAudioBuffer()" in functions[tid].functions.keys():
        return "AudioPlay"

    return tname


def parse_callstack(root_func, src_file):
    for stack in CallStacks:
        if stack.tid == root_func.tid:
            return None

    f = open("file_temp.txt", "w+")
    tname = get_thread_name(root_func.pid, root_func.tid, root_func.tname)
    thread_info = ThreadInfo(root_func.tid, tname)

    f.writelines(src_file.readline())
    root = FrameInfo(root_func.funcname, 0, root_func.children, root_func.self)
    root.module = functions[thread_info.tid].functions[root_func.funcname]
    root_func = None
    stack = [root]
    while True:
        line = src_file.readline()
        if not line:
            break
        f.writelines(line)
        line = replace_return(line)
        root_func = get_line_info(line)
        if root_func is not None:
            break

        line = line.replace("|", " ")
        indent = len(line) - len(line.strip())
        top = stack[len(stack) - 1]
        if indent == len(line):
            continue
        else:
            index = line.rfind("%--")
            is_callee = False
            if index == -1:
                is_callee = True
                funcname = line.strip()
                cur_frame = FrameInfo(funcname, top.indent, 100, 0)
            else:
                temp = list(filter(None, line.split("--")))
                weight = to_float(temp[1].strip("%"))
                funcname = temp[2].strip()
                if funcname == "[hit in function]":
                    top.self_weight = weight * top.weight / 100
                    continue

                cur_frame = FrameInfo(funcname, indent, weight, 0)

            if funcname in functions[thread_info.tid].functions.keys():
                module = functions[thread_info.tid].functions[funcname]
            else:
                module = "Unknown"

            cur_frame.module = module

            if not is_callee:
                while cur_frame.indent <= top.indent:
                    stack.pop()
                    top = stack[len(stack) - 1]

            cur_frame.weight = top.weight * cur_frame.weight / 100
            top.children.append(cur_frame)
            stack.append(cur_frame)

    f.close()
    thread_info.functions = root
    CallStacks.append(thread_info)

    return root_func


def print_stack(file, stack, indent, last):

    file.writelines(indent * JSON_INDENT * ' ' + '{\n')

    file.writelines((indent + 1) * JSON_INDENT * ' ' + '"funcname" : "{}",\n'.format(stack.name))
    file.writelines((indent + 1) * JSON_INDENT * ' ' + '"module" : "{}",\n'.format(stack.module))
    file.writelines((indent + 1) * JSON_INDENT * ' ' + '"weight" : {:.2f},\n'.format(stack.weight))
    file.writelines((indent + 1) * JSON_INDENT * ' ' + '"selfWeight" : {:.2f},\n'.format(stack.self_weight))
    file.writelines((indent + 1) * JSON_INDENT * ' ' + '"children" : [\n')

    last_frame = None
    if len(stack.children) != 0:
        last_frame = stack.children[len(stack.children) - 1]

    for frame in stack.children:
        print_stack(file, frame, indent + 2, frame == last_frame)

    file.writelines((indent + 1) * JSON_INDENT * ' ' + ']\n')

    if last:
        file.writelines(indent * JSON_INDENT * ' ' + '}\n')
    else:
        file.writelines(indent * JSON_INDENT * ' ' + '},\n')


def stack_2_json(filename):
    with open(filename, "w") as dst:
        dst.writelines('{\n')
        dst.writelines(JSON_INDENT * ' ' + '"threads": [\n')

        for thread in CallStacks:
            dst.writelines(2 * JSON_INDENT * ' ' + '{\n')
            dst.writelines(3 * JSON_INDENT * ' ' + '"threadID": {},\n'.format(thread.tid))
            dst.writelines(3 * JSON_INDENT * ' ' + '"func": [\n')
            print_stack(dst, thread.functions, 4, True)

            dst.writelines(3 * JSON_INDENT * ' ' + ']\n')
            if thread == CallStacks[len(CallStacks) - 1]:
                dst.writelines(2 * JSON_INDENT * ' ' + '}\n')
            else:
                dst.writelines(2 * JSON_INDENT * ' ' + '},\n')

        dst.writelines(JSON_INDENT * ' ' + ']\n')
        dst.writelines('}\n')


def graph_2_json(src_file_name, dst_file_name):
    with open(src_file_name, "r") as src:
        cluster_functions(src)

        root_func = None
        while True:
            line = src.readline()
            if not line:
                break

            line = replace_return(line)
            if line == "       |":
                root_func = parse_callstack(root_func, src)
            else:
                root_func = get_line_info(line)

    stack_2_json(dst_file_name)


if __name__ == '__main__':
    graph_2_json("temp.txt", "android.json")
