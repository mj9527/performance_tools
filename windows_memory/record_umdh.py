# coding=utf-8

import psutil


def get_main_process():
    pid_list = psutil.pids()
    for pid in pid_list:
        pid_attr_dict = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'cmdline'])
        if pid_attr_dict['name'] != 'wemeetapp.exe':
            continue
        cmdline = pid_attr_dict['cmdline']
        for param in cmdline:
            if param.find('--module') != -1 and param.find('wemeet.dll') != -1:
                return int(pid_attr_dict['pid'])
    return -1


if __name__ == "__main__":
    pid = get_main_process()
    print pid
