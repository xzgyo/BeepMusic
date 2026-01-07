#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: note.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-04
Last Modified: N/A
Version: 0.1.0
Description: note.py
"""
import sys
import math
import logging

from .config import *

logger = logging.getLogger(__name__)
logger.setLevel(log_lev)
handler = logging.StreamHandler()
handler.setLevel(log_lev)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

def note_to_frequency(note_str: str, octave_shift:int=0):
    if note_str == "0": #空拍
        return 0
    # 音符名到半音偏移的映射(C为0)
    note_map = {
        'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
    }
    note_name = note_str[0].upper()
    try:
        octave = int(''.join(filter(str.isdigit, note_str))) # 提取八度(尾随数字)
    except ValueError:
        octave = 4  # 如果没写数字，默认给个 4
    octave += octave_shift
    semitones = note_map[note_name] # 计算基础半音值
    # 变音符号(#/b)
    if '#' in note_str:
        semitones += 1
    elif 'b' in note_str:
        semitones -= 1
    
    # A4=440Hz是基准
    # 计算相对于 A4 的半音距离
    # C4 的半音数是 12 * 4 + 0 = 48
    # A4 的半音数是 12 * 4 + 9 = 57
    current_note_value = 12 * octave + semitones
    a4_value = 12 * 4 + 9
    n = current_note_value - a4_value

    # 计算公式f = 440 \times 2^{\frac{n}{12}}
    frequency = 440 * (2 ** (n / 12))
    return round(frequency, 2) # 保留两位小鼠

def test(test_notes=["C4", "D4", "A3", "A4#", "B4b", "0"]):
    for note in test_notes:
        logger.info(f"Note={note:<3} Frequency: {note_to_frequency(note)} Hz")

if __name__ == '__main__':
    test()