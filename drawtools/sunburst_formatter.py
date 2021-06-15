# -*- coding: UTF-8 -*-
import json


'''
sunburst_formatter.py 的作用是根据上传至服务器的 JSON 文件生成 sunburstDataset.js 文件
'''


# 旭日图第一层的内容
firstLevel = [
    "main",
    "音频前处理",
    "音频编解码",
    "音频采集播放",
    "jitter",
    "网络",
    "视频编解码",
    "其他",
    "视频前处理",
    "渲染"
]


# 每一个 part 包含的子 part
partToItsChildList = {
    "main": [],
    "音频前处理": [
        "3A处理",
        "agc",
        "啸叫处理",
        "同地多设备检测"
    ],
    "音频编解码": [
        "opus编码"
    ],
    "音频采集播放": [
        "音频播放（含mix）",
        "音频采集"
    ],
    "jitter": [
        "jitter处理",
        "音频后处理"
    ],
    "网络": [
        "fec",
        "rtp"
    ],
    "视频编解码": [
        "视频编码",
        "视频解码"
    ],
    "其他": [
        "xc中的锁",
        "xc中uv的io处理",
        "xc的cycle_once",
        "音频无参考评分LSQA"
    ],
    "视频前处理": [
        "美颜"
    ],
    "渲染": [
        "视频渲染"
    ]
}


# 每一个函数所属的 part
funcToPart = {
    "trae_aec_near_run": "3A处理",
    "trae_agc_run": "agc",
    "trae_howling_preprun": "啸叫处理",
    "trae_slmdd_run_nodataout": "同地多设备检测",

    "opus_encoder_encode": "opus编码",

    "on_audio_render_frame": "音频播放（含mix）",
    "on_audio_capture_frame": "音频采集",

    "audio_jitter_receive": "jitter处理",
    "on_push_audio_play_data": "音频后处理",

    "async_input_audio_fec_dec": "fec",
    "rtp_packet_delive": "rtp",

    "process_video_frame": "视频编码",
    "video_encoder_loop": "视频编码",
    "xc_codec_video_decode": "视频解码",
    "video_stream_decoder_loop": "视频解码",

    "xc_mutex_lock_wait": "xc中的锁",
    "uv__io_poll": "xc中uv的io处理",
    "cycle_once": "xc的cycle_once",
    "XNNAudioListener::DoAudioRenderProcess": "音频无参考评分LSQA",
    "TRTC::YTBeautyWrapper::process": "美颜",
    "VideoRenderImpl::OnTimer": "视频渲染"
}


# 在统计函数的 weight 时，如果存在递归调用的情况，则只需要统计该函数的第一次调用，而忽略后续深层次的调用。
# 故 dfs 的过程中需要维护一个存放函数名的 ignore_list
def sunburst_dfs(func_obj, ignore_list, weight_of):
    find_key = None
    for key in funcToPart:
        if func_obj["funcname"] in key or key in func_obj["funcname"]  \
            and func_obj['funcname'] not in ignore_list:
            find_key = key
            break

    if find_key:
        weight_of[funcToPart[find_key]] += func_obj["weight"]
        ignore_list.append(func_obj["funcname"])
        if "children" in func_obj:
            for child in func_obj["children"]:
                sunburst_dfs(child, ignore_list, weight_of)
        ignore_list.pop(-1)
    else:
        if "children" in func_obj:
            for child in func_obj["children"]:
                sunburst_dfs(child, ignore_list, weight_of)


def sunburst_generate_dataset(part_obj, weight_of):
    if part_obj["name"] in weight_of:
        part_obj["weight"] = weight_of[part_obj["name"]]
    if part_obj["name"] in partToItsChildList:
        part_obj["children"] = []
        for child_part_name in partToItsChildList[part_obj["name"]]:
            part_obj["children"].append({"name": child_part_name})
            sunburst_generate_dataset(part_obj["children"][-1], weight_of)


# 计算每一个 part 的 weight
def sunburst_cal_weight(part):
    if "weight" in part:
        return
    else:
        part["weight"] = 0
        for child in part["children"]:
            sunburst_cal_weight(child)
            part["weight"] += child["weight"]


# 计算每一个 part 所占的百分比
def sunburst_cal_percent(list_input, weight_sum):
    for list_item in list_input:
        if weight_sum == 0.0:
            list_item["value"] = 0.0
        else:
            list_item["value"] = 1.0 * list_item["weight"] / weight_sum

        if "children" in list_item:
            sunburst_cal_percent(list_item["children"], weight_sum)


def sunburst_formatting(input_file_path):
    data_dict = {}

    # 需要统计的所有叶子 part 的 weight
    weight_of = {
        "main": 0,
        "3A处理": 0,
        "agc": 0,
        "啸叫处理": 0,
        "同地多设备检测": 0,
        "opus编码": 0,
        "音频播放（含mix）": 0,
        "音频采集": 0,
        "jitter处理": 0,
        "音频后处理": 0,
        "fec": 0,
        "rtp": 0,
        "视频编码": 0,
        "视频解码": 0,
        "xc中的锁": 0,
        "xc中uv的io处理": 0,
        "xc的cycle_once": 0,
        "音频无参考评分LSQA": 0,
        "美颜": 0,
        "视频渲染": 0,
    }
    sunburst_dataset = []
    with open(input_file_path, 'r') as input_file:
        data_dict = json.load(input_file)

    # main 线程的单独处理
    for thread in data_dict["threads"]:
        root_func_name = thread["func"][0]["funcname"]
        if "Main" in root_func_name or "main" in root_func_name:
            weight_of["main"] = thread["func"][0]["weight"]
            break

    # 统计叶子 part 的 weight，即统计 weightOf 的数据
    for thread in data_dict["threads"]:
        for func_obj in thread["func"]:
            sunburst_dfs(func_obj, [], weight_of)

    # 根据已经统计好的 weightOf 来构建 sunburstDataset
    for part_name_of_first_level in firstLevel:
        sunburst_dataset.append({"name": part_name_of_first_level})
        sunburst_generate_dataset(sunburst_dataset[-1], weight_of)

    # 计算所有 part 的 weightPercentage
    weight_sum = 0
    for i in range(len(sunburst_dataset)):
        sunburst_cal_weight(sunburst_dataset[i])
        weight_sum += sunburst_dataset[i]["weight"]
    sunburst_cal_percent(sunburst_dataset, weight_sum)

    # with open(targetDir + "/sunburstDataset.js", 'w') as sunburstDatasetJS:
    #     sunburstDatasetJS.write("var sunburstDataset = " + json.dumps(sunburstDataset, indent=2))
    return sunburst_dataset
