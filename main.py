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

from src.config import log_fmt
from src.note import note_to_frequency

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

speed = 240

def play_music(file_path: str, octave_shift:int=0):
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
                freq = note_to_frequency(note, octave_shift)
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
        logger.error(f"参数错误，使用python3 {__file__} 文件名 ")
        sys.exit(1)
    else:
        csv_path = sys.argv[1]
        try:
            octave_shift = int(sys.argv[2])
        except:
            octave_shift = 0
        play_music(csv_path, octave_shift)