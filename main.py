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
import os
import sys
import logging
import argparse
import traceback

from src.config import *
from src.play import play_file

# logging
logger = logging.getLogger(__name__)
logger.setLevel(log_lev)
handler = logging.StreamHandler()
handler.setLevel(log_lev)
formatter = logging.Formatter(log_fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)

# argparse
parser = argparse.ArgumentParser(description="")
parser.add_argument("filepath", type=str, help="Audio's csv file path.")
parser.add_argument("-m", "--method", type=str, default="csv", choices=["csv", "midi"], help="Playback method")
parser.add_argument("-s", "--bpm", type=int, default=120, help="Speed (BPM)")
parser.add_argument("-o", "--octave", type=int, default=2, help="Octave shift ")
parser.add_argument("-t", "--track", type=int, default=-1, help="Track No.")
args = parser.parse_args()

if __name__ == "__main__":
    method = args.method
    file_path = args.filepath
    speed = args.bpm
    octave_shift = args.octave
    track = args.track
    logger.debug(f"method={method} filepath={file_path} speed={speed} octave_shift={octave_shift}{f" track={track}" if method == "midi" else ""}")
    try:
        res = play_file(file_path, method, speed, octave_shift, track=track)
        sys.exit(res)
    except KeyboardInterrupt:
        logger.info('^C')
    except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            traceback.print_exc()
