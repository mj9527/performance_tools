# coding=utf-8
import os
import time
import sys
sys.path.append("..")
import base_utils
import setting


def start_capture(wpr):
    cmd = wpr + ' -start CPU -filemode'
    print(cmd)
    os.popen(cmd).read()


def stop_capture(wpr, etl_file):
    cmd = wpr + " -stop " + etl_file
    print(cmd)
    os.popen(cmd).read()


def record(wpt_dir, etl_file, interval):
    wpr = wpt_dir+"wpr.exe"
    wpr = add_double_quote(wpr)
    start_capture(wpr)
    time.sleep(interval)
    stop_capture(wpr, etl_file)


def add_double_quote(origin_str):
    return "\"" + origin_str + "\""


def export_csv(wpt_dir, etl_file, output_dir):
    wpa_exporter = wpt_dir+"wpaexporter.exe"
    print(wpa_exporter)
    profile_file = os.getcwd() + '\\cpuusage.wpaProfile'
    cmd = add_double_quote(wpa_exporter) \
          + " -i " + etl_file \
          + " -profile " + profile_file \
          + " -outputfolder " + output_dir \
          + " -symbols"
    print(cmd)
    os.popen(cmd).read()
    csv_file = output_dir + "CPU_Usage_(Sampled)_Utilization_by_Process,_Thread,_Stack.csv"
    print(csv_file)
    return csv_file


def record_windows_with_config():
    output_dir, prefix = base_utils.get_work_dir_and_prefix_with_config()
    etl_file = prefix + '.etl'
    record(setting.wpt_dir, etl_file, setting.run_time)
    return output_dir, etl_file, prefix


def record_export_with_config():
    output_dir, etl_file, prefix = record_windows_with_config()
    csv_file = export_csv(setting.wpt_dir, etl_file, output_dir)
    return output_dir, csv_file, prefix


