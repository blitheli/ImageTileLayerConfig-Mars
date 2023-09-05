# -*- coding: utf-8 -*-
#   读取当前目录下所有文件夹，生成index.html文件
#       > 读取模板文件index.html
#       > 读取config.json文件，获取 layer_id, wmts_TypeId、BBOX, MinimumLevel, MaximumLevel等属性
#       > 替换模板文件index.html里的路径
#       > 保存index.html文件
#   本函数在所有图层文件夹已存在, 如果部署在不同的服务器上，则ip_port需要修改！！
#   blitheli 20210904

import os
import json


# 根据不同的服务器，修改ip_port
# 瓦片服务器部署的地址，用于生成index.html文件
ip_port = "http://139.224.107.180:9080"

# 读取config.json文件, 获取 layer_id, wmts_TypeId、BBOX, MinimumLevel, MaximumLevel
def extract_config(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)

    # 获取wmts_TypeId、BBOX和WMTS_Capabilities字段的值
    layer_id = config_data["LayerID"]
    wmts_TypeId = config_data["WMTS_TypeId"]
    bbox = config_data["BBOX"]
    minLevel = config_data["MinimumLevel"]
    maxLevel = config_data["MaximumLevel"]

    return layer_id, wmts_TypeId, bbox, minLevel, maxLevel

# 生成index文件
def write_indexHtml():

    bbox_west = str(bbox[0])
    bbox_east = str(bbox[2])
    bbox_south = str(bbox[1])
    bbox_north = str(bbox[3])

    bbox_lon_0 = (bbox[0] + bbox[2])/2
    bbox_lat_0 = (bbox[1] + bbox[3])/2

    bbox_lon = str(round(bbox_lon_0, 2))
    bbox_lat = str(round(bbox_lat_0, 2))

    # 加载index.html模板文件
    with open('index.html', 'r', encoding='utf-8') as file:
        index_0 = file.read()

    replaced_xml = index_0.replace("{ip:port}", ip_port)
    replaced_xml = replaced_xml.replace("{tile_idx}", wmts_TypeId)
    replaced_xml = replaced_xml.replace("{layer_id}", layer_id)
    replaced_xml = replaced_xml.replace("{bbox_west}", bbox_west)
    replaced_xml = replaced_xml.replace("{bbox_east}", bbox_east)
    replaced_xml = replaced_xml.replace("{bbox_south}", bbox_south)
    replaced_xml = replaced_xml.replace("{bbox_north}", bbox_north)
    replaced_xml = replaced_xml.replace("{bbox_lon}", bbox_lon)
    replaced_xml = replaced_xml.replace("{bbox_lat}", bbox_lat)
    replaced_xml = replaced_xml.replace("{minZoom}", str(minLevel+1))
    replaced_xml = replaced_xml.replace("{maxZoom}", str(maxLevel+1))

    index_path = folder_path + '/' + 'index.html'
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(replaced_xml)

# 获取当前目录
current_directory = os.getcwd()

# 获取当前目录下所有的子文件夹
subdirectories = [name for name in os.listdir(
    current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# 筛选出以 "Moon_XX" 开头的文件夹名称
folders = [name for name in subdirectories if name.startswith("Mars_eqc")]


# 遍历当前目录下的子文件夹
for folder in folders:
    folder_path = os.path.join(current_directory, folder)

    # 从config.json文件中读取wmts_TypeId、bbox, MinimumLevel, MaximumLevel
    layer_id, wmts_TypeId, bbox, minLevel, maxLevel = extract_config(
        folder_path + '/config.json')

    write_indexHtml()

print('全部图层文件夹里的index.html生成完毕！！')
