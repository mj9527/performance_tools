# coding=utf-8
import subprocess
import xml.etree.ElementTree as ET
import time


def export_content(trace_file, prefix):
    content_file = prefix + '_content.xml'
    cmd = 'xcrun xctrace export --input ' + trace_file \
          + ' --toc' \
          + ' --output ' + content_file
    print (cmd)
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return content_file


def parse_content(content_file):
    time.sleep(5)
    tree = ET.parse(content_file)
    root = tree.getroot()
    schema_list = []
    for item in root[0]:
        print (item.tag)
        if item.tag == "data":
            for tb in item:
                schema_name = tb.attrib.get('schema')
                if schema_name not in schema_list:
                    schema_list.append(schema_name)
    return schema_list


def export_schema_list(trace_file, prefix, schema_list):
    file_list = []
    for schema_name in schema_list:
        schema_file = export_schema(trace_file, schema_name, prefix)
        file_list.append(schema_file)
    return file_list


def export_schema(trace_file, schema_name, prefix):
    schema_file = prefix + '_' + schema_name + '.xml'
    cmd = 'xcrun xctrace export --input ' + trace_file \
          + ' --xpath \'/trace-toc/run[@number="1"]/data/table[@schema="' + schema_name + '"]\'' \
          + ' --output ' + schema_file
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print (cmd)
    stdout, stderr = child.communicate()
    # print(stdout)
    return schema_file


def get_schema_list(trace_file, prefix):
    content_file = export_content(trace_file, prefix)
    print (content_file)
    schema_list = parse_content(content_file)
    file_list = export_schema_list(trace_file, prefix, schema_list)
    return file_list


def get_time_file(file_list):
    for file_name in file_list:
        if file_name.find('time-profile') != -1:
            print ('start analyze file ', file_name)
            return file_name
    return ""

 # file_list = content_parser.get_schema_list(trace_file, prefix)
 #    time_file = content_parser.get_time_file(file_list)
 #    if time_file == "":
 #        return
 #    print (time_file)


# def analyze_content_config():
#     output_dir = c.output_dir
#     xml_name = output_dir + '2021-02-20_19_19_02_content.xml'
#     trace_file = output_dir + '2021-02-20_19_19_02_time_profile.trace'
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
#     schema_list = parse_content(xml_name)
#     export_schema_list(schema_list, trace_file, output_dir, current_time)

