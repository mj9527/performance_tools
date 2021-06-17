# coding=utf-8
import json


def get_txt_file(stack_collapse_list, file_name):
    txt_data = get_txt_data(stack_collapse_list)
    write_txt_file(txt_data, file_name)
    return file_name


def get_txt_data(stack_collapse_list):
    threads = []
    for index, root in enumerate(stack_collapse_list):
        frame_list = []
        scan_tree_preorder_dfs(root.child_list[0], frame_list)
        threads.append(frame_list)
    return threads


def scan_tree_preorder_dfs(node, frame_list):
    frame = get_frame_txt_data(node.data)
    frame_list.append(frame)
    for child in node.child_list:
        scan_tree_preorder_dfs(child, frame_list)
    return frame


def get_frame_txt_data(origin_frame):
    frame_info = ""
    for i in range(origin_frame.index):
        frame_info += ' '
    frame_info += str(origin_frame.index) + ' '
    frame_info += origin_frame.address
    frame_info += ' ' + str(origin_frame.all_weight)
    return frame_info


def write_txt_file(list_data, file_name):
    with open(file_name, "w") as f:
        for frame_list in list_data:
            for frame in frame_list:
                f.write(str(frame))
                print (frame)
                f.write('\n')
        f.close()


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

