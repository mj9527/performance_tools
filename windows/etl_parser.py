import csv
import json
import sys
import os

module_map = {
    'screen_capture' : 'screen_capture',
    'audio_preprocess' : 'audio_preprocess',
    'xc_codec_video_encode' : 'video_encode',
    'xc_codec_video_decode' : 'video_decode',
    'WinMain' : 'main_thread',
    'OnCameraPreprocess' : 'camera_preprocess',
    'rtp_packet_delive' : 'packet_delive',
    'uv_process_reqs' : 'packet_receive',
    'log_thread_proc' : 'log_thread',
    'do_report' : 'do_report',
    'ksproxy' : 'video_capture',
    'wasapi_render_proc' : "audio_render"
}


def calc_cpu_usage(func_arr, stack_trace_str, module_map):
    if not stack_trace_str:
        print('stack_trace is none')
        return False
    
    module_keys = module_map.keys()

    cur_func_arr = func_arr
    stack_trace_arr = stack_trace_str.split('/')
    for i, func_name in enumerate(stack_trace_arr):
        find_func = False
        for func_obj in cur_func_arr:
            if func_obj['funcname'] == func_name:
                find_func = True
                break
        if not find_func:
            func_obj = {'module' : '', 'funcname' : func_name, 'weight' : 1, 'selfWeight' : 0, 'children' : []}
            module_arr = func_name.split('!')
            if len(module_arr) > 1:
                func_obj['module'] = module_arr[0]
            cur_func_arr.append(func_obj)
        else:
            weight = func_obj['weight'] + 1
            func_obj['weight'] = weight
        
        if 0 == i and 0 == len(func_obj['module']):
            for key in module_keys:
                if key in stack_trace_str:
                    func_obj['module'] = module_map[key]
                    break
                
        
        if i < len(stack_trace_arr) - 1:
            cur_func_arr = func_obj['children']
        else:
            self_weight = func_obj['selfWeight'] + 1
            func_obj['selfWeight'] = self_weight


def save_json_file(perf_tree, path):
    try:
        with open(path, 'w') as fp:
            json.dump(perf_tree, fp)
    except IOError:
        print("write json file eroor")


def csv_to_json(csv_file, json_file):
    if not os.path.exists(csv_file):
        print("csv file not exists")
        return False

    wemeet_proc_name = 'wemeetapp.exe'
    perf_tree = {}

    try:
        f = csv.reader(open(csv_file, 'r'))
    except IOError:
        print("read csv error")
        return False
    
    for line in f:
        if wemeet_proc_name in line[0]:
            #print(line)
            thread_id = line[1]
            threads = perf_tree.get('threads')
            if not threads:
                threads = []
                thread_info = {'threadID' : thread_id}
                threads.append(thread_info)
                perf_tree['threads'] = threads
            else:
                find_thread = False
                for thread_info in threads:
                    if thread_id == thread_info['threadID']:
                        find_thread = True
                if not find_thread:
                    thread_info = {'threadID' : thread_id}
                    threads.append(thread_info)
        
            func_arr = thread_info.get('func')
            if not func_arr:
                func_arr = []
                thread_info['func'] = func_arr
        
            calc_cpu_usage(func_arr, line[2], module_map)

    save_json_file(perf_tree, json_file)
    return True


def main():
    param_num = len(sys.argv)
    if 3 != param_num:
        print("parameter error")
        sys.exit(0)
    csv_file = sys.argv[1]
    json_file = sys.argv[2]
    
    csv_to_json(csv_file, json_file)


if __name__ == '__main__':
    main()    
        