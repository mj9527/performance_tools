# coding=utf-8
import record_windows
import etl_parser
import setting
import os
import flame_graph


def cap_dump_json():
    output_dir, csv_file, prefix = record_windows.record_export_with_config()
    # etl_file = "C:/Users/mjzheng/Documents/WPR Files/mjzheng-PC3.03-31-2021.19-28-35.etl"
    # prefix = setting.windows_output_dir + "12"
    # csv_file = record_windows.export_csv(setting.wpt_dir, etl_file, setting.windows_output_dir)

    json_file = prefix + '.json'
    etl_parser.csv_to_json(csv_file, json_file)

    flame_file = prefix + "_flame.html"
    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    flame_graph.get_flamegrap_from_json(json_file, flame_file)
    return json_file


if __name__ == "__main__":
    cap_dump_json()