# coding=utf-8
import record_apple
import content_parser
import stack_parser
import sys
sys.path.append("..")
import flame_graph
import setting
import base_utils


def start():
    output_dir, prefix = base_utils.get_work_dir_and_prefix_with_config()
    trace_file, ret = record_apple.record_apple_config(prefix)
    if ret != 0:
        return

    print ('start parse content ', trace_file)
    time_file = content_parser.export_schema(trace_file, 'time-profile', prefix)

    # prefix = '/Users/mjzheng/Downloads/ios_data/2021-04-08_17_23_22/2021-04-08_17_23_22'
    # time_file = prefix + '_time-profile.xml'

    json_file = stack_parser.analyse_group(time_file, prefix)

    flame_file = prefix + "_flame.html"
    flame_graph.get_flamegrap_from_json(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)


if __name__ == "__main__":
    start()
