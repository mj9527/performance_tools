# coding=utf-8
import os
import time
import base_utils
import setting

START_CMD_PARAM = ' -start CPU -filemode'


def start_capture(wpr_app_path):
    if not os.path.exists(wpr_app_path):
        print("wpr tool not found")
        return False
    cmd = wpr_app_path + START_CMD_PARAM
    try:
        os.popen(cmd).read()
    except Exception as e:
        raise e
    return True


def stop_capture(wpr_app_path, etl_file):
    if not os.path.exists(wpr_app_path):
        print("wpr tool not found")
        return False
    cmd = wpr_app_path + " -stop " + etl_file
    try:
        os.popen(cmd).read()
    except Exception as e:
        raise e
    return True


def record(wpt_dir, etl_file, interval):
    wpr_app_path = wpt_dir + "\\wpr.exe"
    ret = start_capture(wpr_app_path)
    if not ret:
        return None
    time.sleep(interval)
    ret = stop_capture(wpr_app_path, etl_file)
    if not ret:
        return None


def record_windows_with_config():
    output_dir, prefix = base_utils.get_work_dir_and_prefix(setting.windows_output_dir)
    etl_file = prefix + '.etl'
    record(setting.wpt_dir, etl_file, setting.run_time)
    return output_dir, etl_file, prefix

