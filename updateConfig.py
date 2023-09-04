# -*- coding: utf-8 -*-
#   读取当前目录下所有文件夹，重新生成config.json文件
#       > 从0_TileType.txt文件中读取图层序号
#       > 读取config.json文件，增加WMTS_TypeId属性
#       > 重新保存config.json文件
#
#   本函数在所有图层文件夹已存在，但是原始config.json文件没有WMTS_TypeId属性时使用！！
#   blitheli 20210904


import os
import json

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
        data = json.load(file)
        data["WMTS_TypeId"] =  tile_idx

    with open(configFilePath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

print('所有文件夹内的config.json内容增加WMTS_TypeId属性！')
