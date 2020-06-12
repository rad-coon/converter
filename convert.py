# -*- coding: utf-8 -*-
"""
    convert
    ~~~~~~~~~

    A simple command line application to cut and copy csv files.

    :copyright: 2020 rad_coon
    :license: BSD-3-Clause
"""
import click
import json
import csv
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cli import FlaskCLI
from config import Config

app = Flask('csv-converter')
FlaskCLI(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.cli.command('convert')
@click.argument('input')
@click.argument('output')
@click.argument('pattern')
def convert(input, output, pattern):
    # reading pattern
    config = read_pattern(pattern)
    app.logger.info('initialized')
    if config.log_to_file is True:
        activate_file_logging(config.logfile)    

    app.logger.debug(f'using delimiter: {config.delimiter}')
    app.logger.debug(f'using quotechar: {config.quotechar}')
    app.logger.debug(f'ignoring first line (header): {config.ignore_header}')
    col=0
    for read_col in config.schema:
        app.logger.debug(f'reading pattern for column {col}: {read_col}')
        col+=1

    # reading input file
    app.logger.info(f'reading from {input} ...')
    input_file=open(input)
    input_data = csv.reader(input_file, delimiter=config.delimiter, quotechar=config.quotechar)

    target_array = []
    row = 0
    for row_data in input_data:
        if row == 0 and config.ignore_header is True:
            row+=1
            continue

        target_row=[]
        row_length = len(row_data)
        col = 0
        while col < row_length:
            if config.schema[col] is True:
                app.logger.debug(f' row: {row} column: {col} data: {row_data[col]}')
                target_row.append(row_data[col])
            else:
                app.logger.debug(f' row: {row} column: {col} ignoring column')
            col+=1
        target_array.append(target_row)
        row+=1


    # writing to output file
    app.logger.info(f'writing to {output} ...')

    output_file = open(output, 'w', newline='')
    ouput_file_writer = csv.writer(output_file, delimiter=config.delimiter, quotechar=config.quotechar)
    ouput_file_writer.writerows(target_array)

    app.logger.info('job finished')

def read_pattern(pattern):
    app.logger.info(f'using pattern file {pattern} ...')
    pattern_file=open(pattern)
    pattern_data=json.load(pattern_file)
    config = Config(pattern_data['quotechar'],pattern_data['delimiter'],
                    pattern_data['ignore_first_line'],pattern_data['schema'],
                    pattern_data['logging']['logToFile'],pattern_data['logging']['logfile'])
    return config

def activate_file_logging(filename):
    log_file = filename
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    handler = RotatingFileHandler(log_file,maxBytes=5000000, backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    