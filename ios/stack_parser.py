# coding=utf-8
import json
import xml.etree.ElementTree as ET
import sys
sys.path.append("..")
import symbol_parser
import setting
import stack_printer


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


class NodeInfo:
    def __init__(self, thread_id, node):
        self.node = node
        self.thread_id = thread_id
        self.child_list = []


class FrameInfo:
    def __init__(self, index, address, weight):
        self.index = index
        self.address = address
        self.self_weight = weight
        self.all_weight = weight
        self.func_name = ""
        self.module = ""


def get_thread_tree_list(thread_id_to_backtrace_list, id_to_item):
    thread_tree_list = []
    for (thread_id, backtrace_list) in thread_id_to_backtrace_list.items():
        thread_name = get_thread_name(thread_id, id_to_item)
        # if thread_name.find('pthread_start 0x18fecc') == -1:
        #     continue
        # print ('the same ....', thread_name)
        root = NodeInfo(thread_id, FrameInfo(0, thread_name, 0))
        get_thread_tree(root, backtrace_list)
        thread_tree_list.append(root)
    return thread_tree_list


def get_thread_tree(root, backtrace_list):
    for (backtrace_id, backtrace) in backtrace_list.items():
        child_list = root.child_list
        address_list = backtrace.address_list
        weight = backtrace.weight
        for index, address in enumerate(address_list):
            child = get_child_node(child_list, index, address, weight)
            child_list = child.child_list
    for child in root.child_list:
        root.node.self_weight += child.node.self_weight
        root.node.all_weight += child.node.all_weight


def get_child_node(child_list, index, address, weight):
    for child in child_list:
        node = child.node
        if node.index == index and node.address == address:
            node.self_weight += weight
            node.all_weight += weight
            return child
    child = NodeInfo(0, FrameInfo(index, address, weight))
    child_list.append(child)
    return child


def get_thread_name(thread_id, id_to_item):
    thread_item = id_to_item.get(thread_id)
    thread_name = thread_item.attrib.get('fmt')
    word_list = thread_name.split()
    if len(word_list) >= 2:
        thread_name = word_list[0] + " " + word_list[1]
    return thread_name


def analyse_group(xml_file, json_file, txt_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # step 1
    id_to_item = get_all_id_to_item(root)

    # step 2 thread_id->[backtrace list]
    thread_id_to_backtrace_list, address_list = get_thread_to_backtrace_list(root, id_to_item)
    stack_printer.print_thread_backtrace(thread_id_to_backtrace_list, id_to_item)

    # get symbol address
    address_symbol = {}
    if setting.symbol_parse == 1:
        module_file = '/Users/mjzheng/Downloads/ios_data/2021-04-08_17_23_22/20210408172529188_ori.crash'
        address_symbol = symbol_parser.symbol_with_file(module_file, address_list)

    # step 3
    thread_tree_list = get_thread_tree_list(thread_id_to_backtrace_list, id_to_item)

    if setting.symbol_parse == 1:
        symbol_thread_tree(thread_tree_list, address_symbol)

    # step
    txt_tree = stack_printer.get_txt_data(thread_tree_list)
    stack_printer.write_txt_file(txt_file, txt_tree)

    # step 4
    json_data = stack_printer.get_json_data(thread_tree_list)
    stack_printer.write_json_file(json_file, json_data)
    return


def symbol_thread_tree(thread_tree_list, address_symbol):
    for thread_tree in thread_tree_list:
        symbol_frame_tree(thread_tree, address_symbol)


def symbol_frame_tree(tree_node, address_symbol):
    node = tree_node.node
    if node.address in address_symbol:
        symbol = address_symbol[node.address]
        node.module = symbol.module_name
        node.func_name = symbol.func_name
    if not tree_node.child_list:
        return
    if len(tree_node.child_list) == 0:
        return

    for child in tree_node.child_list:
        symbol_frame_tree(child, address_symbol)
    return


if __name__ == "__main__":
    print('hello')
