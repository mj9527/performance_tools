# coding=utf-8
import datetime
import umdh_file_parser
import sys
sys.path.append("..")
import setting
import base_def
import stack_printer
import flame_graph


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
    stack_list = umdh_file_parser.base_parser(file_name)

    # thread_tree_list = get_thread_tree_list(stack_list)

    thread_to_stack_list = group_stack(stack_list)

    thread_tree_list = get_all_thread_tree(thread_to_stack_list)

    # step 1, get stack alloc size and reverse stack

    # step 2
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time

    # perf_data = prefix + '.perf'
    # write_perf(thread_to_stack_list, perf_data)

    perf_data = prefix + '.perf'
    write_memory_perf(thread_to_stack_list, perf_data)
    return

    json_file = prefix + '.json'
    json_data = stack_printer.get_json_data(thread_tree_list)
    stack_printer.write_json_file(json_file, json_data)

    text_file = prefix + '.txt'
    text_data = stack_printer.get_txt_data(thread_tree_list)
    stack_printer.write_txt_file(text_file, text_data)

    flame_file = prefix + "_flame.html"
    flame_graph.get_flamegrap_from_json(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    return json_file


def write_perf(thread_to_stack_list, save_path):
    j = 1
    with open(save_path, "w") as f:
        for start_func, thread_stack_list in thread_to_stack_list.items():
            for thread_stack in thread_stack_list:
                thread_name = str(j) + "    " + str(j) + "    " + str(thread_stack.alloc_size) + ":   " + str(thread_stack.alloc_size) + " cpu-clock:\n"
                f.write(thread_name)
                frame_list = thread_stack.frame_list[::-1]
                for index, frame_info in enumerate(frame_list):
                    if frame_info.module == '<no module>':
                        frame_info.module = '[unknown]'
                        frame_info.func_name = '[unknown]'
                    frame = "       0 " + frame_info.func_name + ' ([' + frame_info.module + '])' + '\n'
                    f.write(frame)
                f.write('\n')
            j = j+1
        f.close()


def write_memory_perf(thread_to_stack_list, save_path):
    j = 1
    with open(save_path, "w") as f:
        for start_func, thread_stack_list in thread_to_stack_list.items():
            for thread_stack in thread_stack_list:
                #thread_name = str(j) + "    " + str(j) + "    " + str(thread_stack.alloc_size) + ":   " + str(thread_stack.alloc_size) + " cpu-clock:\n"
                #f.write(thread_name)
                frame_list = thread_stack.frame_list[::-1]
                for index, frame_info in enumerate(frame_list):
                    if frame_info.module == '<no module>':
                        frame_info.module = '[unknown]'
                        frame_info.func_name = '[unknown]'
                    frame = "       " + frame_info.func_name + '\n'
                    f.write(frame)
                f.write("       " + str(thread_stack.alloc_size) + '\n')
                f.write('\n')
            j = j+1
        f.close()


def group_stack(stack_list):
    thread_to_stack_list = {}
    for thread_stack in stack_list:
        start_func = thread_stack.frame_list[0].func_name
        if start_func in thread_to_stack_list.keys():
            thread_stack_list = thread_to_stack_list[start_func]
            thread_stack_list.append(thread_stack)
        else:
            thread_stack_list = [thread_stack]
            thread_to_stack_list[start_func] = thread_stack_list
    print len(thread_to_stack_list)
    return thread_to_stack_list


def get_all_thread_tree(thread_to_stack_list):
    thread_tree_list = []
    index = 1
    for start_func, thread_stack_list in thread_to_stack_list.items():
        root = base_def.NodeInfo(index, base_def.FrameInfo(0, "", 0))
        get_thread_tree2(root, thread_stack_list)
        thread_tree_list.append(root)
        index = index + 1
        # if index == 10:
        #     break
    return thread_tree_list


def get_thread_tree2(root, thread_stack_list):
    for thread_stack in thread_stack_list:
        child_list = root.child_list
        address_list = thread_stack.frame_list
        weight = thread_stack.alloc_size
        for index, frame_info in enumerate(address_list):
            child = get_child_node2(child_list, index, frame_info, weight)
            child_list = child.child_list
    for child in root.child_list:
        root.node.self_weight += child.node.self_weight
        root.node.all_weight += child.node.all_weight
        root.node.module = child.node.module
        root.node.func_name = child.node.func_name


def get_child_node2(child_list, index, frame_info, weight):
    for child in child_list:
        node = child.node
        if node.index == frame_info.index and node.func_name == frame_info.func_name:
            node.self_weight += weight
            node.all_weight += weight
            return child
    child = base_def.NodeInfo(0, frame_info)
    child_list.append(child)
    return child


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    json_parser(file_name, output_dir)


