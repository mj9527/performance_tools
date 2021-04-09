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
        self.backtrace_detail = detail


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


def get_thread_tree(thread_id_to_backtrace_list, id_to_item):
    threads = []
    for (thread_id, backtrace_list) in thread_id_to_backtrace_list.items():
        thread_name = get_thread_name(thread_id, id_to_item)
        # if thread_name.find('pthread_start 0x18fecc') == -1:
        #     continue
        # print ('the same ....', thread_name)
        thread_root = NodeInfo(thread_id, FrameInfo(0, thread_name, 0))
        scan_all_backtrace(thread_root, backtrace_list)
        threads.append(thread_root)
    return threads


def scan_all_backtrace(root, thread):
    for (backtrace_id, bt) in thread.items():
        child_list = root.child_list
        backtrace_detail = bt.backtrace_detail
        for index, address in enumerate(backtrace_detail):
            child, found = get_node(child_list, index, address, bt.weight)
            if found == 0:
                child_list.append(child)
            child_list = child.child_list
    for top_node in root.child_list:
        root.node.self_weight += top_node.node.self_weight
        root.node.all_weight += top_node.node.all_weight


def get_node(child_list, index, address, weight):
    for child in child_list:
        node = child.node
        if node.index == index and node.address == address:
            node.self_weight += weight
            node.all_weight += weight
            return child, 1
    child = NodeInfo(0, FrameInfo(index, address, weight))
    return child, 0


def get_thread_name(thread_id, id_to_item):
    thread_item = id_to_item.get(thread_id)
    thread_name = thread_item.attrib.get('fmt')
    word_list = thread_name.split()
    if len(word_list) >= 2:
        thread_name = word_list[0] + " " + word_list[1]
    return thread_name


def write_txt_to_file(save_path, list_data):
    with open(save_path, "w") as f:
        for frame_list in list_data:
            for frame in frame_list:
                f.write(str(frame))
                print (frame)
                f.write('\n')
        f.close()


def thread_tree_to_json(thread_group):
    json_root = {}
    threads = []
    for th_info in thread_group:
        frame_list = []
        frame_tree_to_json(th_info, frame_list)
        th = {"threadID": th_info.thread_id, "func": frame_list}
        threads.append(th)
    json_root["threads"] = threads
    return json_root


def frame_tree_to_json(child, frame_list):
    child_frame_list = []
    node = child.node
    func_name = node.func_name
    if func_name == "":
        func_name = node.address
    frame = {"funcname": func_name, "module": node.module,
             "selfWeight": node.self_weight, "weight": node.all_weight, "children": child_frame_list}
    frame_list.append(frame)

    if not child.child_list:
        return
    if len(child.child_list) == 0:
        return

    for child in child.child_list:
        frame_tree_to_json(child, child_frame_list)


def write_json_to_file(save_path, json_data):
    with open(save_path, "w") as f:
        json_str = json.dumps(json_data)
        f.write(json_str)


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
    threads = get_thread_tree(thread_id_to_backtrace_list, id_to_item)

    if setting.symbol_parse == 1:
        symbol_thread_tree(threads, address_symbol)

    # step
    txt_tree = stack_printer.print_thread_tree(threads)
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
