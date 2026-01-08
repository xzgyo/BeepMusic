#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: mid.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-07
Last Modified: N/A
Version: 0.1.0
Description: mid.py
"""
import os
import sys
import time
import mido
import logging

from .config import *

logger = logging.getLogger(__name__)
logger.setLevel(log_lev)
handler = logging.StreamHandler()
handler.setLevel(log_lev)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

__all__ = ["play_from_midi", "list_all_track"]

def play_from_midi(file_path: str, track_index: int, bpm: int=120, octave_shift: int=0):
    """
    play_from_midi 的 Docstring
    
    :param file_path: 文件路径
    :type file_path: str
    :param track_index: 音轨序号
    :type track_index: int
    :param bpm: 播放速度(BPM)
    :type bpm: int
    :param octave_shift: 八度调整
    :type octave_shift: int
    """
    mid = mido.MidiFile(file_path)
    logger.info(f"Playing midi file: {file_path}")
    # notes_data's format: {'freq': 1234, 'beats': 1.0}
    notes_data = parse_midi_to_notes(mid, track_index, octave_shift) 
    ms_per_beat = (60 / bpm) * 1000 # 单位: ms
    for item in notes_data:
        #if not row: continue
        freq = float(item['freq'])
        beats = item['beats']
        duration = beats * ms_per_beat
        if freq > 0:
            cmd = f'beep -f {freq} -l {duration}'
            logger.info(f"B={beats:.4f} F={freq:.2f} D={duration:.2f}")
            res = os.system(cmd)
            if res != 0:
                logger.error(f"Error with code {res} at running command `{cmd}`")
                sys.exit(1)
        else:
            time.sleep(duration / 1000.0)

def parse_midi_to_notes(mid: mido.MidiFile, track_index: int, octave_shift:int=0):
    """
    parse_midi_to_notes 的 Docstring
    
    :param mid: 打开的MIDI文件
    :type mid: mido.MidiFile
    :param track_index: 音轨序号
    :type track_index: int
    :param octave_shift: 八度调整
    :type octave_shift: int
    """
    logger.info("Converting midi file to list[]")
    track = mid.tracks[track_index]
    ticks_per_beat = mid.ticks_per_beat
    results = []
    active_notes = {}
    last_event_end_tick = 0
    current_tick = 0
    for msg in track:
        current_tick += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            if current_tick > last_event_end_tick:
                results.append({'freq': '0', 'beats': (current_tick - last_event_end_tick) / ticks_per_beat})
            active_notes[msg.note] = current_tick
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in active_notes:
                start_tick = active_notes.pop(msg.note)
                duration_beats = (current_tick - start_tick) / ticks_per_beat
                results.append({'freq': note_number_to_frequency(msg.note, octave_shift), 'beats': duration_beats})
                last_event_end_tick = max(last_event_end_tick, current_tick)
    logger.info("Convert midi file to list[] success")
    return results

def note_number_to_frequency(note_number: int, octave_shift: int=0) -> float:
    if note_number == 0:  # 休止符
        return 0
    adjusted_note = note_number + (octave_shift * 12)
    freq = 440 * (2 ** ((adjusted_note - 69) / 12))
    return freq

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

# def midi_note_number_to_name(n):
#     names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
#     res = f"{names[n%12]}{(n//12)-1}"
#     logger.debug(f"n={n} res={res}")
#     input()
#     return res

# if __name__ == "__main__":
#     play_from_midi(sys.argv[1], 1, 240, 2)