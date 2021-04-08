# coding=utf-8
import json
import xml.etree.ElementTree as ET
import sys
sys.path.append("..")
import symbol_parser


def get_all_id(root):
    result = {}
    for item in root[0]:
        if item.tag == 'row':
            dict1 = scan_level(item)
            result.update(dict1)
    return result


def scan_level(item):
    dict2 = {}
    for i in item:
        if i.attrib.get('id'):
            dict2[i.attrib.get('id')] = i
        dict3 = scan_level(i)
        dict2.update(dict3)
    return dict2


def print_all_id(dict):
    print ('len', len(dict))
    for key in dict:
        print (key, dict[key])


class Backtrace:
    def __init__(self):
        backtrace_id = 0
        weight = 0
        backtrace_detail = []


# # 相同backtrace_id weight聚合, 并解析backtrace_id
def get_thread_group(root, pattern):
    thread_group = {}
    address_list = []
    for c in root[0]:
        if c.tag != 'row':
            continue
        thread_id, backtrace_id, weight = get_row_info(c, pattern)
        if backtrace_id == 0:
            print ('waring: no backtrace item', thread_id)
            continue

        thread = {}
        if thread_id in thread_group.keys():
            thread = thread_group[thread_id]
        if backtrace_id in thread.keys():
            bt = thread[backtrace_id]
            bt.weight += weight
            thread[backtrace_id] = bt
        else:
            bt = Backtrace()
            bt.backtrace_id = backtrace_id
            bt.weight = weight
            backtrace_item = pattern.get(backtrace_id)
            detail = get_backtrace_detail(pattern, backtrace_item, address_list)
            bt.backtrace_detail = detail
            thread[backtrace_id] = bt
        thread_group[thread_id] = thread
    return thread_group, address_list


def get_row_info(c, pattern):
    weight = 0
    thread_id = 0
    backtrace_id = 0
    for i in c:
        if i.tag == 'weight':
            weight_id = get_id(i)
            weight_item = pattern.get(weight_id)
            weight_value = weight_item.attrib.get('fmt')
            ls = weight_value.split()
            if len(ls) == 2:
                weight = float(ls[0])
                #unit = ls[1]
                # print ('weight', weight)
            else:
                print ('error')
        elif i.tag == 'thread':
            thread_id = get_id(i)
        elif i.tag == 'backtrace':
            backtrace_id = get_id(i)
    return thread_id, backtrace_id, weight


def get_backtrace_detail(pattern, item, address_list):
    result = []
    for j in item:
        if j.tag == 'text-addresses':
            text_id = get_id(j)
            j = pattern.get(text_id)
            if type(j.text) == str:
                #print (j.text)
                frames = j.text.split()
                for frame in frames:
                    address = hex(int(frame))
                    result.append(address)
                    if address not in address_list:
                        address_list.append(address)
    result.reverse()
    return result


def get_id(item):
    return item.attrib.get('id') if item.attrib.get('id') else item.attrib.get('ref')


def print_thread_group(thread_group, pattern):
    for (thread_id, thread) in thread_group.items():
        thread_item = pattern.get(thread_id)
        thread_name = thread_item.attrib.get('fmt')
        print (thread_name)
        for (backtrace_id, bt) in thread.items():
            detail = bt.backtrace_detail
            print (detail, bt.weight)
        print ('\n')


class ThreadInfo:
    def __init__(self):
        top_node = FrameInfo()
        frame_tree = {}
        thread_id = 0


def get_thread_tree(thread_group, pattern):
    threads = []
    for (thread_id, thread) in thread_group.items():
        thread_name = get_thread_name(thread_id, pattern)
        info = ThreadInfo()
        info.thread_id = thread_id
        info.top_node = get_frame_info(0, thread_name, thread_name, 0)
        info.frame_tree = get_frame_tree(info.top_node, thread)
        threads.append(info)
    return threads


def get_thread_name(thread_id, pattern):
    thread_item = pattern.get(thread_id)
    thread_name = thread_item.attrib.get('fmt')
    word_list = thread_name.split()
    if len(word_list) >= 2:
        thread_name = word_list[0] + " " + word_list[1]
    return thread_name


def get_frame_tree(top_node, thread):
    frame_tree = {}
    top_children = []
    top_weight = 0;
    for (backtrace_id, bt) in thread.items():
        backtrace_detail = bt.backtrace_detail
        for index, address in enumerate(backtrace_detail):
            parent_key = get_key(index, address)
            if index == 0:
                add_frame(top_children, index, address, parent_key, bt.weight)
                top_weight += bt.weight
            children_list = get_children_list(frame_tree, parent_key)
            children_index = index + 1
            if children_index < len(backtrace_detail):
                children_address = backtrace_detail[children_index]
                children_key = get_key(children_index, children_address)
                add_frame(children_list, children_index, children_address, children_key, bt.weight)
            if children_list:
                frame_tree[parent_key] = children_list
    frame_tree[top_node.key] = top_children
    top_node.all_weight = top_weight
    top_node.self_weight = top_weight
    return frame_tree


class FrameInfo:
    def __init__(self):
        key = ""
        index = 0
        address = 0
        self_weight = 0
        all_weight = 0
        func_name = ""
        module = ""


def get_frame_info(index, address, key, weight):
    frame = FrameInfo()
    frame.index = index
    frame.key = key
    frame.address = address
    frame.self_weight = weight
    frame.all_weight = weight
    frame.func_name = ""
    frame.module = ""
    return frame


def get_children_list(frame_tree, key):
    children = []
    if key in frame_tree:
        children = frame_tree[key]
    return children


def add_frame(ls, index, address, key, weight):
    if is_repeat_frame(ls, key, weight):
        return
    frame = get_frame_info(index, address, key, weight)
    ls.append(frame)


def is_repeat_frame(ls, key, weight):
    for frame in ls:
        if frame.key == key:
            frame.all_weight += weight
            return True
    return False


def print_thread_tree(thread_group):
    threads = []
    for th_info in thread_group:
        frame_list = []
        print_frame_tree(th_info.frame_tree, th_info.top_node, frame_list)
        threads.append(frame_list)
    return threads


def write_txt_to_file(save_path, list_data):
    with open(save_path, "w") as f:
        for frame_list in list_data:
            for frame in frame_list:
                f.write(str(frame))
                print (frame)
                f.write('\n')
        f.close()


def print_frame_tree(frame_tree, node, frame_list):
    frame = print_frame(node)
    frame_list.append(frame)
    if len(frame_tree) == 0:
        return
    if node.key not in frame_tree:
        return
    children = frame_tree[node.key]
    if not children:
        return
    for frame in children:
        print_frame_tree(frame_tree, frame, frame_list)
    return


def print_frame(node):
    frame_info = ""
    for i in range(node.index):
        frame_info += ' '
    frame_info += node.key
    frame_info += ' ' + str(node.all_weight)
    return frame_info


def thread_tree_to_json(thread_group):
    json_root = {}
    threads = []
    for th_info in thread_group:
        frame_list = []
        frame_tree_to_json(th_info.frame_tree, th_info.top_node, frame_list)
        th = {"threadID": th_info.thread_id, "func": frame_list}
        threads.append(th)
    json_root["threads"] = threads
    return json_root


def frame_tree_to_json(frame_tree, node, frame_list):
    child_frame_list = []
    func_name = node.func_name
    if func_name == "":
        func_name = node.address
    frame = {"funcname": func_name, "module": node.module,
             "selfWeight": node.self_weight, "weight": node.all_weight, "children": child_frame_list}
    frame_list.append(frame)

    if len(frame_tree) == 0:
        return
    if node.key not in frame_tree:
        return
    children = frame_tree[node.key]
    if not children:
        return
    for child in children:
        frame_tree_to_json(frame_tree, child, child_frame_list)


def write_json_to_file(save_path, json_data):
    with open(save_path, "w") as f:
        json_str = json.dumps(json_data)
        f.write(json_str)


def get_key(frame_index, address):
    return str(frame_index) + " " + str(address)


def analyse_group(xml_file, json_file, txt_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # step 1
    pattern = get_all_id(root)

    # step 2
    thread_group, address_list = get_thread_group(root, pattern)
    print_thread_group(thread_group, pattern)

    # get symbol address
    module_file = '/Users/mjzheng/Downloads/ios_data/2021-04-08_17_23_22/20210408172529188_ori.crash'
    address_symbol = symbol_parser.symbol_with_file(module_file, address_list)
    #address_symbol = {}

    # step 3
    threads = get_thread_tree(thread_group, pattern)

    symbol_thread_tree(threads, address_symbol)

    # step
    txt_tree = print_thread_tree(threads)
    write_txt_to_file(txt_file, txt_tree)

    # step 4
    json_data = thread_tree_to_json(threads)
    write_json_to_file(json_file, json_data)
    return


def symbol_thread_tree(thread_group, address_symbol):
    for th_info in thread_group:
        symbol_frame_tree(th_info.frame_tree, th_info.top_node, address_symbol)


def symbol_frame_tree(frame_tree, node, address_symbol):
    if node.address in address_symbol:
        symbol = address_symbol[node.address]
        node.module = symbol.module_name
        node.func_name = symbol.func_name
    if len(frame_tree) == 0:
        return
    if node.key not in frame_tree:
        return
    children = frame_tree[node.key]
    if not children:
        return
    for frame in children:
        symbol_frame_tree(frame_tree, frame, address_symbol)
    return


if __name__ == "__main__":
    print('hello')
