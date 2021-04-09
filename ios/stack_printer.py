


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


def print_thread_tree(thread_group):
    threads = []
    for th_info in thread_group:
        frame_list = []
        index = 1
        print_frame_tree(th_info, frame_list, index)
        threads.append(frame_list)
    return threads


def print_frame_tree(child, frame_list, index):
    frame = print_frame(child.node)
    frame_list.append(frame)
    if not child.child_list:
        return
    if len(child.child_list) == 0:
        return
    for node in child.child_list:
        print_frame_tree(node, frame_list, index+1)
    return


def print_frame(node):
    frame_info = ""
    for i in range(node.index):
        frame_info += ' '
    frame_info += str(node.index) + ' '
    frame_info += node.address
    frame_info += ' ' + str(node.all_weight)
    return frame_info