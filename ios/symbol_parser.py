# coding=utf-8
import subprocess


class ModuleInfo:
    def __init__(self):
        start_address = 0x0
        end_address = 0x0
        name = ""
        arch = ""
        path = ""
        ls = []


class SymbolInfo:
    def __init__(self):
        address = 0x0
        module_name = ""
        func_name = ""


def string_to_hex(data):
    a = data.encode('hex')
    b = a.decode('hex')
    return b


def get_module_list(file_name):
    modules = []
    with open(file_name, 'r') as f:
        for line in f:
            words = line.split()
            module = ModuleInfo()
            module.start_address = string_to_hex(words[0])
            module.end_address = string_to_hex(words[2])
            module.name = words[3]
            module.arch = words[4]
            module.path = words[6]
            module.ls = []
            modules.append(module)
    return modules


def print_module_list(modules):
    for module in modules:
        print_module_info(module)


def print_module_info(module_info):
    print (module_info.start_address, module_info.end_address, module_info.name, module_info.path)


def find_module_with_address(modules, address):
    for module in modules:
        if module.start_address <= address <= module.end_address:
            return module
    return None


def symbol_address(module, address):
    symbol_file = c.output_dir + '2021-03-01_20_45_42/' + 'WeMeetApp.app.dSYM/Contents/Resources/DWARF/WeMeetApp'
    exe_path = ''
    if module.path.find('/System/Library') != -1:
        exe_path = "/Users/mjzheng/Library/Developer/Xcode/iOS DeviceSupport/14.1 (18A8395)/Symbols" \
                   + module.path
    elif module.path.find('xcast.framework') != -1:
        exe_path = c.output_dir + '2021-03-01_20_45_42/' + 'xcast.framework.dSYM/Contents/Resources/DWARF/xcast'
    else:
        exe_path = symbol_file

    cmd = "xcrun atos -arch arm64 -l " + module.start_address + \
          " -o '" + exe_path \
          + "' " + address
    #print (cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    func_name = []
    if stderr != '':
        #print ("symbole error", stderr)
        print (module.path)
        return func_name
    lines = stdout.splitlines()
    for line in lines:
        func_name.append(line)
    return func_name


def group_address_by_module(modules, address_list):
    for address in address_list:
        module = find_module_with_address(modules, address)
        if module != None:
            if address not in module.ls:
                module.ls.append(address)


def symbol_module_address(modules):
    dict = {}
    for module in modules:
        if len(module.ls) == 0:
            continue
        str_address = address_list_to_str(module.ls)
        func_name_list = symbol_address(module, str_address)
        if len(func_name_list) != len(module.ls):
            print ('unmatch length ', module.name)
        for index, address in enumerate(module.ls):
            info = SymbolInfo()
            info.address = address
            info.module_name = module.name
            info.func_name = address
            if index < len(func_name_list):
                info.func_name = func_name_list[index]
            dict[address] = info
    return dict


def address_list_to_str(address_list):
    str_address = ""
    for address in address_list:
        str_address += address + " "
    return str_address


def symbol_with_file(address_list):
    file_name = c.output_dir + '2021-03-01_20_45_42/' + '20210301204538531_ori.crash'
    modules = get_module_list(file_name)
    group_address_by_module(modules, address_list)
    dict = symbol_module_address(modules)
    return dict


if __name__ == "__main__":
    address_list = ['0x1acedbbca']
    symbol_with_file(address_list)