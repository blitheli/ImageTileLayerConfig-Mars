# -*- coding: utf-8 -*-
#   读取当前目录下info.txt文件中的图层信息，生成相应图层文件夹及相关文件
#   运行前注意填写星球及图层类型
#   当前仅支持相同星球和图层类型的info信息，支持多个信息同时读取并生成
#   2023-07-13  苏秀中
#   2023-07-14  liyunfei，更新百度翻译api id
#   20230902    blitheli,增加代理接口，sxz修正abstract为空的BUG

import os
import json
import requests
import hashlib
import re
import random
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

proxies = {
  'http': 'http://127.0.0.1:10809',
  'https': 'http://127.0.0.1:10809',
}


#运行前注意填写行星和图层类型

planet = 'Mars'  #月球为Moon，火星为Mars
service = 'EQ'  #赤道为EQ，北极为NP，南极为SP

#生成0_TileType文件, 当前图层序号默认为1000000000
# 这里根据实际情况手动设置初始的编号，后续自动+1
if planet == 'Moon':
    if service == 'EQ':
        tile_idx = 1000000000
    elif service == 'SP':
        tile_idx = 1000010100
    elif service == 'NP':
        tile_idx = 1000020100
elif planet == 'Mars':
    if service == 'EQ':
        tile_idx = 1300000020
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

# info中包含多个图层时使用

info_path = 'info_mars_eqc.txt'  # 指定文本文件的路径

# 读取文本文件内容
with open(info_path, 'r', encoding = "utf-8") as file:
    file_content = file.read()

# 以...为分界符分割内容
info_s = file_content.split('...')

info_error = []


#定义翻译函数
def translate_text(text):
    if not text:
        return ''  # 如果文本为空，返回空字符串

    app_id = '20230714001744028'
    app_key = 'ZQQZHfKusrB4vAZJR9R0'
    text_to_translate = text

    # API终点
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    # 生成随机数
    salt = random.randint(32768, 65536)

    # 计算签名
    sign = hashlib.md5((app_id + text_to_translate + str(salt) + app_key).encode()).hexdigest()

    # 构造请求参数
    params = {
        'q': text_to_translate,
        'from': 'auto',
        'to': 'zh',  # 翻译目标语言，这里选择中文
        'appid': app_id,
        'salt': salt,
        'sign': sign
    }

    # 发送GET请求
    response = requests.get(url, params=params, proxies=proxies)

    # 解析响应
    result = response.json()
    translation = result['trans_result'][0]['dst']
    return translation

def extract_info(string):
    lines = string.split('\n')  # 将字符串按行分割成列表
    title = lines[0]  # 第二行为title
    layer_id = None
    bbox = None
    wmts_endpoint = None
    abstract = None
    projection = None
    if service == "EQ":
        service_lower = 'eqc'
    else:
        service_lower = service.lower()

    for index, line in enumerate(lines):
        if line.startswith('Layer ID :'):
            layer_id_raw = line.split(':')[1].strip()  # 提取Layer ID后的内容，并去除首尾空格
            layer_id = planet + "_" + service_lower + "_" + layer_id_raw
        elif line.startswith('bbox :'):
            bbox_str = line.split(':')[1].strip().split(',')  # 提取bbox后的内容，并去除首尾空格
            bbox = [float(num) for num in bbox_str]
        #elif line.startswith('WMTS Endpoint :'):
        #    start_index = line.index("WMTS Endpoint :") + len("WMTS Endpoint :")
        #    wmts_endpoint = line[start_index:].strip()

        elif line.startswith('Projection :'):
            projection_lines = lines[index + 1:]  # 获取"Projection"行后面的所有行
            projection_multilines = '\n'.join(projection_lines)  # 将这些行合并为一个字符串，每行之间用换行符分隔
            break
    
    pattern = r'\n\s*\n'
    projection = re.sub(pattern, '\n', projection_multilines)
    
    title = None
    for i, line in enumerate(lines):
        if 'Layer ID :' in line:
            title = lines[i-1].strip()
            break
    
    #abstract_index = info.find("Abstract")
    #colon_index = info.find(":", abstract_index)
    #abstract = info[colon_index+1:].split('\n', 1)[0]
    
    layerid_parts = layer_id.split('_')
    pic_name = "_".join(layerid_parts[2:])
    icon = "{MoonImage}\\" + layer_id + "\\" + pic_name + "-120.png"
    preview = "{MoonImage}\\" + layer_id + "\\index.html"
    wmts_capabilities =  "{MoonImage}\\" + layer_id + "\\WMTSCapabilities.xml"
    metadata = "{MoonImage}\\" + layer_id + "\\MetaData.html"
    folder_path = os.path.join(r'./', layer_id)
    
    #abstract_cn = translate_text(abstract)
    
    return title, layer_id, bbox, icon, preview, wmts_capabilities, metadata, projection, folder_path, pic_name


#生成config文件(config.json)
def generate_config_file(service, title, layer_id, bbox, projection, icon, abstract, preview, wmts_capabilities, metadata, folder_path):

    #projection_single_line = re.sub(r'[\n\t\s]', '', projection)
    projection_single_line = re.sub(r'"', '\'', projection[1:])  #去掉开头的换行符

    config = {
        "ProjectionType": service,
        "Title": title,
        "LayerID": layer_id,
        "Icon": icon,
        "BBOX": bbox,
        "Abstract": abstract_cn,
        "Projection": projection_single_line,
        "Preview": preview,
        "WMTS_Capabilities": wmts_capabilities,
        "MetaData": metadata
    }
    
    file_path = os.path.join(folder_path, "config.json")  # 指定文件夹路径和文件名
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

    print(f"config已保存到：{file_path}")

#下载wtms文件
def download_wmts(url):
    response = requests.get(url, stream=True, proxies=proxies)
    file_name = url.split('/')[-1]  # 获取文件名
       
    save_file_path = os.path.join(folder_path, file_name)  # 拼接保存文件的完整路径

    with open(save_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"wmts文件已保存到：{save_file_path}")


#下载pic文件
def download_pic(url):
    response = requests.get(url, stream=True, proxies=proxies)
    file_name = pic_name + '-120.png'  # 获取文件名
       
    save_file_path = os.path.join(folder_path, file_name)  # 拼接保存文件的完整路径

    with open(save_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f"pic文件已保存到：{save_file_path}")


#下载metadata文件
def save_webpage(url):
    response = requests.get(url, proxies=proxies)
    save_file_path = folder_path + '/' + 'metadata.html'

    with open(save_file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"meta网页已保存到：{save_file_path}")


#生成info文件
def write_to_info():
    layer_id_txt = "Layer ID:" + layer_id
    bbox_txt = "bbox:" + str(bbox)
    wmts_endpoint_txt = "WMTS Endpoint :" + wmts_endpoint
    abstract_txt = "Abstract :" + abstract
    projection_txt = "Projection:" + projection
    strings = [title, layer_id_txt, bbox_txt, wmts_endpoint_txt, abstract_txt, abstract_cn, projection_txt]
    
    save_file_path = folder_path + '/info.txt'
    
    with open(save_file_path, 'w', encoding="utf-8") as file:
        for idx, string in enumerate(strings, start=1):
            file.write(string + '\n')
    print(f"info已保存到：{save_file_path}")



#抓取abstract、wmts_endpoint
def extract_abstract():
       
    # 打开HTML文件
    with open(folder_path + '/' + 'metadata.html', 'r', encoding='utf-8') as file:
        html = file.read()

    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html, 'html.parser')

    # 提取文本
    text = soup.get_text()

    abstract_start = text.find("Abstract:")
    purpose_end = text.find("Purpose:")

    #metadata文件错误返回NaN
    if abstract_start == -1 or purpose_end == -1:
        print('metadata文件中未找到相关内容')
        abstract = 'NaN'
        abstract_cn =  'NaN'
        wmts_endpoint = 'https://trek.nasa.gov/tiles/' + planet + '/' +  service + '/' + pic_name
        return abstract, abstract_cn, wmts_endpoint

    abstract = text[abstract_start + len("Abstract:"):purpose_end].strip()
    abstract_cn = translate_text(abstract)
    
    wmts_endpoint = 'https://trek.nasa.gov/tiles/' + planet + '/' +  service + '/' + pic_name

    return abstract, abstract_cn, wmts_endpoint

#获取wmts中地图层数
def count_tile_matrices(xml_file):
    #with open(xml_file, 'r', encoding='utf-8') as file:
    #    xml = file.read()
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    tile_matrix_count = 0
    for element in root.iter('{http://www.opengis.net/wmts/1.0}TileMatrix'):
        tile_matrix_count += 1
    
    return tile_matrix_count

# Python实现unproject方法
def unproject(x, y):
    lon = x * 90.0 / (2727718) #月球直径1,737,400m
    lat = y * 90.0 / (2727718)
    return [lon, lat]

# Python实现unprojectToDegreesBounds方法
def unprojectToDegreesBounds(bounds):
    mins = unproject(bounds[0], bounds[1])
    maxs = unproject(bounds[2], bounds[3])
    #return [toDegrees(mins[0]), toDegrees(mins[1]), toDegrees(maxs[0]), toDegrees(maxs[1])]
    return [mins[0],mins[1], maxs[0], maxs[1]]


# 生成lrc文件，目前仅支持EQ，南北极需要手动修改bbox
def write_lrc():
    
    bbox_west = str(bbox[0])
    bbox_east = str(bbox[2])
    bbox_south = str(bbox[1])
    bbox_north = str(bbox[3])

    wmts_path = folder_path + '/' + 'WMTSCapabilities.xml'
    wmts_count = str(count_tile_matrices(wmts_path))

    with open('0.lrc', 'r', encoding='utf-8') as file:
        lrc_0 = file.read()
    replaced_xml = lrc_0.replace("{layer_name}", layer_id)
    replaced_xml = replaced_xml.replace("{wmts_url}", wmts_url)
    replaced_xml = replaced_xml.replace("{bbox_west}", bbox_west)
    replaced_xml = replaced_xml.replace("{bbox_east}", bbox_east)
    replaced_xml = replaced_xml.replace("{bbox_south}", bbox_south)
    replaced_xml = replaced_xml.replace("{bbox_north}", bbox_north)
    replaced_xml = replaced_xml.replace("{level_end}", wmts_count)

    lrc_path = folder_path + '/' + '0.lrc'
    with open(lrc_path, 'w', encoding='utf-8') as file:
        file.write(replaced_xml)

    print(f"lrc已保存到：{lrc_path}")


# 生成0_TyleType.txt文件，以供瓦片服务器自定义图源识别
def write_tile(tile_idx):
    tile_idx = str(tile_idx)
    save_file_path = folder_path + '/' + '0_TileType.txt'
    
    with open(save_file_path, 'w', encoding="utf-8") as file:
        file.write(tile_idx)
    print(f"0_TileType文件已保存到：{save_file_path}")

for info in info_s:
    
    print("------------------------------")
    #time.sleep(0.4)  #
     #开始读取info并生成文件

    title, layer_id, bbox, icon, preview, wmts_capabilities, metadata, projection, folder_path, pic_name = extract_info(info)

    wmts_url = 'https://trek.nasa.gov/tiles/' + planet + '/'+ service + '/' + pic_name + '/1.0.0/WMTSCapabilities.xml'
    pic_url = 'https://trek.nasa.gov/tiles/' + planet + '/'+ service + '/' + pic_name + '/thumbnail/' + pic_name + '-120.png'
    metadata_url = 'https://trek.nasa.gov/' + planet.lower() + '/TrekWS/rest/cat/metadata/fgdc/html?label=' + pic_name
    folder_path = './' + layer_id
    
    # 使用os.mkdir()函数创建文件夹
    if not os.path.exists(folder_path):
        #检查wmts文件是否正确
        wmts_respons = requests.get(wmts_url, proxies=proxies)
        if wmts_respons.status_code != 200:
            print(f"图层{layer_id}wmts文件获取失败. HTTP status code:", wmts_respons.status_code)
            info_error.append(info)
            #print(info)
            continue
        
        # 使用os.makedirs()函数创建文件夹（如果不存在）
        os.makedirs(folder_path)

    else:
        print(f"文件夹{layer_id}已经存在。")
        continue

    print(f"开始生成{layer_id}图层文件")


    # 生成 wmts、icon、metadata、info 文件
    download_wmts(wmts_url)
    download_pic(pic_url)
    save_webpage(metadata_url)
    abstract, abstract_cn, wmts_endpoint = extract_abstract()
    write_to_info()

    '''
    print("Title:", title)
    print("Layer ID:", layer_id)
    print("Icon:", icon)
    print("bbox:", bbox)
    print("WMTS Endpoint :", wmts_endpoint)
    print("Abstract :", abstract)
    print(abstract_cn)
    print("preview :", preview)
    print("wmts_capabilities :", wmts_capabilities)
    print("metadata :", metadata)
    print("Projection:", projection)
    '''

    # 生成 config.json 文件
    generate_config_file(service, title, layer_id, bbox, projection, icon, abstract, preview, wmts_capabilities, metadata, folder_path)

    # 生成 lrc 文件
    if service == 'SP' or service == 'NP':      #如果是南北极图层，修改bbox单位为degree
        bbox = unprojectToDegreesBounds(bbox)
    write_lrc()

    #生成0_TileType文件
    write_tile(tile_idx)
    tile_idx = tile_idx + 1
    
    print(f"图层{layer_id}文件已生成")    

# 打开txt文件以写入模式
with open('info_error.txt', 'w') as file:
    # 将列表中的元素逐行写入txt文件
    for element in info_error:
        file.write(element + '...')
print('错误图层信息已写入info_error.txt')
print('全部内容生成完毕')