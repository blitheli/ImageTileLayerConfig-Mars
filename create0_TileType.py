# -*- coding: utf-8 -*-
#   读取当前目录下所有文件夹，重新生成0_TileType.txt文件，按照顺序生成编号
#   此时文件夹顺序为字母编号顺序，0_TileType.txt文件中的编号依次+1
#
#   本函数在所有图层文件夹已存在，但是想对图层重新编号时使用！！

#   blitheli 20210904


import os


# 火星图层的开始编号，之前已有一些
tile_idx = 1300000020

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
    tile_type_file_path = os.path.join(folder_path, "0_TileType.txt")
    with open(tile_type_file_path, "w", encoding="utf-8") as file:
        file.write(str(tile_idx))
        tile_idx = tile_idx + 1

print('所有文件夹内的0_TileType.txt内容生成完毕！')
