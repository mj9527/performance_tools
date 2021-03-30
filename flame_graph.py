import json
import os
from drawtools.flamegraph_formatter import flame_formatting
from drawtools.sunburst_formatter import sunburst_formatting


def get_flamegrap_from_json(json_file, html_file):
    flame_json = flame_formatting(json_file)
    s = json.dumps(flame_json, indent=2)
    a = s.replace('\r', '').replace('\n', '').replace(' ', '').replace('"', r'\"')
    with open(os.getcwd() + '/../drawtools/flamegraph_template.html', 'r') as fr:
        sr = fr.read()
        out = sr.replace('__TEMP__', a)

        with open(html_file, 'w') as fw:
            fw.write(out)
        print("flamegrap html:" + html_file)


def get_sunburstgraph_from_json(json_file, html_file):
    sunburst_json = sunburst_formatting(json_file)
    s = json.dumps(sunburst_json, indent=2)
    # print(s)
    a = s.replace('\r', '').replace('\n', '').replace("\\", "\\\\").replace(' ', '').replace('"', r'\"')
    with open(os.getcwd() + '/../drawtools/sunburst_template.html', 'r') as fr:
        sr = fr.read()
        out = sr.replace('__TEMP__', a)

        with open(html_file, 'w') as fw:
            fw.write(out)
        print("sunburstgraph html:" + html_file)


if __name__ == '__main__':
    prefix = "/Users/mjzheng/Downloads/ios_data/2021-03-30_19_27_05/2021-03-30_19_27_05"
    json_file = prefix + ".json"
    flame_file = prefix + "_flame.html"
    sunburst_file = prefix + "_sunburst.html"
    get_sunburstgraph_from_json(json_file, sunburst_file)
    get_flamegrap_from_json(json_file, flame_file)

