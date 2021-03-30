# coding=utf-8
import record_apple
import content_parser


def export_content_with_config(trace_file, prefix):
    content_file = export_content(trace_file, prefix)
    schema_list = parse_content(content_file)

    file_list = export_schema_list(trace_file, prefix, schema_list)
    for file_name in file_list:
        if file_name.find('time-profile') != -1:
            print ('start analyze file ', file_name)
            json_name = prefix + '.json'
            txt_file = prefix + '.txt'
            analyse_group(file_name , json_name, txt_file)
            break
    return schema_list


def run_instrument_with_config():
    trace_file, prefix, ret = record_apple.record_ios_with_config()
    if ret != 0:
        return

    content_file = content_parser.export_content(trace_file, prefix)
    schema_list = content_parser.parse_content(content_file)
    file_list = content_parser.export_schema_list(trace_file, prefix, schema_list)

    for file_name in file_list:
        if file_name.find('time-profile') != -1:
            print ('start analyze file ', file_name)
            json_name = prefix + '.json'
            txt_file = prefix + '.txt'
            analyse_group(file_name , json_name, txt_file)
            break
    return schema_list


if __name__ == "__main__":
    run_instrument_with_config()