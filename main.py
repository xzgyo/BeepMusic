import sys
import os
import csv
import time
import platform
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


N = {
    '0': 0,
    'CL3': 131, 'CL4': 147, 'CL5': 165, 'CL6': 175, 'CL7': 196,
    'C3': 262, 'D3': 294, 'E3': 330, 'F3': 349, 'G3': 392, 'A3': 440, 'B3': 494,
    'C4': 523, 'D4': 587, 'E4': 659, 'F4': 698, 'G4': 784, 'A4': 880, 'A4#': 932, 'B4': 988,
    'C5': 1047, 'D5': 1175, 'E5': 1319, 'F5': 1397, 'G5': 1568, 'A5': 1760, 'B5': 1976
}
speed = 240

def play_music(file_path):
    if platform.system() != "Linux":
        logger.error("仅支持Linux")
        sys.exit(1)

    has_driver = os.popen("lsmod | grep pcspkr").read()
    if not has_driver:
        logger.error("请先运行sudo modprobe pcspkr")
        sys.exit(1)

    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        sys.exit(1)

    logger.info(f"Playing file: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row: continue
                note = row[0]
                beat = float(row[1])
                freq = N[note]
                duration = beat * speed
                if freq > 0:
                    cmd = f'beep -f {freq} -l {duration}'
                    logger.info(f"N={note} B={beat} F={freq} D={duration}")
                    res = os.system(cmd)
                    if res != 0:
                        logger.error(f"Error with code {res} at running command `{cmd}`")
                        sys.exit(1)
                else:
                    time.sleep(duration / 1000.0)
    except KeyboardInterrupt:
        logger.error("\n已停止")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("未指定文件")
        sys.exit(1)
    else:
        csv_path = sys.argv[1]
        play_music(csv_path)