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
初始化venv并安装依赖
```bash
python -m venv .venv
. .venv/bin/activate
pip3 install mido
pip3 install pandas
```
最后播放《Unwelcome School》
```bash
python3 main.py "music/Unwelcome School - Mitsukiyo.mid" -m midi -t 2 -s 180
```
或者使用music.csv中的
```bash
python3 main.py music.csv -s 180
```
> [!NOTE]
> 所有乐谱都在music目录下 


