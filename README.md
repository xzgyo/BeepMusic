# BeepMusic  
[English Version](./README.en_US.md)  
## 简介  
Linux上使用主板蜂鸣器放音乐  
## 如何运行  
先安装`beep`软件包，以deb系的Ubuntu为例  
```bash
sudo apt install beep
```
然后开启`pcspkr`功能  
```bash
sudo modprobe pcspkr
```
最后以`music.csv`中的旋律演奏（以速度180，升2个八度的方式）  
```bash
python3 main.py music.csv -s 180 -o 2
```
> [!NOTE]
> 关于`music.csv`  
> 作者送了你一个千本樱的乐谱，~~多好啊~~  


