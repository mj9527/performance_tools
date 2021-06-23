# coding=utf-8
import base_def


def take_weight(elem):
    return elem.data.all_weight


def collapse_stack(std_stack_list):
    stack_group_dict = group_stack(std_stack_list)
    stack_collapse_list = collapse_stack_group_list(stack_group_dict)
    stack_collapse_list.sort(key=take_weight)
    stack_collapse_list = stack_collapse_list[::-1]
    #print_collapse_stack_start_func(stack_collapse_list)
    return stack_collapse_list


def print_collapse_stack_start_func(stack_collapse_list):
    for root in stack_collapse_list:
        if root.data.module == 'xcast':
            print 'collpase top frame ', root.data.module, '', root.data.func_name


def group_stack(std_stack_list):
    stack_group_dict = {}
    for std_stack in std_stack_list:
        start_func = std_stack.frame_list[0].func_name
        if start_func in stack_group_dict.keys():
            stack_group = stack_group_dict[start_func]
            stack_group.append(std_stack)
        else:
            stack_group = [std_stack]
            stack_group_dict[start_func] = stack_group
    print len(stack_group_dict)
    return stack_group_dict


def collapse_stack_group_list(stack_group_list):
    stack_collapse_list = []
    for start_func, stack_group in stack_group_list.items():
        root = base_def.TreeNode(None)
        collapse_stack_group(root, stack_group)
        stack_collapse_list.append(root.child_list[0])
    return stack_collapse_list


def collapse_stack_group(root, stack_group):
    for std_stack in stack_group:
        child_list = root.child_list
        for index, frame in enumerate(std_stack.frame_list):
            child = get_child_node(child_list, frame)
            child_list = child.child_list


def get_child_node(child_list, frame):
    for child in child_list:
        data = child.data
        if data.index == frame.index and data.func_name == frame.func_name:
            data.self_weight += frame.self_weight
            data.all_weight += frame.all_weight
            return child
    child = base_def.TreeNode(frame)
    child_list.append(child)
    return child

