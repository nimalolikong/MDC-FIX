<h1 align="center">MDC(源码修改自用版)</h1>

![img](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat)
![img](https://img.shields.io/badge/Python-3.8-yellow.svg?style=flat&logo=python) ![Static Badge](https://img.shields.io/badge/GPL-3.0%20license-gray)

# 开始之前

本人**究极懒狗**，技术也差，仅仅在原项目上简单添加了自己想要一些特性，保证自用舒服，**不保证维护**，**禁止一切商用**，**不发布各平台二进制文件(狗命要紧)**，要自改请直接下载源码或者克隆本项目。issues也不懂怎么搞，没怎么用过github,当自用出问题了就会更新，其他功能也不想实现，最近很忙也不会看反馈（忙毕业）

# 源项目

基于yoshiko2[Movie_Data_Caputure v6.6.7](https://github.com/yoshiko2/Movie_Data_Capture)

添加预览图代码逻辑参考来自[jav老司机](https://sleazyfork.org/zh-CN/scripts/25781-jav%E8%80%81%E5%8F%B8%E6%9C%BA)的加载预览大图部分（我直接开抄）

# **简单使用方法**

使用vscode运行源码，请下载好requirements.txt依赖，并将目标文件和目标文件夹地址添加到config.ini文件中，在Movie_Data_Capture.py文件运行整个项目，其他参考下面[AV_Data_Capture](https://github.com/YEreed/AV_Data_Capture)的使用文档，使用效果就不放上来了，有兴趣自己试试

# 改进

* 增加下载blogJAV、JAVStore的电影预览图到extrafanart(可能会存在下载到空图，不过无所谓,本来emby和jellyfin也没办法完全展示所有剧照)
* 实现Fanza,JAVBus统一搜索，保证ABC-123格式的番号都能在fanza，JAVBus被搜索到
  (目前我也只用这两个源)
* 支持Fanza搜索动漫名，并在config中新加anime_naming_rule满足里番电影不同标题命名需求，注意不是文件名，文件名默认为能匹配的日文标题，大部分能匹配成功，如果匹配失败请尝试修改官方日文名
* 修改Fanza刮削extrafanart失败(冬季特卖广告窗口给挡完了) ，新引入selenium作为webdriver，调试使用chrome(没有请[安装chrome](https://dl.google.com/tag/s/installdataindex/update2/installers/ChromeStandaloneSetup64.exe))从而关闭广告窗口并获取源码(会出现chrome调试窗口)  (请最好使用全局代理防止反复ssl连接失败)
* 修复一部分fc2刮削失败的问题，仅使用fc2和msin刮削，但是仍存在刮削失败的可能，而且无法刮削到sukebei.nyaa.si简介中的图片
* 增加番号统一化，实现番号保存格式都是 **ABC-123**
* 在nfo简介栏中默认写入番号，可在emby搭配油猴脚本[根据脚本快速搜索](https://sleazyfork.org/zh-CN/scripts/423350-%E6%A0%B9%E6%8D%AE%E7%95%AA%E5%8F%B7%E5%BF%AB%E9%80%9F%E6%90%9C%E7%B4%A2)-v0.17(作者没有维护最新版本，现阶段可使用最新版本是v0.17，请直接在历史版本安装-20231219)

# 待改进

* javbus刮削极个别有可能出现乱码，原因未知，出现乱码请使用单个Fanza源刮削

# 文档

* （因为上游项目更新，mdc原wiki已不可用，这里提供原版[AV_Data_Capture](https://github.com/YEreed/AV_Data_Capture)留存的教程,不保证完全可用，感谢YEreed大佬和yoshiko2大佬的分享（懒狗是这样的，啥都只能嫖别人的

# 申明

当你查阅、下载了本项目源代码，即代表你接受了以下条款

* 本项目和项目成果仅供技术，学术交流和Python3性能测试使用
* 用户必须确保获取影片的途径在用户当地是合法的
* 运行时和运行后所获取的元数据和封面图片等数据的版权，归版权持有人持有
* 本项目贡献者编写该项目旨在学习Python3 ，提高编程水平
* 本项目不提供任何影片下载的线索
* 请勿提供运行时和运行后获取的数据提供给可能有非法目的的第三方，例如用于非法交易、侵犯未成年人的权利等
* 用户仅能在自己的私人计算机或者测试环境中使用该工具，禁止将获取到的数据用于商业目的或其他目的，如销售、传播等
* 用户在使用本项目和项目成果前，请用户了解并遵守当地法律法规，如果本项目及项目成果使用过程中存在违反当地法律法规的行为，请勿使用该项目及项目成果
* 法律后果及使用后果由使用者承担
* 若用户不同意上述条款任意一条，请勿使用本项目和项目成果
