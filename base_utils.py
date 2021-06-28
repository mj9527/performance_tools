# coding=utf-8
import datetime
import os
import setting


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
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
    if setting.OS_TYPE == 'ios':
        origin_dir = setting.IOS_OUTPUT_DIR
    elif setting.OS_TYPE == 'osx':
        origin_dir = setting.MAC_OUTPUT_DIR
    elif setting.OS_TYPE == 'windows':
        origin_dir = setting.WINDOWS_OUTPUT_DIR
    else:
        origin_dir = ''
    output_dir, prefix = get_work_dir_and_prefix(origin_dir)
    return output_dir, prefix
