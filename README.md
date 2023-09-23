# 渲染监视器 - Python

## 前言
> 为了方便起见，我试图开发出一个可以监视MMD动画渲染进度的脚本，此脚本的基本功能有：
1. 监视文件夹内新增的文件，提取数字，即当前渲染帧数；
2. 计算前一帧到新增一帧的渲染时间；
3. 统计GPU使用率； 
4. 输入总帧数计算渲染进度，以及预计完成时间； 
5. 输出信息，以及API接口

## 前提
1. 需要输入或者拖入文件夹设置监视目录 
2. 需要输入总共渲染帧数
3. 被监视的文件夹内必须有：数字.xxx格式的文件，例如：001.jpg; out001.png;

## API格式
    data:{
        "total": 6000,
        "count": 2400 or '未开始',
        "timer": 6.4s,
        "gpu": 82%,
        "complete": 84.2%,
        "expected": '1小时21分钟'
    }

## 使用
1. 使用exe文件 [百度云下载]()
   1. 双击打开oversee.exe文件，此时会弹出cmd框
   2. 输入当前目录下的某个文件，或者拖入要监视的文件夹
   3. 输入动画需要渲染的总帧数
   4. 即可开始监视
2. 使用py文件 GitHub下载
   1. 安装所需要的拓展库
   2. 运行oversee.py文件 注意：需要在cmd里运行，在编辑器里运行会报错
   3. 转到上方使用exe文件的第二步开始


## 后记
作者：琰凛
