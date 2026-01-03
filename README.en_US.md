# BeepMusic  
[中文版](./README.md)  
## Description  
Playing music using the motherboard buzzer on Linux  
## How To Run  
First, install the package `beep`. (Using a deb-based Ubuntu system as an example.)  
```bash
sudo apt install beep
```
Then enable the `pcspkr` modprobe.  
```bash
sudo modprobe pcspkr
```
Finally, the melody from `music.csv` will be played.  
```bash
python3 main.py music.csv
```
> [!NOTE]
> About `music.csv`  
> The author gave you sheet music for Senbonzakura (Thousand Cherry Blossoms), ~~how wonderful!~~  


