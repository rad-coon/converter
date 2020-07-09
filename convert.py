# -*- coding: utf-8 -*-
"""
    convert
    ~~~~~~~~~

    A simple command line application to cut and copy csv files.

    :copyright: 2020 rad-coon
    :license: BSD-3-Clause
"""
import csv
import json
import logging
from os import close
import re
from logging.handlers import RotatingFileHandler
import click
from flask import Flask
from flask.logging import default_handler
from flask_cli import FlaskCLI
from numpy.core.numeric import False_
import pandas as pd
import os

from config import Config

app = Flask('csv-converter')
FlaskCLI(app)


@app.cli.command('convert')
@click.argument('input')
@click.argument('output')
@click.argument('pattern')
def convert(input, output, pattern):
    """Kopiert Quell-CSV-Datei, unter Anwendung der Regeln in der Pattern-JSON-Datei, in Ziel-CSV-Datei. Siehe auch: https://github.com/rad-coon/converter/blob/master/README.MD"""

    # reading pattern
    config = read_pattern(pattern)
    setup_logging(config)

    app.logger.info('initialized')

    app.logger.debug(f'using delimiter: {config.delimiter}')
    app.logger.debug(f'using quotechar: {config.quotechar}')
    app.logger.debug(f'ignoring first line (header): {config.ignore_header}')

    col = 0
    for read_col in config.column_schema:
        app.logger.debug(f'reading pattern for column {col}: {read_col}')
        col += 1

    row = 0
    for read_row in config.row_schema:
        app.logger.debug(f'reading pattern for row {row}: {read_row}')
        row += 1

    # reading input file
    app.logger.info(f'reading from {input} ...')
    tmp_file = False
    if str.endswith(input, ('xls', 'xslx')):
        app.logger.debug('input file is excel file. creating csv copy...')
        data_xls = pd.read_excel(input, 0, index_col=None)
        data_xls.to_csv('tmp_input.csv', encoding='utf-8',
                        sep=config.delimiter, quotechar=config.quotechar, index=False)
        input = 'tmp_input.csv'
        tmp_file = True

    input_file = open(input, encoding='utf-8')
    input_data = csv.reader(
        input_file, delimiter=config.delimiter, quotechar=config.quotechar)

    target_array = []
    row = 0
    for row_data in input_data:
        # ignore header if enabled
        if row == 0 and config.ignore_header is True:
            row += 1
            continue

        # only copy line defined by pattern
        if config.row_schema[row - ((row//len(config.row_schema)) * len(config.row_schema))] is False:
            row += 1
            continue

        target_row = []
        row_length = len(row_data)
        col = 0
        while col < row_length:
            # only write column if allowed
            if config.column_schema[col] is True:
                app.logger.debug(
                    f'row: {row} column: {col} data: {row_data[col]}')
                target_row.append(row_data[col])
            elif config.column_schema[col] is False:
                app.logger.debug(f'row: {row} column: {col} ignoring column')
            # or if a regex is given
            else:
                app.logger.debug(
                    f'row: {row} column: {col} using regex + alt: {config.column_schema[col]}')
                regex_result = re.search(
                    config.column_schema[col]["regex"], row_data[col])
                if regex_result is not None:
                    target_row.append(regex_result.group(
                        config.column_schema[col]['group']))
                else:
                    target_row.append(config.column_schema[col]['alternate'])
            col += 1
        target_array.append(target_row)
        row += 1

    # writing to output file
    app.logger.info(f'writing to {output} ...')

    output_file = open(output, 'w', newline='', encoding='utf-8')
    ouput_file_writer = csv.writer(
        output_file, delimiter=config.delimiter, quotechar=config.quotechar)
    ouput_file_writer.writerows(target_array)

    input_file.close()
    output_file.close()

    if tmp_file:
        app.logger.debug(f'deleting tmp file {input}')
        os.remove(input)
        app.logger.debug(f'file deleted')
    app.logger.info('job finished')


def read_pattern(pattern):
    app.logger.info(f'using pattern file {pattern} ...')
    pattern_file = open(pattern)
    pattern_data = json.load(pattern_file)
    config = Config(pattern_data)
    return config


def setup_logging(config):
    formatter = logging.Formatter(config.log_format)
    app.logger.removeHandler(default_handler)
    app.logger.setLevel(
        logging.DEBUG if config.log_debug is True else logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if config.log_debug is True else logging.INFO)
    ch.setFormatter(formatter)
    app.logger.info(f'debug logging: {config.log_debug}')
    app.logger.addHandler(ch)

    if config.log_to_file is True:
        handler = RotatingFileHandler(
            config.logfile, maxBytes=config.max_byte_size, backupCount=config.backup_count)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.debug(f'logging to file: {config.logfile}')
        app.logger.debug(
            f'max size for log files set to {config.max_byte_size / (2 **20)} MB')
        app.logger.debug(
            f'keeping up to {config.backup_count} copies of older log files')
