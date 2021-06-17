# coding=utf-8
import json
import xml.etree.ElementTree as ET
import sys
sys.path.append("..")
import symbol_parser
import setting
import base_def
import stack_director


def get_all_id_to_item(root):
    id_to_item = {}
    for item in root[0]:
        if item.tag == 'row':
            dict1 = get_id_to_item(item)
            id_to_item.update(dict1)
    return id_to_item


def get_id_to_item(item):
    dict2 = {}
    for i in item:
        if i.attrib.get('id'):
            dict2[i.attrib.get('id')] = i
        dict3 = get_id_to_item(i)
        dict2.update(dict3)
    return dict2


class Backtrace:
    def __init__(self, backtrace_id, weight, detail):
        self.backtrace_id = backtrace_id
        self.weight = weight
        self.address_list = detail
        self.symbol_list = []
        self.frame_list =[]


# # 相同backtrace_id weight聚合, 并解析backtrace_id
def get_thread_to_backtrace_list(root, id_to_item):
    thread_id_to_backtrace_list = {}
    address_list = []
    for c in root[0]:
        if c.tag != 'row':
            continue
        thread_id, backtrace_id, weight = get_row_info(c, id_to_item)
        if backtrace_id == 0:
            print ('waring: no backtrace item', thread_id)
            continue

        backtrace_list = {}
        if thread_id in thread_id_to_backtrace_list.keys():
            backtrace_list = thread_id_to_backtrace_list[thread_id]
        if backtrace_id in backtrace_list.keys():
            bt = backtrace_list[backtrace_id]
            bt.weight += weight
            backtrace_list[backtrace_id] = bt
        else:
            backtrace_item = id_to_item.get(backtrace_id)
            detail = get_backtrace_detail(id_to_item, backtrace_item, address_list)
            bt = Backtrace(backtrace_id, weight, detail)
            backtrace_list[backtrace_id] = bt
        thread_id_to_backtrace_list[thread_id] = backtrace_list
    return thread_id_to_backtrace_list, address_list


def get_row_info(c, id_to_item):
    weight = 0
    thread_id = 0
    backtrace_id = 0
    for i in c:
        if i.tag == 'weight':
            weight_id = get_id(i)
            weight_item = id_to_item.get(weight_id)
            weight_value = weight_item.attrib.get('fmt')
            ls = weight_value.split()
            if len(ls) == 2:
                weight = float(ls[0])
            else:
                print ('error')
        elif i.tag == 'thread':
            thread_id = get_id(i)
        elif i.tag == 'backtrace':
            backtrace_id = get_id(i)
    return thread_id, backtrace_id, weight


def get_backtrace_detail(id_to_item, item, address_list):
    result = []
    for j in item:
        if j.tag == 'text-addresses':
            text_id = get_id(j)
            j = id_to_item.get(text_id)
            if type(j.text) == str:
                frames = j.text.split()
                for frame in frames:
                    tmp = int(frame)
                    if tmp == 0:
                        print ("error", frame, j.text)
                        continue
                    address = hex(int(frame))
                    result.append(address)
                    if address not in address_list:
                        address_list.append(address)
    result.reverse()
    return result


def get_id(item):
    return item.attrib.get('id') if item.attrib.get('id') else item.attrib.get('ref')


def get_thread_name(thread_id, id_to_item):
    thread_item = id_to_item.get(thread_id)
    thread_name = thread_item.attrib.get('fmt')
    word_list = thread_name.split()
    if len(word_list) >= 2:
        thread_name = word_list[0] + " " + word_list[1]
    return thread_name


def analyse_group(xml_file, prefix):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # step 1
    id_to_item = get_all_id_to_item(root)

    # step 2 thread_id->[backtrace list]
    thread_id_to_backtrace_list, address_list = get_thread_to_backtrace_list(root, id_to_item)
    #stack_txt.print_thread_backtrace(thread_id_to_backtrace_list, id_to_item)

    # get symbol address
    address_symbol = {}

    module_file = prefix + '.log'
    if setting.symbol_parse == 1:
        address_symbol = symbol_parser.symbol_with_file(module_file, address_list)
    stack_group_list = symbol_thread_backtrace(thread_id_to_backtrace_list, address_symbol)

    stack_director.start_play2(stack_group_list, prefix)
    return


def symbol_thread_backtrace(thread_group, address_symbol):
    stack_group_dict = {}
    for (thread_id, thread) in thread_group.items():
        std_stack_list = []
        for (backtrace_id, bt) in thread.items():
            frame_list = []
            for index, address in enumerate(bt.address_list):
                weight = bt.weight
                if address in address_symbol:
                    symbol = address_symbol[address]
                    func_name = symbol.func_name
                    module = symbol.module_name
                else:
                    func_name = address
                    module = 'unknow'
                info = base_def.FrameInfo(index, address, func_name, module, weight)
                frame_list.append(info)
            std_stack = base_def.StackInfo(frame_list, bt.weight)
            std_stack_list.append(std_stack)
        stack_group_dict[thread_id] = std_stack_list
    return stack_group_dict


if __name__ == "__main__":
    print('hello')
