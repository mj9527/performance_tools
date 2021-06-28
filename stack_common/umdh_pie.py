# coding=utf-8
from pyecharts import Pie
from pyecharts import Bar


def show_kv_pie(kv, prefix):
    attr_list = []
    value_list = []
    for key, value in kv.items():
        attr_list.append(key)
        value_list.append(value)
    pie_file = prefix + '_pie.html'
    show_pie(attr_list, value_list, pie_file)
    # bar_file = prefix + '_bar.html'
    # show_bar(attr_list, value_list, bar_file)


def show_pie(attr_list, value_list, output_file):
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


def show_bar(attr_list, value_list, output_file):
    bar = Bar()
    bar.add('',  # label
            attr_list,  # 横坐标
            value_list,  # 纵坐标
            is_more_utils=True)  # 设置最右侧工具栏
    bar.render(output_file)


if __name__ == "__main__":
    print 'none'