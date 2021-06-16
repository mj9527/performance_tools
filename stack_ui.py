# coding=utf-8
import stack_printer
import flame_graph


def display_stack(json_data, prefix):
    json_file = prefix + '.json'
    stack_printer.write_json_file(json_file, json_data)

    flame_file = prefix + "_flame.html"
    flame_graph.get_flamegrap_from_json(json_file, flame_file)

    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    return json_file
