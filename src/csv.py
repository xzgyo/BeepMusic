#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: csv.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-07
Last Modified: N/A
Version: 0.1.0
Description: csv.py
"""
import sys
import os
import csv
import time
import logging

from .config import *
from .note import note_to_frequency

logger = logging.getLogger(__name__)
logger.setLevel(log_lev)
handler = logging.StreamHandler()
handler.setLevel(log_lev)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

def play_from_csv(file_path: str, bpm: int=240, octave_shift: int=0, system: str="Linux"):
    """
    play_from_csv 的 Docstring
    
    :param file_path: 文件路径
    :type file_path: str
    :param bpm: 播放速度(BPM)
    :type speed: int
    :param octave_shift: 八度调整
    :type octave_shift: int
    :param system: 系统类型
    :type system: str
    """
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        sys.exit(1)
    logger.info(f"Playing file: {file_path}")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        ms_per_beat = (60 / bpm) * 1000
        for row in reader:
            if not row: continue
            note = row[0]
            beats = float(row[1])
            freq = note_to_frequency(note, octave_shift)
            duration = beats * ms_per_beat
            if freq > 0:
                if system == "Linux":
                    cmd = f'beep {freq} {duration}'
                elif system == "Windows":
                    cmd = f'powershell -c "[console]::beep({freq},{duration})"'
                else:
                    logger.error(f"Unknown system: {system}")
                    sys.exit(1)
                logger.info(f"N={note} B={beats} F={freq} D={duration}")
                res = os.system(cmd)
                if res != 0:
                    logger.error(f"Error with code {res} at running command `{cmd}`")
                    sys.exit(1)
            else:
                time.sleep(duration / 1000.0)
