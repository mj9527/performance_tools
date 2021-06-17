# coding=utf-8
import json


def get_json_file(stack_collapse_list, file_name):
    json_data = get_json_data(stack_collapse_list)
    write_json_file(json_data, file_name)
    return file_name


def get_json_data(stack_collapse_list):
    threads = []
    for index, root in enumerate(stack_collapse_list):
        frame = scan_tree_postorder_dfs(root.child_list[0])
        child_list = [frame]
        thread = {"threadID": index+1, "func": child_list}
        threads.append(thread)
    json_root = {"threads": threads}
    return json_root


def scan_tree_postorder_dfs(node):
    child_format_list = []
    for child in node.child_list:
        child_format = scan_tree_postorder_dfs(child)
        child_format_list.append(child_format)
    frame = get_frame_json_data(node.data, child_format_list)
    return frame


def get_frame_json_data(origin_frame, child_frame_list):
    func_name = origin_frame.func_name
    if func_name == "":
        func_name = origin_frame.address
    frame = { "funcname": func_name,
              "module": origin_frame.module,
              "selfWeight": origin_frame.self_weight,
              "weight": origin_frame.all_weight,
              "children": child_frame_list}
    return frame


def write_json_file(json_data, file_name):
    with open(file_name, "w") as f:
        json_str = json.dumps(json_data)
        f.write(json_str)
        f.close()

