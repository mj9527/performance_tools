# coding=utf-8


def write_perf(std_stack_list, save_path):
    j = 1
    with open(save_path, "w") as f:
        for start_func, thread_stack_list in std_stack_list.items():
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


def write_memory_perf(std_stack_list, save_path):
    j = 1
    with open(save_path, "w") as f:
        for start_func, thread_stack_list in std_stack_list.items():
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


def write_stack_file(std_stack_list, save_path):
    with open(save_path, "w") as f:
        for stack_id, std_stack in enumerate(std_stack_list):
            thread_name = str(stack_id) + "    " + str(stack_id) + "    " + str(std_stack.weight) + ":   " + str(std_stack.weight) + " cpu-clock:\n"
            f.write(thread_name)
            for index, frame in enumerate(std_stack.frame_list):
                frame = "       0 " + frame.func_name + ' ([' + frame.module + '])' + '\n'
                f.write(frame)
            f.write('\n')
        f.close()
