# coding=utf-8

import psutil
import subprocess
import time


def get_main_process():
    pid_list = psutil.pids()
    for pid in pid_list:
        pid_attr_dict = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'exe', 'cmdline'])
        if pid_attr_dict['name'] != 'wemeetapp.exe':
            continue
        cmdline = pid_attr_dict['cmdline']
        for param in cmdline:
            if param.find('--module') != -1 and param.find('wemeet.dll') != -1:
                print pid_attr_dict['exe']
                return int(pid_attr_dict['pid']), pid_attr_dict['exe']
    return -1


def execute_cmd(cmd):
    print (cmd)
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = child.communicate()
    print stdout, stderr


def add_double_quote(origin_str):
    return "\"" + origin_str + "\""


def inject_process(exe_path):
    cmd = 'gflags.exe /i \"' + exe_path + '\" +ust'
    execute_cmd(cmd)


def record_memory(pid, file_name):
    cmd = 'umdh -p:' + str(pid) + ' -f:' + add_double_quote(file_name)
    execute_cmd(cmd)


def compare_snapshot(previous_file, behind_file, diff_file):
    cmd = 'umdh -d ' + add_double_quote(previous_file) + ' ' + \
          add_double_quote(behind_file) + ' -f:' + add_double_quote(diff_file)
    execute_cmd(cmd)


def record_interval(prefix, interval):
    pid, path = get_main_process()
    inject_process(path)

    previous_file = prefix+'_previous.txt'
    record_memory(pid, previous_file)
    time.sleep(interval)
    behind_file = prefix+'_behind.txt'
    record_memory(pid, behind_file)
    diff_file = prefix + '_diff.txt'
    compare_snapshot(previous_file, behind_file, diff_file)
    return diff_file


if __name__ == "__main__":
    print 'good'
