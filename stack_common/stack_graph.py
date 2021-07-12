# coding=utf-8
import json
import os
from drawtools.flamegraph_formatter import flame_formatting
from drawtools.sunburst_formatter import sunburst_formatting
import stack_json


def get_flame_graph(file_name, html_file, json_file):
    flame_json = flame_formatting(file_name)
    stack_json.write_json_file(flame_json, json_file)
    s = json.dumps(flame_json, indent=2)
    a = s.replace('\r', '').replace('\n', '').replace(' ', '').replace('"', r'\"')
    with open(os.getcwd() + '/drawtools/flamegraph_template.html', 'r') as fr:
        sr = fr.read()
        out = sr.replace('__TEMP__', a)
        with open(html_file, 'w') as fw:
            fw.write(out)
        print("flamegrap html:" + html_file)


def get_sunburst_graph(file_name, html_file):
    sunburst_json = sunburst_formatting(file_name)
    s = json.dumps(sunburst_json, indent=2)
    # print(s)
    a = s.replace('\r', '').replace('\n', '').replace("\\", "\\\\").replace(' ', '').replace('"', r'\"')
    with open(os.getcwd() + '/drawtools/sunburst_template.html', 'r') as fr:
        sr = fr.read()
        out = sr.replace('__TEMP__', a)
        with open(html_file, 'w') as fw:
            fw.write(out)
        print("sunburstgraph html:" + html_file)


if __name__ == '__main__':
    PREFIX = "/Users/mjzheng/Downloads/ios_data/2021-03-30_19_27_05/2021-03-30_19_27_05"
    JSON_FILE = PREFIX + ".json"
    FLAME_FILE = PREFIX + "_flame.html"
    SUNBURST_FILE = PREFIX + "_sunburst.html"
    get_flame_graph(JSON_FILE, SUNBURST_FILE)
    get_sunburst_graph(JSON_FILE, FLAME_FILE)
