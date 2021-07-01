# coding=utf-8
import subprocess
import sys
sys.path.append("..")
import setting
import record_modules


def get_pid(sync_cmd, bundle_id):
    print ('start get pid')
    print (sync_cmd)
    child = subprocess.Popen(sync_cmd, shell=True, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()
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
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()
    lines = stdout.splitlines()
    for line in lines:
        print (line.decode('utf-8'))
    return 0


def record_apple_config(prefix):
    if setting.OS_TYPE == 'ios':
        print ('record ios')
        sync_cmd = r'frida-ps -Ua'
        inject_cmd = r'frida -U '
        uuid = setting.IOS_UUID
        bundle_id = setting.IOS_BUNDLE_ID
    else:
        sync_cmd = r'frida-ps'
        inject_cmd = r'frida '
        uuid = setting.MAC_UUID
        bundle_id = setting.MAC_BUNDLE_ID
    template = setting.INSTRUMENT_TEMPLATE
    interval = setting.RUN_TIME * 1000

    trace_file = prefix + '.trace'
    pid = get_pid(sync_cmd, bundle_id)
    ret = record(uuid, pid, template, interval, trace_file)
    module_file = prefix + '.log'
    record_modules.export_module_to_file(inject_cmd, pid, module_file)
    return trace_file, ret
