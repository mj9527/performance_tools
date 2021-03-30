# -*- coding: UTF-8 -*-
import json


def replace_key_if_exists(input_dict, old_key, new_key):
    if old_key not in input_dict:
        return

    input_dict[new_key] = input_dict[old_key]
    del input_dict[old_key]


def flame_dfs(flame_dict):
    replace_key_if_exists(flame_dict, "threads", "children")
    replace_key_if_exists(flame_dict, "threadID", "name")
    replace_key_if_exists(flame_dict, "func", "children")
    replace_key_if_exists(flame_dict, "funcname", "name")
    replace_key_if_exists(flame_dict, "weight", "value")

    if "name" in flame_dict:
        flame_dict["name"] = str(flame_dict["name"])

    for child in flame_dict["children"]:
        flame_dfs(child)


def flame_formatting(data_json_file):
    data_dict = {}
    with open(data_json_file, 'r') as f:
        data_dict = json.load(f)
    total_value = 0

    for thread in data_dict["threads"]:
        thread_value = 0
        for func in thread["func"]:
            thread_value += func["weight"]
        thread["value"] = thread_value
        total_value += thread_value

    data_dict["name"] = data_json_file
    data_dict["value"] = total_value

    flame_dfs(data_dict)
    return data_dict
