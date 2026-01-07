#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: mid_to_csv.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-07
Last Modified: N/A
Version: 0.1.0
Description: mido to csv. DONT USE THIS FILE NOW!!!
"""

import io
import sys
import mido
import pandas
import logging

from .config import *

__all__ = []#__all__ = ["midi_track_to_csv", "list_all_track"]
sys.stderr.write('DONT USE THIS FILE NOW!!!\n')
sys.exit(0)

logger = logging.getLogger(__name__)
logger.setLevel(log_lev)
handler = logging.StreamHandler()
handler.setLevel(log_lev)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

def midi_track_to_csv(midi_file_path: str, track_index: int) -> str:
    """
    midi_track_to_csv 的 Docstring
    
    :param midi_file_path: MIDI文件路径
    :type midi_file_path: str
    :param track_index: 音轨号
    :type track_index: int
    :return: csv文件内容
    :rtype: str
    """
    logger.debug(f"Start to convert '{midi_file_path}' to csv.")
    mid = mido.MidiFile(midi_file_path)
    if track_index >= len(mid.tracks):
        logger.error(f"该 MIDI 只有 {len(mid.tracks)} 条音轨")
        return ""
    selected_track = mid.tracks[track_index]
    events = []
    for msg in selected_track:
        event_dict = msg.dict()
        data = {
            'type': msg.type,
            **event_dict
        }
        events.append(data)
    df = pandas.DataFrame(events)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    logger.debug(f"File '{midi_file_path}'s cvs is ready.")
    return csv_buffer.getvalue()

def list_all_track(midi_file_path: str) -> str:
    """
    list_all_track 的 Docstring
    
    :param midi_file_path: MIDI文件路径
    :type midi_file_path: str
    :return: 说明
    :rtype: str
    """
    mid = mido.MidiFile(midi_file_path)
    res_list = []
    for i, track in enumerate(mid.tracks):
        res_list.append(f"Track {i}: {track.name}")
    return "\n".join(res_list)

def test(midi_file_path: str):
    logger.debug(list_all_track(midi_file_path))
    track = int(input("Track: "))
    logger.debug(midi_track_to_csv(midi_file_path, track))

if __name__ == "__main__":
    test(sys.argv[1])
