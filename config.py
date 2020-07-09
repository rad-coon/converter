# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~~~~

    maps read pattern from json file.

    :copyright: 2020 rad-coon
    :license: BSD-3-Clause
"""

class Config:
  def __init__(self, pattern_json):
    self.quotechar = pattern_json['quotechar']
    self.delimiter = pattern_json['delimiter']
    self.ignore_header = pattern_json['ignore_first_line']
    self.column_schema = pattern_json['column_schema']
    self.row_schema = pattern_json['row_schema']
    self.logfile = pattern_json['logging']['logfile']
    self.log_to_file = pattern_json['logging']['log_to_file']
    self.max_byte_size = pattern_json['logging']['max_byte_size']
    self.backup_count = pattern_json['logging']['backup_count']
    self.log_format = pattern_json['logging']['log_format']
    self.log_debug = pattern_json['logging']['log_debug']
