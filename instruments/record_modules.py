# coding=utf-8
import subprocess
import json


def string_to_hex(data):
    a = data.encode('hex')
    b = a.decode('hex')
    return b


def get_modules(inject_cmd, pid):
    cmd = inject_cmd + str(pid) + ' -l instruments/enumerate_modules.js'
    print (cmd)
    child = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    child.stdin.write('quit')
    stdout, stderr = child.communicate()
    print stderr
    print stdout
    lines = stdout.splitlines()
    module_list = []
    for line in lines:
        if 'name' not in str(line):
            #print ('filter', line)
            continue
        m = json.loads(line)
        base = m["base"]
        base_int = int(base, 16)
        sz = m["size"]
        end = hex(base_int + sz)
        #print (base, sz, end)
        module = base + ' - ' + end + ' ' + m["name"] + ' arm64 <2f8209bfa2153311b9c3696e683b2646> ' + m["path"]
        module_list.append(module)
        #print (module)
    return module_list


def write_module(save_path, lines):
    print ('start write file')
    with open(save_path, "w") as f:
        for line in lines:
            f.write(str(line))
            f.write('\n')
        f.close()


def export_module_to_file(inject_cmd, pid, save_path):
    lines = get_modules(inject_cmd, pid)
    write_module(save_path, lines)
    return


if __name__ == "__main__":
    export_module_to_file(2971, '34.log')
