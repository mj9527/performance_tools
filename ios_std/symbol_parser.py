# coding=utf-8
import os
import subprocess
import sys
sys.path.append("..")
import setting


class ModuleInfo:
    def __init__(self):
        self.start_address = 0x0
        self.end_address = 0x0
        self.name = ""
        self.arch = ""
        self.path = ""
        self.ls = []
        self.symbol_file = ""


class SymbolInfo:
    def __init__(self):
        self.address = 0x0
        self.module_name = ""
        self.func_name = ""


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


def get_symbol_path(module_path):
    module_name = os.path.basename(module_path)
    symbol_file = ''
    for k in setting.SYMBOL_DICT:
        if module_path.find(k) != -1:
            symbol_file = setting.SYMBOL_DICT[k]
            break
    if module_path.find('/private/') != -1:
        if module_path.find('Frameworks') != -1:
            symbol_file += module_name + ".framework.dSYM/Contents/Resources/DWARF/" + module_name
        else:
            symbol_file += module_name + ".app.dSYM/Contents/Resources/DWARF/" + module_name
    if module_path.find('/System/') != -1:
        symbol_file += module_path

    if module_path.find('/usr/lib') != -1:
        symbol_file += module_path
    return symbol_file


def symbol_address(module, address):
    symbol_file = get_symbol_path(module.path)
    module.symbol_file = symbol_file
    if symbol_file == module.path:
        return []
    cmd = "xcrun atos -arch arm64 -l " + module.start_address + \
          " -o '" + symbol_file \
          + "' " + address
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    func_name = []
    if stderr != '':
        print ('parse error', stderr)
        return func_name
    lines = stdout.splitlines()
    for line in lines:
        func_name.append(line)
    return func_name


def group_address_by_module(modules, address_list):
    for address in address_list:
        module = find_module_with_address(modules, address)
        if module is not None:
            if address not in module.ls:
                module.ls.append(address)


def symbol_module_address(modules):
    dict = {}
    for module in modules:
        if len(module.ls) == 0:
            continue
        str_address = address_list_to_str(module.ls)
        func_name_list = symbol_address(module, str_address)
        if len(func_name_list) == 0:
            #print ('fail to symbaol address')
            continue
        if len(func_name_list) != len(module.ls):
            print ('unmatch length ', module.symbol_file)
            continue
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


def symbol_with_file(file_name, address_list):
    modules = get_module_list(file_name)
    group_address_by_module(modules, address_list)
    address_to_modules = symbol_module_address(modules)
    return address_to_modules


if __name__ == "__main__":
    address_list = ['0x1acedbbca']
    symbol_with_file("", address_list)
