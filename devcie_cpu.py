from urllib import unquote
import json


def read_file_by_line(file_name):
    f = open(file_name)
    lines = []
    line = f.readline()
    while line:
        words = line.split(',')
        device = unquote(words[0])
        cpu = int(float(words[1]))
        if cpu >= 40:
            dt = {'model': str(device), 'os_version': '*', 'app_cpu_threshold': cpu, 'thread_cpu_threshold': 40}
            lines.append(dt)
        line = f.readline()
    write_json_file(lines, '/Users/mjzheng/Downloads/scene_data/device_list.json')
    f.close()
    return lines


def write_json_file(json_data, file_name):
    with open(file_name, "w") as f:
        json_str = json.dumps(json_data)
        f.write(json_str)
        f.close()


if __name__ == "__main__":
    FILE_NAME = '/Users/mjzheng/Downloads/scene_data/device_cpu_scene.txt'
    read_file_by_line(FILE_NAME)
