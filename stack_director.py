# coding=utf-8
import datetime
import stack_tree
import stack_json
import stack_txt
import stack_graph


def start_play(std_stack_list, output_dir):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time

    stack_collapse_list = stack_tree.collapse_stack(std_stack_list)

    json_file = prefix + '.json'
    stack_json.get_json_file(stack_collapse_list, json_file)

    txt_file = prefix + '.txt'
    stack_txt.get_txt_file(stack_collapse_list, txt_file)

    flame_file = prefix + "_flame.html"
    stack_graph.get_flame_graph(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    stack_graph.get_sunburst_graph(json_file, sunburst_file)


def start_play2(stack_group_dict, prefix):
    stack_collapse_list = stack_tree.collapse_stack_group_list(stack_group_dict)

    json_file = prefix + '.json'
    stack_json.get_json_file(stack_collapse_list, json_file)

    txt_file = prefix + '.txt'
    stack_txt.get_txt_file(stack_collapse_list, txt_file)

    flame_file = prefix + "_flame.html"
    stack_graph.get_flame_graph(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    stack_graph.get_sunburst_graph(json_file, sunburst_file)
