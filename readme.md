本项目为 “瓦片服务器”发布的影像 创建Config文件，便于网站调用，显示所有图层信息

### 本项目仅为生成Mars的图层！
### 根据info.txt内的内容，自动创建所有图层的文件夹，以用于“瓦片服务器”中的“自定义图源”文件夹
### 大部分图层来源于：https://trek.nasa.gov/tiles/apidoc/trekAPI.html?body=mars
### 在每个图层文件内部
- info.txt              为图层的描述信息，自动从总文件中提取, 以供参考
- index.html            为图层的预览文件(手动或自动生成)
- WMTSCapabilities.xml  为图层的WMTS能力文件
- **.png                为图层的预览图
- metadata.html         为图层的元数据文件


## 通过调用createMoonConfig.py、createMarsConfig.py，自动生成 配置文件, 里面为每个图层的元数据信息描述，供网站调用
- MoonLayerConfig.json
- MarsLayerConfig.json


## 运行
- 将此文件夹通过IIS或其他服务器发布即可，客户端直接调用 **Config.json 即可！


## 数据来源
- 大部分图层文件夹来源于“红豆地球”生成的“自定义图源”内文件夹
- 新增一个数据源后，从“红豆地球”-“自定义图源”内拷贝出到此处
- 然后在文件夹内添加额外信息，如：index.html、metadata.html、**.png、WMTSCapabilities.xml
- 其中index.html需要独立测试下，是否能正常显示！右键"open with live server"，自动启动浏览器，如果能正常显示，就可以了！    


 ## 数据下载
- 在moontrek网站下载月球南北极数据时，需下载原始tif数据，发布成arcgis服务，再使用切片下载工具下载
- 下载网址格式https://trek.nasa.gov/moon/TrekWS/rest/cat/data/stream?label=[layerID]
- 其中[layerID]为moonterk中的layer_ID

## 自动创建文件夹并下载图层信息数据
- 将图层信息复制到info.txt文件中，可参考其中内容，不用点击abstract和wmts_endpoint，可自动抓取
- 运行createLayerInfo_multiInfo，自动创建文件夹并下载图层信息数据，包括png图片、config.json、wmts文件、metadata文件、info.txt、lrc文件、序号文件
- 运行前注意填写星球（Moon、Mars）及图层类型（EQ、NP、SP）
- 当前支持多个信息同时读取并生成，但仅支持相同星球和图层类型的info信息


20230614    初次编写
20230621    增加了自动生成配置文件的功能
20230703    增加了月球北极和南极的图层
20230710    增加了图层信息自动生成功能
20230713    优化了图层信息自动生成功能，支持生成lrc、序号文件，并支持多个信息同时生成
20230724    优化图层信息自动生成功能，对于wmts链接失效的图层可单独保留在新的info_error文件中
20230724    集中对全部moon_eqc图层进行了编号，保存在tile_idx_eqc.xlsx文件中，并生成了index.html文件
20230728    Moon_eqc_gggrx_1200a_anom_l1200.eq 的id错误
            Moon_eqc_gggrx_1200a_geoid_l660.eq
20230903    更改为Mars单独项目
            初次生成所有mars图层文件夹，暂时metadata无法获取！
            此次生成的0_TileType可以用于红豆地球的自定义图源！
            后续待metadata可获取后，可重新删除所有文件重新生成！
            config.json中增加WMTS_TileId,minimumLevel等属性
            生成index.html文件
