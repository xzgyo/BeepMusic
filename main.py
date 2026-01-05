#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: main.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-03
Last Modified: N/A
Version: 0.1.0
Description: main.py
"""
import sys
import os
import csv
import time
import platform
import logging
import argparse
import traceback

from src.config import log_fmt
from src.note import note_to_frequency

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

# argparse
parser = argparse.ArgumentParser(description="")
parser.add_argument("filepath", type=str, help="Audio's csv file path.")
parser.add_argument("-s", "--bpm", type=int, default=120, help="Speed (BPM)")
parser.add_argument("-o", "--octave", type=int, default=0, help="Octave shift ")
args = parser.parse_args()

def check_system(needed_system: str="Linux"):
    """
    check_system 的 Docstring
    
    :param needed_system: 说明
    :type needed_system: str
    """
    if platform.system() != needed_system:
        logger.error(f"Are you sure you're running this script on a {needed_system} computer???")
        logger.error(f"{needed_system} only!")
        sys.exit(1)

def check_driver_pcspkr():
    """
    check_driver_pcspkr() : 检测当前环境是否开启了pcspkr
    """
    check_cmd = "lsmod | grep pcspkr"
    need_run_if_no_driver = "sudo modprobe pcspkr"
    has_driver = os.popen(check_cmd).read()
    if not has_driver:
        logger.error("Need `pcspkr` mod")
        logger.error(f"Run '{need_run_if_no_driver}' first")
        sys.exit(1)

def calculate_beat_duration(bpm: int) -> int:
    """
    calculate_beat_duration 的 Docstring
    
    :param bpm: 速度(单位BMP)
    :type bpm: int
    :return: 计算所得的值
    :rtype: int
    """
    # Duration (ms) = \frac{60 \text{ seconds}}{BPM} \times 1000
    if bpm <= 0:
        return 0
    ms_per_beat = 60000 / bpm
    return int(ms_per_beat)

def play_music(file_path: str, speed: int=240, octave_shift: int=0):
    """
    play_music 的 Docstring
    
    :param file_path: 文件夹路径
    :type file_path: str
    :param speed: 播放速度(BPM)
    :type speed: int
    :param octave_shift: 八度调整
    :type octave_shift: int
    """
    check_system()
    check_driver_pcspkr()
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        sys.exit(1)
    logger.info(f"Playing file: {file_path}")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            note = row[0]
            beat = float(row[1])
            freq = note_to_frequency(note, octave_shift)
            duration = beat * calculate_beat_duration(speed)
            if freq > 0:
                cmd = f'beep -f {freq} -l {duration}'
                logger.info(f"N={note} B={beat} F={freq} D={duration}")
                res = os.system(cmd)
                if res != 0:
                    logger.error(f"Error with code {res} at running command `{cmd}`")
                    sys.exit(1)
            else:
                time.sleep(duration / 1000.0)

if __name__ == "__main__":
    csv_path = args.filepath
    speed = args.bpm
    octave_shift = args.octave
    logger.debug(f"filepath={csv_path} speed={speed} octave_shift={octave_shift}")
    try:
        play_music(csv_path, speed, octave_shift)
    except KeyboardInterrupt:
        logger.info('^C')
    except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            traceback.print_exc()
