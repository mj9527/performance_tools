# coding=utf-8
import record_apple
import content_parser
import stack_parser
import sys
sys.path.append("..")
import flame_graph


def get_time_file(file_list):
    for file_name in file_list:
        if file_name.find('time-profile') != -1:
            print ('start analyze file ', file_name)
            return file_name
    return ""


def start():
    trace_file, prefix, ret = record_apple.record_ios_with_config()
    if ret != 0:
        return

    print ('start parse content')
    file_list = content_parser.get_schema_list(trace_file, prefix)
    time_file = get_time_file(file_list)
    if time_file == "":
        return
    json_file = prefix + '.json'
    txt_file = prefix + '.txt'
    stack_parser.analyse_group(time_file, json_file, txt_file)

    flame_file = prefix + "_flame.html"
    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    flame_graph.get_flamegrap_from_json(json_file, flame_file)


if __name__ == "__main__":
    start()
