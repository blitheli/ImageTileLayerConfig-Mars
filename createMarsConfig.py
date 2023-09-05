#   读取当前目录下所有文件夹内的config.json文件，生成特定的json对象（放在Layers数组中），并保存为文件
#   20230705  liyunfei
#   20230905  增加TileUrlTemplate属性属性
#
import os
import json
import datetime

def read_config():

    config_data = {"Description":"本文件存储了瓦片服务器发布的相关图层信息",
                   "version":"1.0.0",
                   "Author":"liyunfei",
                   "TileUrlTemplate":"http://{ip}:{port}/type={WMTS_TypeId}&x={x}&y={y}&z={z}",
                   "CreateTime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   "Layers": []}
    
    # 循环每个文件夹 
    for root, dirs, files in os.walk(".", topdown=True):
        
        # 只处理Mars目录下的文件
        if not root.startswith(".\\Mars"):
            continue

        # 循环每个文件
        for name in files:
            if name == "config.json":
                file_path = os.path.join(root, name)
                with open(file_path, "r", encoding='utf-8') as config_file:
                    config_data['Layers'].append(json.load(config_file))

    return config_data

jsonConfig = read_config()
with open("MarsLayerConfig.json", "w", encoding='utf-8') as file:
    json.dump(jsonConfig, file, indent=4, ensure_ascii=False) # 保证中文不乱码

print("----------end----------")