from urllib import unquote
import json
import subprocess


def read_file_by_line(file_name, symbol_dir, arch):
    f = open(file_name)
    lines = []
    line = f.readline()
    while line:
        words = line.split(' ')
        #print(words[0], words[1], words[2], words[3].replace('\n', ''))
        cmd = 'atos -o ' + symbol_dir + words[1] + '.framework.dSYM/Contents/Resources/DWARF/' + words[1] \
              + ' -arch ' + arch + ' -l ' + words[2] + ' ' + words[3].replace('\n', '')
        #print cmd
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print stdout.replace('\n', '')
        line = f.readline()
    return lines


def write_json_file(json_data, file_name):
    with open(file_name, "w") as f:
        json_str = json.dumps(json_data)
        f.write(json_str)
        f.close()


if __name__ == "__main__":
    FILE_NAME = '/Users/zhengjunming/Downloads/xcast_armv7_2.log'
    SYMBOL_DIR = '/Users/zhengjunming/Downloads/1.7.7/'
    ARCH_NAME = 'armv7'
    #ARCH_NAME = 'arm64'
    read_file_by_line(FILE_NAME, SYMBOL_DIR, ARCH_NAME)
