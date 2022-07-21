# KenkoGoServer

![Python Version](https://img.shields.io/badge/python-3.9.13-blue)
![License](https://img.shields.io/github/license/AkagiYui/KenkoGoServer)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/AkagiYui/KenkoGoServer)
[![OSCS Status](https://www.oscs1024.com/platform/badge/AkagiYui/KenkoGoServer.git.svg)](https://www.murphysec.com/dr/nz85l1OmneIOz3uzYE)

A Controller of [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[该仓库](https://github.com/AkagiYui/KenkoGoServer) 仅实现后端服务，~~前端服务请前往 [kenkogo-webui](https://github.com/AkagiYui/kenkogo-webui)~~


## 功能介绍 Introduction

这是一个 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp) 守护程序

用来管理一个~~或多个~~ go-cqhttp 进程，监听并转发事件。
提供`掉线重连`,`风控提示`等功能。

## 快速开始 Quick Start

```shell
chmod +x ./kenkogo
./kenkogo --debug
```

> 命令行参数说明
> 
> --debug: 开启调试模式，将输出更多信息

当控制台提示`启动完毕`时，可输入`/help`查看可用的指令。


## 更新日志 [Changelog](Changelog.md)


## 注意事项 Tips

该项目尚未成熟，`master`分支仍处于开发阶段，请勿在生产环境使用。

该项目是我的第一个 Python 项目，代码中可能存在大量错误或不规范的地方，有任何问题请在 issues 上提出，以帮助我进步，谢谢。

建议仅使用该项目完成进程管理，其他功能实现可使用 [NoneBot2](https://v2.nonebot.dev/)


## 开发相关 Development

### 使用技术 Technology Stack

Python: [3.9.13](https://www.python.org/) [下载地址](https://www.python.org/downloads/release/python-3913/)

打包工具: [Nuitka](https://nuitka.net/) [下载地址](https://nuitka.net/doc/download.html)

数据库: [SQLite](https://www.sqlite.org/index.html)

自动构建: [GitHub Actions](https://https://docs.github.com/cn/actions)

### Python包 Python Package

- [pip-tools 6.8.0](https://github.com/jazzband/pip-tools/) 依赖表生成工具
- [isort 5.10.1](https://pycqa.github.io/isort/) 导入排序工具
- [rich 12.5.1](https://github.com/Textualize/rich/blob/master/README.cn.md) 控制台美化工具
- [ruamel.yaml 0.17.21](https://yaml.readthedocs.io/en/latest/) Yaml解析工具
- [uvicorn 0.18.2](https://www.uvicorn.org/) ASGI web 服务器
- [fastapi 0.79.0](https://fastapi.tiangolo.com/zh/) HTTP/Websocket服务器

### 待办事项 Todo

- [ ] 为 NoneBot2 的驱动提供接口
- [ ] 集成 [Socket.IO](https://github.com/miguelgrinberg/python-socketio)
- [ ] 集成 [websocket](https://websockets.readthedocs.io/en/stable/)[-client](https://github.com/websocket-client/websocket-client)
- [ ] 集成 [websockets](https://websockets.readthedocs.io/en/stable/)
- [ ] 使用 https://github.com/rholder/retrying
- [ ] 编写 Nuitka 脚本
- [ ] [distro](https://github.com/python-distro/distro) 系统平台信息获取工具
- [ ] [requests](https://requests.readthedocs.io/en/latest/) HTTP客户端

## 从代码开始 Start from Code

请确保你的机器有 **Python 3.9.10** 的环境，其他版本未经测试。

1. 部署运行环境

```shell
git clone https://github.com/AkagiYui/KenkoGoServer
cd ./KenkoGoServer
python -m venv venv
./venv/Scripts/activate
python -m pip install -r ./requirements.txt
```

2. 修改配置文件

```shell
cd ./src
cp config.yml.bak config.yml
```

3. 启动脚本

```shell
python ./main.py --debug
```
