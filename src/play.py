#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: play.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-07
Last Modified: N/A
Version: 0.1.0
Description: play.py
"""
import sys
import os
import platform
import logging

from .config import *
from .mid import play_from_midi, list_all_track
from .csv import play_from_csv

__all__ = ["play_file"]

logger = logging.getLogger(__name__)
logger.setLevel(log_lev)
handler = logging.StreamHandler()
handler.setLevel(log_lev)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

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


def play_file(file_path: str, method: str, bpm: int=120, octave_shift: int=0, *args, **kwargs) -> int:
    """
    play_music 的 Docstring
    
    :param file_path: 文件路径
    :type file_path: str
    :param method: 播放方式("csv"|"midi")，如果是midi则必须提供音轨号(track=)
    :type method: str
    :param bpm: 播放速度
    :type bpm: int
    :param octave_shift: 八度调整
    :type octave_shift: int
    """
    check_system()
    check_driver_pcspkr()
    if method == "csv":
        logger.info('Play from csv')
        play_from_csv(file_path, bpm, octave_shift)
    elif method == "midi":
        logger.info('Play from midi')
        if not 'track' in kwargs or kwargs['track'] < 0:
            logger.error("Which track in midi?")
            logger.info(f"\nList of all tracks:\n{list_all_track(file_path)}\n")
            return -1
        play_from_midi(file_path, kwargs["track"], bpm, octave_shift)
    return 0
