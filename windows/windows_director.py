import record_windows
import etl_parser
import setting
import os
import flame_graph


def export_csv(wpa_exporter, etl_file, profile_file, export_dir):
    if not os.path.exists(wpa_exporter):
        print("wpaexporter tool not found")
        return False

    if not os.path.exists(etl_file):
        print("etl file not found")
        return False

    if not os.path.exists(profile_file):
        print("profile file not found")
        return False

    cmd = wpa_exporter + " -i " + etl_file + " -profile " + profile_file + \
          " -outputfolder " + export_dir + " -symbols"
    try:
        os.popen(cmd).read()
    except Exception as e:
        raise e
    return True


def cap_dump_json(profile_file):
    output_dir, etl_file, prefix = record_windows.record_windows_with_config()

    profile_file = os.getcwd() + '/cpuusage.wpaProfile'
    wpa_exporter = setting.wpt_dir + "\\wpaexporter.exe"
    ret = export_csv(wpa_exporter, etl_file, profile_file, output_dir)
    if not ret:
        return None

    json_file = prefix + '.json'
    csv_file = output_dir + "\\CPU_Usage_(Sampled)_Utilization_by_Process,_Thread,_Stack.csv"
    etl_parser.csv_to_json(csv_file, json_file)

    flame_file = prefix + "_flame.html"
    sunburst_file = prefix + "_sunburst.html"
    flame_graph.get_sunburstgraph_from_json(json_file, sunburst_file)
    flame_graph.get_flamegrap_from_json(json_file, flame_file)
    return json_file

