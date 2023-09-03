# -*- coding: utf-8 -*-
#   读取当前所有文件夹(Mars_eqc开头的)，和相应图层序号,生成Mars_EQ.xlsx文件
#       1 文件夹名称为图层编号
#       2 0_TileType.txt文件中的图层编号
#   假设所有图层中都有0_TileType.txt文件
#
#   20230903    初次改编,blitheli
import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd

# 运行前注意填写行星和图层类型
planet = 'Mar'  # 月球为Moon，火星为Mars
service = 'EQ'  # 赤道为EQ，北极为NP，南极为SP

# 创建一个空的DataFrame对象
df = pd.DataFrame(columns=['layer_id', 'tile_idx'])

# 获取当前目录
current_directory = os.getcwd()

# 获取当前目录下所有的子文件夹
subdirectories = [name for name in os.listdir(
    current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# 筛选出以 "Mars_eqc" 开头的文件夹名称
folders = [name for name in subdirectories if name.startswith("Mars_eqc")]

# 遍历当前目录下的子文件夹(默认每个子文件夹下都有0_TileType.txt文件)
for folder in folders:
    folder_path = os.path.join(current_directory, folder)
    # 从0_TileType.txt文件中读取图层序号tile_idx
    tile_type_file_path = os.path.join(folder_path, "0_TileType.txt")
    with open(tile_type_file_path, "r", encoding="utf-8") as file:
        tile_idx = file.read().strip()
    # 将数据添加到DataFrame
    df.loc[len(df)] = [folder, tile_idx]

# 保存DataFrame到Excel文件(Mars_EQ.xlsx)
df.to_excel('Mars_EQ.xlsx', index=False)
print('所有图层的名称和编号写入到Mars_EQ.xlsx文件中！！')