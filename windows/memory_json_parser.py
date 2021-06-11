# coding=utf-8
import flame_graph
import datetime
import memory_file_parser
import sys
sys.path.append("..")
import setting
import base_def
import stack_printer


def get_thread_tree_list(stack_list):
    thread_tree_list = []
    for thread_stack in stack_list:
        thread_name = ""
        thread_id = thread_stack.thread_id
        root = base_def.NodeInfo(thread_id, base_def.FrameInfo(0, thread_name, thread_stack.alloc_size))
        get_thread_tree(root, thread_stack)
        thread_tree_list.append(root)
    return thread_tree_list


def get_thread_tree(root, thread_stack):
    child_list = root.child_list
    for info in thread_stack.frame_list:
        child = base_def.NodeInfo(thread_stack.thread_id, info)
        child_list.append(child)
        child_list = child.child_list


def json_parser(file_name, output_dir):
    stack_list = memory_file_parser.base_parser(file_name)

    # step 1, get stack alloc size and reverse stack
    thread_tree_list = get_thread_tree_list(stack_list)

    # step 2
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time

    json_file = prefix + '.json'
    json_data = stack_printer.get_json_data(thread_tree_list)
    stack_printer.write_json_file(json_file, json_data)

    flame_file = prefix + "_flame.html"
    flame_graph.get_flamegrap_from_json(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    return json_file


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    json_parser(file_name, output_dir)


