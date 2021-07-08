# coding=utf-8
import os
import time


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
    profile_file = os.getcwd() + '\\windows\\cpuusage.wpaProfile'
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
