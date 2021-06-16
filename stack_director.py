# coding=utf-8
import datetime
import stack_tree
import stack_printer
import stack_ui
import setting


def start_play(std_stack_list, output_dir):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    prefix = output_dir + current_time

    stack_collapse_list = stack_tree.collapse_stack(std_stack_list)

    json_data = stack_printer.get_json_data(stack_collapse_list)

    stack_ui.display_stack(json_data, prefix)


if __name__ == "__main__":
    file_name = setting.input_memory_file
    output_dir = setting.output_memory_dir
    #json_parser(file_name, output_dir)


