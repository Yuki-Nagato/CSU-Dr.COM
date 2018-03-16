# 中南大学联通校园网客户端 Python版

## 环境

Python 3

## 快速上手

```
python3 csu-drcom.py login -u 帐号 -p 密码
```

## 登录

```
python3 csu-drcom.py login -u 帐号 -p 密码
python3 csu-drcom.py login -u 帐号 -p 密码 -s 服务器IP
python3 csu-drcom.py login -u 帐号 -p 密码 --test-address 用于探测服务器IP的网址
```

## 注销

```
python3 csu-drcom.py logout
python3 csu-drcom.py logout -s 服务器IP
```

## 说明

目前中南大学南校区服务器IP为`119.39.119.2`，如有变化我将更新。通过指定`-s`参数可以自定义该地址。