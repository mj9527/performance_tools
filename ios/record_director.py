# coding=utf-8
import record_apple
import content_parser
import stack_parser
import sys
sys.path.append("..")
import flame_graph
import setting


def get_time_file(file_list):
    for file_name in file_list:
        if file_name.find('time-profile') != -1:
            print ('start analyze file ', file_name)
            return file_name
    return ""


def record_apple_config():
    if setting.apple_type == 'ios':
        print ('record ios')
        trace_file, prefix, ret = record_apple.record_ios_with_config()
        return trace_file, prefix, ret
    else:
        trace_file, prefix, ret = record_apple.record_mac_with_config()
        return trace_file, prefix, ret


def start():
    trace_file, prefix, ret = record_apple_config()
    if ret != 0:
        return

    print (trace_file)
    print (prefix)

    print ('start parse content')
    file_list = content_parser.get_schema_list(trace_file, prefix)
    time_file = get_time_file(file_list)
    if time_file == "":
        return
    print (time_file)

    # time_file = '/Users/mjzheng/Downloads/ios_data/2021-04-08_17_23_22/2021-04-08_17_23_22_time-profile.xml'
    # prefix = '/Users/mjzheng/Downloads/ios_data/2021-04-08_17_23_22/2021-04-08_17_23_22'

    # time_file = '/Users/mjzheng/Downloads/ios_data/2021-04-12_10_26_28/2021-04-12_10_26_28_time-profile.xml'
    # prefix = '/Users/mjzheng/Downloads/ios_data/2021-04-12_10_26_28/2021-04-12_10_26_28'

    json_file = prefix + '.json'
    txt_file = prefix + '.txt'
    module_file = prefix + '.log'
    stack_parser.analyse_group(time_file, json_file, txt_file, module_file)

    flame_file = prefix + "_flame.html"
    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    flame_graph.get_flamegrap_from_json(json_file, flame_file)


if __name__ == "__main__":
    start()
