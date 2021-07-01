# coding=utf-8

def write_perf(std_stack_list, save_path):
    j = 1
    with open(save_path, "w") as f:
        for _, thread_stack_list in std_stack_list.items():
            for thread_stack in thread_stack_list:
                thread_name = str(j) + "    " + str(j) + "    " + str(thread_stack.alloc_size) \
                              + ":   " + str(thread_stack.alloc_size) + " cpu-clock:\n"
                f.write(thread_name)
                frame_list = thread_stack.frame_list[::-1]
                for _, frame_info in enumerate(frame_list):
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
        for _, thread_stack_list in std_stack_list.items():
            for thread_stack in thread_stack_list:
                #thread_name = str(j) + "    " + str(j) + "    " + str(thread_stack.alloc_size)
                # + ":   " + str(thread_stack.alloc_size) + " cpu-clock:\n"
                #f.write(thread_name)
                frame_list = thread_stack.frame_list[::-1]
                for _, frame_info in enumerate(frame_list):
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
            thread_name = str(stack_id) + "    " + str(stack_id) + "    " + str(std_stack.weight) + ":   " \
                          + str(std_stack.weight) + " cpu-clock:\n"
            f.write(thread_name)
            for _, frame in enumerate(std_stack.frame_list):
                frame = "       0 " + frame.func_name + ' ([' + frame.module + '])' + '\n'
                f.write(frame)
            f.write('\n')
        f.close()


def write_std_flame_file(std_stack_list, save_path):
    with open(save_path, "w") as f:
        for stack_id, std_stack in enumerate(std_stack_list):
            stack_line = ''
            for _, frame in enumerate(std_stack.frame_list):
                stack_line += ';' + frame.func_name
            stack_line += ' ' + str(std_stack.weight) + '\n'
            f.write(stack_line)
        f.close()


def read_std_flame_file(file_name):
    f = open(file_name)
    lines = []
    line = f.readline()
    while line:
        lines.append(line)
        line = f.readline()
    f.close()
    return lines


if __name__ == "__main__":
    FILE_NAME = '/Users/mjzheng/Downloads/ios_data/2021-07-01_10_48_52/2021-07-01_10_48_52_std_stack.txt'
    read_std_flame_file(FILE_NAME)