# coding=utf-8
import subprocess
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


def record_apple_config(prefix, os_type, uuid, bundle_id, template, interval):
    if os_type == 'ios':
        print ('record ios')
        sync_cmd = r'frida-ps -Ua'
        inject_cmd = r'frida -U '
    else:
        sync_cmd = r'frida-ps'
        inject_cmd = r'frida '
    if uuid == '':
        device_dict = enum_device()
        if os_type in device_dict:
            uuid = device_dict[os_type]
            print 'auto get uuid', uuid
    trace_file = prefix + '.trace'
    pid = get_pid(sync_cmd, bundle_id)
    ret = record(uuid, pid, template, interval, trace_file)
    module_file = prefix + '.log'
    record_modules.export_module_to_file(inject_cmd, pid, module_file)
    return trace_file, ret


def enum_device():
    cmd = "xcrun xctrace list devices"
    print (cmd)
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stdout = child.communicate()
    lines = stdout.splitlines()
    device_dict = {}
    for line in lines:
        if line.find('Devices') != -1:
            continue
        elif line.find('Simulators') != -1:
            break
        elif line == '':
            continue
        else:
            pos = line.rfind('(')
            sz = len(line)
            if pos != -1:
                device_name = line[:pos-1].strip()
                uuid = line[pos+1:sz-1].strip()
                os_type = ''
                if device_name.find('(') != -1:
                    os_type = 'ios'
                else:
                    os_type = 'mac'
                device_dict[os_type] = uuid
                print os_type, device_name, uuid
    return device_dict