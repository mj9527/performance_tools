# coding=utf-8
import subprocess
import datetime
import xml.etree.ElementTree as ET


def export_content(trace_file, prefix):
    content_file = prefix + '_content.xml'
    cmd = 'xcrun xctrace export --input ' + trace_file \
          + ' --toc' \
          + ' --output ' + content_file
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print (cmd)
    return content_file


def parse_content(content_file):
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
        schema_file = prefix + '_' + schema_name + '.xml'
        export_schema(trace_file, schema_name, schema_file)
        file_list.append(schema_file)
    return file_list


def export_schema(trace_file, schema_name, schema_file):
    cmd = 'xcrun xctrace export --input ' + trace_file \
          + ' --xpath \'/trace-toc/run[@number="1"]/data/table[@schema="' + schema_name + '"]\'' \
          + ' --output ' + schema_file
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print (cmd)
    stdout, stderr = child.communicate()
    # print(stdout)




# def analyze_content_config():
#     output_dir = c.output_dir
#     xml_name = output_dir + '2021-02-20_19_19_02_content.xml'
#     trace_file = output_dir + '2021-02-20_19_19_02_time_profile.trace'
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
#     schema_list = parse_content(xml_name)
#     export_schema_list(schema_list, trace_file, output_dir, current_time)

