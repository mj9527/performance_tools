# coding=utf-8
import datetime
import os
import setting


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False


def get_work_dir_and_prefix(output_dir):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    output_dir = output_dir + current_time + '/'
    mkdir(output_dir)
    prefix = output_dir + current_time
    return output_dir, prefix


def get_work_dir_and_prefix_with_config():
    origin_dir = ''
    if setting.os_type == 'ios_std':
        origin_dir = setting.ios_output_dir
    elif setting.os_type == 'osx':
        origin_dir = setting.mac_output_dir
    elif setting.os_type == 'windows':
        origin_dir = setting.windows_output_dir
    else:
        origin_dir = ''
    output_dir, prefix = get_work_dir_and_prefix(origin_dir)
    return output_dir, prefix
