# coding=utf-8
import json


def print_all_id(dict):
    print ('len', len(dict))
    for key in dict:
        print (key, dict[key])


def print_thread_backtrace(thread_group, id_to_item):
    for (thread_id, thread) in thread_group.items():
        thread_item = id_to_item.get(thread_id)
        thread_name = thread_item.attrib.get('fmt')
        print (thread_name)
        for (backtrace_id, bt) in thread.items():
            detail = bt.address_list
            print (detail, bt.weight)
        print ('\n')


def get_txt_data(thread_tree_list):
    threads = []
    for thread_tree in thread_tree_list:
        frame_list = []
        get_tree_txt_data(thread_tree, frame_list)
        threads.append(frame_list)
    return threads


def get_tree_txt_data(child, frame_list):
    frame = get_node_txt_data(child.node)
    frame_list.append(frame)
    if not child.child_list:
        return
    if len(child.child_list) == 0:
        return
    for node in child.child_list:
        get_tree_txt_data(node, frame_list)
    return


def get_node_txt_data(node):
    frame_info = ""
    for i in range(node.index):
        frame_info += ' '
    frame_info += str(node.index) + ' '
    frame_info += node.address
    frame_info += ' ' + str(node.all_weight)
    return frame_info


def get_json_data(stack_collapse_list):
    threads = []
    fmt_func = get_node_json_data
    for index, root in enumerate(stack_collapse_list):
        frame = scan_tree_postorder_dfs(root.child_list[0], fmt_func)
        child_list = [frame]
        thread = {"threadID": index+1, "func": child_list}
        threads.append(thread)
    json_root = {"threads": threads}
    return json_root


def scan_tree_postorder_dfs(node, fmt_func):
    child_format_list = []
    for child in node.child_list:
        child_format = scan_tree_postorder_dfs(child, fmt_func)
        child_format_list.append(child_format)
    #frame = get_node_json_data(node.data, child_format_list)
    frame = fmt_func(node.data, child_format_list)
    return frame


def get_node_json_data(node, child_frame_list):
    func_name = node.func_name
    if func_name == "":
        func_name = node.address
    frame = { "funcname": func_name,
              "module": node.module,
              "selfWeight": node.self_weight,
              "weight": node.all_weight,
              "children": child_frame_list}
    return frame


def write_json_file(save_path, json_data):
    with open(save_path, "w") as f:
        json_str = json.dumps(json_data)
        f.write(json_str)


def write_txt_file(save_path, list_data):
    with open(save_path, "w") as f:
        for frame_list in list_data:
            for frame in frame_list:
                f.write(str(frame))
                print (frame)
                f.write('\n')
        f.close()
