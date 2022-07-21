# 提交前检查！

## 编写 更新日志

`U` Updated 增强了某个功能

`F` Fixed 修复了某个功能

`A` Added 增加了某个功能

`D` Deprecated 弃用了某个功能

`R` Removed 删除了某个功能

## 版本号 信息修改

VERSION 加一

VERSION_STRING 修改

## 更新 依赖表

检查 `requirements.in` 文件

```shell
# 生成 requirements.txt
pip-compile  --annotation-style=line
```

## 导入排序

```shell
isort .
```