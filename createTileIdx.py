# -*- coding: utf-8 -*-
#   读取当前目录下info.txt文件中的图层信息，生成相应图层序号


import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd

#运行前注意填写行星和图层类型

planet = 'Mars'  #月球为Moon，火星为Mars
service = 'EQ'  #赤道为EQ，北极为NP，南极为SP


# info中包含多个图层时使用

info_path = 'info.txt'  # 指定文本文件的路径

# 读取文本文件内容
with open(info_path, 'r') as file:
    file_content = file.read()

# 以...为分界符分割内容
info_s = file_content.split('...')

info_error = []


def extract_info(string):
    lines = string.split('\n')  # 将字符串按行分割成列表
    title = lines[0]  # 第二行为title
    layer_id = None

    if service == "EQ":
        service_lower = 'eqc'
    else:
        service_lower = service.lower()

    for index, line in enumerate(lines):
        if line.startswith('Layer ID :'):
            layer_id_raw = line.split(':')[1].strip()  # 提取Layer ID后的内容，并去除首尾空格
            layer_id = planet + "_" + service_lower + "_" + layer_id_raw
    
    layerid_parts = layer_id.split('_')
    pic_name = "_".join(layerid_parts[2:])
    wmts_capabilities =  "{MoonImage}\\" + layer_id + "\\WMTSCapabilities.xml"
    folder_path = os.path.join(r'./', layer_id)

    
    return title, layer_id, pic_name


#生成0_TileType文件, 当前图层序号默认为1000000000
if planet == 'Moon':
    if service == 'EQ':
        tile_idx = 1000000000
    elif service == 'SP':
        tile_idx = 1000010100
    elif service == 'NP':
        tile_idx = 1000020100
elif planet == 'Mars':
    if service == 'EQ':
        tile_idx = 1300000000
    elif service == 'SP':
        tile_idx = 1300010000
    elif service == 'NP':
        tile_idx = 1300020000
elif planet == 'Earth':
    if service == 'EQ':
        tile_idx = 2000000000
    elif service == 'SP':
        tile_idx = 2000010000
    elif service == 'NP':
        tile_idx = 2000020000


# 创建一个空的DataFrame对象
df = pd.DataFrame(columns=['Planet', 'Service', 'layer_id', 'tile_idx'])

for info in info_s:
    
    print("------------------------------")
    #time.sleep(0.4)  #
     #开始读取info并生成文件

    title, layer_id, pic_name = extract_info(info)

    wmts_url = 'https://trek.nasa.gov/tiles/' + planet + '/'+ service + '/' + pic_name + '/1.0.0/WMTSCapabilities.xml'

    #检查wmts文件是否正确
    wmts_respons = requests.get(wmts_url)
    if wmts_respons.status_code != 200:
        print(f"图层{layer_id}wmts文件获取失败. HTTP status code:", wmts_respons.status_code)
        info_error.append(info)
        #print(info)
        continue
    tile_idx = tile_idx + 1
    data = [planet, service, layer_id, tile_idx]
    # 将数据添加到DataFrame
    df = df.append(pd.Series(data, index=df.columns), ignore_index=True)

# 保存DataFrame到Excel文件
df.to_excel('tile_idx.xlsx', index=False)
print("tile_idx数据已成功添加到文件！")

# 打开txt文件以写入模式
with open('info_error.txt', 'w') as file:
    # 将列表中的元素逐行写入txt文件
    for element in info_error:
        file.write(element + '...')
print('错误图层信息已写入info_error.txt')
print('全部内容生成完毕')