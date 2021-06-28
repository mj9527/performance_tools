# coding=utf-8
import json
import xml.etree.ElementTree as ET
import sys
sys.path.append("..")
import symbol_parser
import setting
import base_def


class Backtrace:
    def __init__(self, backtrace_id, weight, address_list):
        self.backtrace_id = backtrace_id
        self.weight = weight
        self.address_list = address_list


def parse_time_profile(xml_file, prefix):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    id_to_item = get_all_id_to_item(root)

    # step 1 : {thread_id->{backtrace_id->backtrace}}
    thread_id_to_backtrace_list = group_stack_list_by_thread(root, id_to_item)

    # step 2 : get symbol address
    address_symbol = {}
    if setting.SYMBOL_PARSE == 1:
        module_file = prefix + '.log'
        address_list = get_address_list(thread_id_to_backtrace_list)
        address_symbol = symbol_parser.symbol_with_file(module_file, address_list)

    # step 3 : {thread_id->stack_list]}
    stack_group_list = unify_thread_backtrace(thread_id_to_backtrace_list, address_symbol)
    return stack_group_list


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


def inside_file(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    id_to_item = get_all_id_to_item(root)
    tid_to_bid_to_wid = inside_stack(root)


def inside_stack(root):
    tid_to_bid_to_wid = {}
    for c in root[0]:
        if c.tag != 'row':
            continue
        thread_id, backtrace_id, weight_id = get_row_info(c)
        if backtrace_id == 0:
            print ('waring: no backtrace item', thread_id)
            continue

        if thread_id in tid_to_bid_to_wid.keys():
            bid_dict = tid_to_bid_to_wid[thread_id]
        else:
            bid_dict = {}
            tid_to_bid_to_wid[thread_id] = bid_dict

        if backtrace_id in bid_dict.keys():
            wid_list = bid_dict[backtrace_id]
        else:
            wid_list = []
            bid_dict[backtrace_id] = wid_list
        wid_list.append(weight_id)
    return tid_to_bid_to_wid


# # 相同backtrace_id weight聚合, 并解析backtrace_id
def group_stack_list_by_thread(root, id_to_item):
    thread_id_to_stack_list = {}
    for c in root[0]:
        if c.tag != 'row':
            continue
        thread_id, backtrace_id, weight_id = get_row_info(c)
        if backtrace_id == 0:
            print ('waring: no backtrace item', thread_id)
            continue

        weight = get_weight_by_id(weight_id, id_to_item)
        thread_name = get_thread_name(thread_id, id_to_item)

        backtrace_list = {}
        if thread_id in thread_id_to_stack_list.keys():
            backtrace_list = thread_id_to_stack_list[thread_id]
        if backtrace_id in backtrace_list.keys():
            bt = backtrace_list[backtrace_id]
            bt.weight += weight
            backtrace_list[backtrace_id] = bt
        else:
            address_list = get_backtrace_by_id(backtrace_id, id_to_item)
            bass_address = thread_name + '_' + str(thread_id)
            address_list.insert(0, bass_address)
            #print 'insert thread name ', thread_name
            bt = Backtrace(backtrace_id, weight, address_list)
            backtrace_list[backtrace_id] = bt
        thread_id_to_stack_list[thread_id] = backtrace_list
    return thread_id_to_stack_list


def get_row_info(c):
    weight_id = 0
    thread_id = 0
    backtrace_id = 0
    for i in c:
        if i.tag == 'weight':
            weight_id = get_id(i)
        elif i.tag == 'thread':
            thread_id = get_id(i)
        elif i.tag == 'backtrace':
            backtrace_id = get_id(i)
    return thread_id, backtrace_id, weight_id


def get_weight_by_id(weight_id, id_to_item):
    weight_item = id_to_item.get(weight_id)
    weight_value = weight_item.attrib.get('fmt')
    ls = weight_value.split()
    if len(ls) == 2:
        weight = float(ls[0])
    else:
        print 'fail to get weight ', weight_id
        weight = 0.0
    return weight


def get_backtrace_by_id(backtrace_id, id_to_item):
    item = id_to_item.get(backtrace_id)
    address_list = []
    for j in item:
        if j.tag == 'text-addresses':
            text_id = get_id(j)
            j = id_to_item.get(text_id)
            if type(j.text) == str:
                frames = j.text.split()
                for frame in frames:
                    tmp = int(frame)
                    if tmp == 0:
                        print ("waring: filter invalid frame ", frame, j.text)
                        continue
                    address = hex(int(frame))
                    address_list.append(address)
    address_list.reverse()
    return address_list


def get_id(item):
    return item.attrib.get('id') if item.attrib.get('id') else item.attrib.get('ref')


def get_thread_name(thread_id, id_to_item):
    thread_item = id_to_item.get(thread_id)
    thread_name = thread_item.attrib.get('fmt')
    word_list = thread_name.split()
    if len(word_list) >= 2:
        thread_name = word_list[0] + "_" + word_list[1]
    return thread_name


def unify_thread_backtrace(thread_id_to_backtrace_list, address_symbol):
    std_stack_list = []
    for (thread_id, stacK_dict) in thread_id_to_backtrace_list.items():
        for (backtrace_id, bt) in stacK_dict.items():
            std_stack = get_std_stack(bt, address_symbol)
            std_stack_list.append(std_stack)
    return std_stack_list


def get_std_stack(bt, address_symbol):
    frame_list = []
    for index, address in enumerate(bt.address_list):
        weight = bt.weight
        if address in address_symbol:
            symbol = address_symbol[address]
            func_name = symbol.func_name
            if func_name.find('"') != -1:
                func_name = func_name.replace('"', '')
                print 'find ...................... ', func_name
            if func_name.find('?') != -1:
                func_name = func_name.replace('?', '')
                print 'find ...................... ', func_name
            if func_name.find(u'\u0001') != -1:
                print 'find XXXX', func_name
                func_name = func_name.replace(u'\u0001', '')
        else:
            func_name = address
            module = 'unknow'
        info = base_def.FrameInfo(index, address, func_name, module, weight)
        frame_list.append(info)
    std_stack = base_def.StackInfo(frame_list, bt.weight)
    return std_stack


def get_address_list(thread_id_to_stack_list):
    address_list = []
    for (thread_id, stack_list) in thread_id_to_stack_list.items():
        for (backtrace_id, bt) in stack_list.items():
            for index, address in enumerate(bt.address_list):
                if address not in address_list:
                    address_list.append(address)
    return address_list


if __name__ == "__main__":
    print('hello')
