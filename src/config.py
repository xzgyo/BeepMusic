#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: config.py
Author: xzgyo
Email: xzgyo@outlook.com
Created: 2026-01-04
Last Modified: N/A
Version: 0.1.0
Description: Project configuration file
"""
import logging

__all__ = ["log_fmt", "log_lev"]

log_fmt = '%(asctime)s [%(filename)s] [%(levelname)s] %(message)s'
log_lev = logging.DEBUG