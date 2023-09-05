# -*- coding: utf-8 -*-
#   读取当前目录下所有文件夹，重新生成config.json文件
#       > 从0_TileType.txt文件中读取图层序号
#       > 读取config.json文件，增加WMTS_TypeId属性
#       > 从WMTSCapabilities.xml文件中获取瓦片的层级(最小默认为0),0级瓦片的行数和列数
#       > 重新保存config.json文件
#   增加如下属性：
#       "WMTS_TypeId": 
#       "MinimumLevel": 
#       "MaximumLevel": 
#       "NumberOfLevelZeroTilesX": 
#       "NumberOfLevelZeroTilesY":
#
#   本函数在所有图层文件夹已存在，但是原始config.json文件没有WMTS_TypeId属性时使用！！
#   blitheli 20210904


import os
import json
import xml.etree.ElementTree as ET

# 获取wmts中地图层数(实际需要-1),返回[瓦片层级数,0级瓦片列数,0级瓦片行数]


def getXmlData(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # MatrixWidth,MatrixHeight集合
    mws = root.findall('.//{http://www.opengis.net/wmts/1.0}MatrixWidth')
    mhs = root.findall('.//{http://www.opengis.net/wmts/1.0}MatrixHeight')

    tile_matrix_count = 0
    for element in root.iter('{http://www.opengis.net/wmts/1.0}TileMatrix'):
        tile_matrix_count += 1

    return [tile_matrix_count, int(float(mws[0].text)), int(float(mhs[0].text))]


# 获取当前目录
current_directory = os.getcwd()

# 获取当前目录下所有的子文件夹
subdirectories = [name for name in os.listdir(
    current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# 筛选出以 "Mars_eqc" 开头的文件夹名称
folders = [name for name in subdirectories if name.startswith("Mars_eqc")]

# 遍历当前目录下的子文件夹
for folder in folders:
    folder_path = os.path.join(current_directory, folder)

    # 从0_TileType.txt文件中读取图层序号
    tile_type_file_path = os.path.join(folder_path, "0_TileType.txt")
    with open(tile_type_file_path, "r", encoding="utf-8") as file:
        tile_idx = file.read()

    # 加载config.json文件，增加WMTS_TypeId属性
    configFilePath = os.path.join(folder_path, "config.json")
    with open(configFilePath, "r", encoding="utf-8") as file:
        configData = json.load(file)
        configData["WMTS_TypeId"] = tile_idx

    # 瓦片的层级(最小默认为0),0级瓦片的行数和列数(从WMTSCapabilities.xml文件中获取)
    maxLevel, zeroTileX, zeroTileY = getXmlData(
        folder_path + '/' + 'WMTSCapabilities.xml')
    configData["MinimumLevel"] = 0
    configData["MaximumLevel"] = maxLevel-1
    configData["NumberOfLevelZeroTilesX"] = zeroTileX
    configData["NumberOfLevelZeroTilesY"] = zeroTileY

    # 瓦片的行列数(从WMTSCapabilities.xml文件中获取)
    configData["NumberOfLevelZeroTilesX"] = 2
    configData["NumberOfLevelZeroTilesY"] = 1

    # 将config json数据重新保存
    with open(configFilePath, "w", encoding="utf-8") as file:
        json.dump(configData, file, indent=4, ensure_ascii=False)

print('所有文件夹内的config.json内容增加WMTS_TypeId...等属性！')
