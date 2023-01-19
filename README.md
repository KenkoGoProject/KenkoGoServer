# KenkoGoServer

![Python Version](https://img.shields.io/badge/python-3.9.13-blue)
![License](https://img.shields.io/github/license/KenkoGoProject/KenkoGoServer)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/KenkoGoProject/KenkoGoServer)
![lines](https://img.shields.io/tokei/lines/github/KenkoGoProject/KenkoGoServer)

A Controller of [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

注意：[KenkoGoServer](https://github.com/KenkoGoProject/KenkoGoServer)不同于以前的[KenkoGo](https://github.com/AkagiYui/KenkoGoOld)，
该项目是一个RestfulAPI的程序，请通过HTTP请求来控制，当该项目进入稳定状态后，`KenkoGo`将被删除。

[该仓库](https://github.com/KenkoGoProject/KenkoGoServer) 仅实现守护服务，
功能实现请使用 [KenkoGoClient](https://github.com/KenkoGoProject/KenkoGoClient)，
或使用 [kenkogo-webui](https://github.com/KenkoGoProject/kenkogo-webui) 查看数据。


## 功能介绍 Introduction

这是一个 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp) 守护程序

用来管理一个 go-cqhttp 进程，监听并转发事件。

- [x] go-cqhttp 消息转发
- [x] 自动下载最新 go-cqhttp 二进制文件
- [x] 为客户端提供 go-cqhttp 状态变化事件
- [x] API 接口鉴权
- [ ] 掉线重启（已添加，未测试）
- [ ] 风控提示（已添加，未测试）
- [ ] 与 NoneBot2 的驱动对接

## 快速开始 Quick Start

### Windows 10 PowerShell

请确保你的机器有 **Python 3.9.13** 的环境，其他版本未经测试。

1. 部署运行环境

```ps
git clone https://github.com/KenkoGoProject/KenkoGoServer
cd ./KenkoGoServer
python -m venv venv
./venv/Scripts/activate
python -m pip install -r ./requirements.txt
cd ./src
```

2. 修改配置文件

你也可以跳过这一步， KenkoGo 将会自动生成一个配置文件。

```ps
cp config.yaml.bak config.yaml
```

> 配置项说明
>
> host: 监听地址，默认为 0.0.0.0，即监听所有地址。
>
> post: 监听端口，默认为 18082。
>
> github_proxy: GitHub 代理地址，暂时仅用于下载 go-cqhttp，目前仅支持 `ghproxy.com`，留空表示不使用代理。

3. 启动脚本

```ps
python ./main.py --debug
```

> 命令行参数说明
>
> -h --help: 显示帮助信息
>
> -a --auto-start: 自动启动 go-cqhttp
>
> -d --debug: 开启调试模式，将输出更多信息
>
> -c --config: 指定配置文件路径

4. 客户端连接

当控制台提示`KenkoGo Started at xxx`时，可输入`/help`查看可用的指令。

或者使用 [**KenkoGoClient**](https://github.com/KenkoGoProject/KenkoGoClient) 连接 KenkoGo。

还有一种可用但不推荐的方法是使用`/start`指令来启动 go-cqhttp 实例。

### Linux Debian 11

请确保你的机器有 **Python 3.9.13** 的环境，其他版本未经测试。

1. 部署运行环境

```shell
git clone https://github.com/AkagiYui/KenkoGoServer
cd ./KenkoGoServer
python3 -m venv venv
source ./venv/bin/activate

apt install libzbar0
python -m pip install -r ./requirements.txt

cd ./src
```

2. 修改配置文件

你也可以跳过这一步， KenkoGoServer 将会自动生成一个配置文件。

```shell
cp config.yaml.bak config.yaml
```

3. 启动脚本

```ps
python ./main.py --debug
```

4. 客户端连接

当控制台提示`KenkoGoServer Started at xxx`时，可输入`/help`查看可用的指令。

或者使用 [KenkoGoClient](https://github.com/KenkoGoProject/KenkoGoClient) 连接 KenkoGo。

还有一种可用但不推荐的方法是使用`/start`指令来启动 go-cqhttp 实例。


## 更新日志 [Changelog](Changelog.md)


## 注意事项 Tips

该项目尚未成熟，`master`分支仍处于开发阶段，请勿在生产环境使用。

该项目是我的第一个 Python 项目，代码中可能存在大量错误或不规范的地方，有任何问题请在 issues 上提出，以帮助我进步，谢谢。

建议仅使用该项目完成进程管理，其他功能实现可使用 [NoneBot2](https://v2.nonebot.dev/)

该项目未计划支持 Windows 10 以下版本的系统，并且非 amd64 架构的系统暂未经过测试。

## 开发相关 Development

- 操作系统：[Windows 10 19044.1586](https://www.microsoft.com/zh-cn/windows)
- 系统架构：amd64

### 使用技术 Technology Stack

- Python: [3.9.13](https://www.python.org/) [下载地址](https://www.python.org/downloads/release/python-3913/)
- 依赖表生成工具: [pip-tools 6.8.0](https://github.com/jazzband/pip-tools/)
- 导入排序工具: [isort 5.10.1](https://pycqa.github.io/isort/)
- 代码格式化工具: [flake8 4.0.1](https://flake8.readthedocs.io/en/latest/) [mypy 0.971](https://mypy.readthedocs.io/en/latest/)
- ~~构建工具: [Nuitka](https://nuitka.net/) [下载地址](https://nuitka.net/doc/download.html)~~
- ~~数据库: [SQLite](https://www.sqlite.org/index.html)~~
- ~~自动构建: [GitHub Actions](https://https://docs.github.com/cn/actions)~~

### 运行时Python包  Runtime Python Package

- [rich 12.5.1](https://github.com/Textualize/rich/blob/master/README.cn.md) 控制台美化工具
- [ruamel.yaml 0.17.21](https://yaml.readthedocs.io/en/latest/) Yaml解析工具
- [uvicorn 0.18.2](https://www.uvicorn.org/) ASGI web 服务器
- [fastapi 0.79.0](https://fastapi.tiangolo.com/zh/) HTTP/Websocket服务器
- [requests 2.28.1](https://requests.readthedocs.io/en/latest/) HTTP客户端
- [websockets 10.3](https://websockets.readthedocs.io/en/stable/) Websocket 协议框架
- [python-multipart 0.0.5](https://github.com/andrew-d/python-multipart) 提供 multipart/form-data 的上传功能
- [psutil 5.9.1](https://github.com/giampaolo/psutil) 系统信息获取工具
- [distro 1.7.0](https://github.com/python-distro/distro) 系统平台信息获取工具
- [Pillow 9.2.0](https://python-pillow.org/) 图像处理工具
- [qrcode 7.3.1](https://github.com/lincolnloop/python-qrcode) 二维码生成工具
- [pyzbar 0.1.9](https://pypi.org/project/pyzbar/) 二维码识别工具

### 待办事项 Todo

- [ ] 自动修改标题含 QQ 昵称
- [ ] 编写 Nuitka 脚本
- [ ] 记录客户端登入时间戳
- [ ] 获取上传的文件列表
- [ ] 定时删除过期的文件
- [ ] 实例运行时允许先下载其他版本，其他时间再替换
- [ ] 配置文件缺少项目时写出默认值

## 从代码开始 Start from Code

### 代码检查 Code Lint

```shell
python -m pip install -r ./requirements-dev.txt
python ./code_lint.py
```

### 构建 Build

```shell
python -m pip install -r ./requirements-build.txt
python ./build_binary.py
```

### 构建 Docker Image

```shell
docker build -t kenkogo-server .
```
