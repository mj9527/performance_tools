# coding=utf-8
import datetime
import stack_tree
import stack_json
import stack_txt
import stack_graph
import unify_input_file


def take_four(elem):
    return elem.weight


def sort_stack_list(std_stack_list):
    std_stack_list.sort(key=take_four)
    std_stack_list = std_stack_list[::-1]
    return std_stack_list


def start_play(std_stack_list, prefix):
    sort_file = prefix + '_sort.txt'
    std_stack_list = sort_stack_list(std_stack_list)
    unify_input_file.write_stack_file(std_stack_list, sort_file)

    stack_collapse_list = stack_tree.collapse_stack(std_stack_list)
    generate_graph(stack_collapse_list, prefix)
    return std_stack_list


def start_play2(stack_group_dict, prefix):
    stack_collapse_list = stack_tree.collapse_stack_group_list(stack_group_dict)
    generate_graph(stack_collapse_list, prefix)
    

def generate_graph(stack_collapse_list, prefix):
    json_file = prefix + '.json'
    stack_json.get_json_file(stack_collapse_list, json_file)

    txt_file = prefix + '.txt'
    stack_txt.get_txt_file(stack_collapse_list, txt_file)

    flame_file = prefix + "_flame.html"
    stack_graph.get_flame_graph(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    stack_graph.get_sunburst_graph(json_file, sunburst_file)
