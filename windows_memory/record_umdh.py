# coding=utf-8

import psutil


def enum_process():
    pidList = psutil.pids()
    for pid in pidList:
        pidDictionary = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'username', 'exe', 'create_time'])
        for keys in pidDictionary.keys():
            tempText = keys + ':' + str(pidDictionary[keys]) + '\n'
            print tempText


if __name__ == "__main__":
    enum_process()
