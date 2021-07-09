# -*- coding: utf-8 -*-
import os

from simpleperf import callgraph_2_json

CPU_SRCH_MAP = {"arm": "armeabi-v7a", "arm64": "arm64-v8a", "x86": "x86", "x86_64": "x86_64"}


def copy_symbols_and_simpleperf_to_device(device_id, ndk_path, package_name, symbol_path=None):
    app_path, cpu_arch = get_app_path(package_name, device_id)
    if app_path is None:
        print("can not find " + package_name)
        return False

    if (symbol_path is not None) and (cpu_arch is not None):
        os.system("adb -s {0} push {1}/{2}/. /data/local/tmp/{3}/symbols/{4}".
                  format(device_id, symbol_path, CPU_SRCH_MAP[cpu_arch], package_name, cpu_arch))
    else:
        symbol_path = None
        cpu_arch = "arm"

    simpleperf_path = os.path.join(ndk_path, "simpleperf/bin/android")
    os.system("adb -s {} push {} /data/local/tmp/{}/simpleperf".format(device_id, simpleperf_path, package_name))

    with open("cmd.txt", "w") as cmd_file:
        cmd_file.writelines("run-as {}\n".format(package_name))
        cmd_file.writelines("cp /data/local/tmp/{}/simpleperf/{}/simpleperf .\n".format(package_name, cpu_arch))
        cmd_file.writelines("chmod 0775 ./simpleperf\n")
        if (symbol_path is not None):
            cmd_file.writelines("mkdir -p {}/lib/{}/\n".format(app_path, cpu_arch))
            cmd_file.writelines("cp /data/local/tmp/{0}/symbols/{1}/* ./{2}/lib/{1}/\n".
                                format(package_name, cpu_arch, app_path))

    os.system("adb -s {} shell < cmd.txt".format(device_id))
    return True


def reocord_perfdata(package_name, outfile, device_id, cap_time_sec):
    pid = get_pid(package_name, device_id)

    with open("cmd.txt", "w") as cmd_file:
        cmd_file.writelines("run-as {}\n".format(package_name))
        cmd_file.writelines("./simpleperf record -g -p {} --duration {} --symfs .\n".format(pid, cap_time_sec))
        cmd_file.writelines("./simpleperf report --sort tid,comm --symfs . > analyse_file\n")
        cmd_file.writelines("./simpleperf report --sort tid,symbol --symfs . >> analyse_file\n")
        cmd_file.writelines("./simpleperf report --children --symfs . >> analyse_file\n")
        cmd_file.writelines("./simpleperf report -g --symfs . >> analyse_file\n")

    os.system("adb -s {} shell setprop security.perf_harden 0".format(device_id))
    os.system("adb -s {} shell < cmd.txt".format(device_id))
    os.system('adb -s {} shell "run-as {} cat ./analyse_file" > temp_file'.format(device_id, package_name))

    callgraph_2_json.graph_2_json("temp_file", outfile)


def get_app_path(package_name, device_id):
    result = os.popen("adb -s {} shell pm path {}".format(device_id, package_name))
    res = result.read()
    for line in res.splitlines():
        print(line)
        begin = line.find("/")
        end = line.rfind("/")
        path = line[begin + 1:end]

        result = os.popen("adb -s {} shell ls {}/lib".format(device_id, path))
        res = result.read()
        cpu_arch = None
        if len(res.splitlines()) > 0:
            cpu_arch = res.splitlines()[0]

        print("package={}, path={}, cpu_arch={}".format(package_name, path, cpu_arch))
        return path, cpu_arch

    print("can not find package {} .".format(package_name))
    return None, None


def get_pid(package_name, device_id):
    cmd = 'adb -s {} shell "top -n 1 -o PID,%CPU,CMDLINE -s 2 | grep {}"'.format(device_id, package_name)
    res = os.popen(cmd).read()
    for line in res.splitlines():
        if line.find("grep") != -1:
            continue

        cols = line.split()
        if cols[len(cols) - 1] == package_name:
            print(line)
            return cols[0]
    print("can not find {} process.".format(package_name))
    return None
