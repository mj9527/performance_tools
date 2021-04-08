# coding=utf-8
import subprocess
import os
import sys
sys.path.append("..")
import setting
import base_utils


def get_pid(sync_cmd, bundle_id):
    print ('start get pid')
    print (sync_cmd)
    child = subprocess.Popen(sync_cmd, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = child.communicate()
    # print ('start parse')
    lines = stdout.splitlines()
    for row in lines:
        print (row)
        if row.find(bundle_id) != -1:
            words = row.split()
            pid = words[0]
            print (pid)
            return pid
    return 0


def record(uuid, pid, template, interval, file_name):
    if pid == 0:
        print ('failed to get process id')
        return 1

    cmd = "xcrun xctrace record --template '" + template + \
          "' --attach " + str(pid) + \
          " --output " + file_name + \
          " --device " + uuid + \
          " --time-limit " + str(interval) + "ms"
    print (cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        print (line.decode('utf-8'))
    p.wait()
    p.stdout.close()
    return 0


def record_ios_with_config():
    output_dir, prefix = base_utils.get_work_dir_and_prefix(setting.ios_output_dir)
    trace_file = prefix + '.trace'
    sync_cmd = r'frida-ps -Ua'
    pid = get_pid(sync_cmd, setting.ios_app_bundle_id)
    ret = record(setting.ios_uuid, pid, setting.template, setting.run_time * 1000, trace_file)
    return trace_file, prefix, ret


def record_mac_with_config():
    output_dir, prefix = base_utils.get_work_dir_and_prefix(setting.mac_output_dir)
    trace_file = prefix + '.trace'
    sync_cmd = r'frida-ps'
    pid = get_pid(sync_cmd, setting.mac_app_bundle_id)
    ret = record(setting.mac_uuid, pid, setting.template, setting.run_time * 1000, trace_file)
    return trace_file, prefix, ret


if __name__ == "__main__":
    #record_mac_with_config()
    record_ios_with_config()

