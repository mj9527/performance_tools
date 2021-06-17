# coding=utf-8
from pyecharts import Pie
import datetime


def show_memory_dic(module_to_size, output_dir):
    attr_list = []
    value_list = []
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    output_file = output_dir + current_time + '_memory_pie.html'
    for key, value in module_to_size.items():
        attr_list.append(key)
        value_list.append(value)
    show_memory(attr_list, value_list, output_file)


def show_memory(attr_list, value_list, output_file):
    pie = Pie(width='1000px', height='600px')
    pie.add(
        "",
        attr_list,
        value_list,
        is_label_show=True,
        #legend_orient='vertical',
        #legend_pos='left',
        center=["50%", "60%"]
    )
    pie.render(path=output_file)


if __name__ == "__main__":
    print 'none'