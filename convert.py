# -*- coding: utf-8 -*-
"""
    convert
    ~~~~~~~~~

    A simple command line application to cut and copy csv files.

    :copyright: 2020 Stefan Reinhardt
    :license: BSD-3-Clause
"""
import click
import json
import csv
import logging
from flask import Flask
from flask_cli import FlaskCLI

app = Flask('csv-converter')
FlaskCLI(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.logger.info('initialized')

@app.cli.command('convert')
@click.argument('input')
@click.argument('output')
@click.argument('pattern')
def convert(input, output, pattern):
    # reading pattern
    app.logger.debug(f'using pattern file {pattern} ...')
    pattern_file=open(pattern)
    pattern_data=json.load(pattern_file)

    delimiter = pattern_data["delimiter"]
    quotechar = pattern_data["quotechar"]
    ignore_header = pattern_data["ignore_first_line"]
    schema = pattern_data["schema"]

    app.logger.debug(f'using delimiter: {delimiter}')
    app.logger.debug(f'using quotechar: {quotechar}')
    app.logger.debug(f'ignoring first line (header): {ignore_header}')
    col=0
    for read_col in schema:
        app.logger.debug(f'reading pattern for column {col}: {read_col}')
        col+=1

    # reading input file
    app.logger.info(f'reading from {input} ...')
    input_file=open(input)
    input_data = csv.reader(input_file, delimiter=delimiter, quotechar=quotechar)

    target_array = []
    row = 0
    for row_data in input_data:
        if row == 0 and ignore_header is True:
            row+=1
            continue

        target_row=[]
        row_length = len(row_data)
        col = 0
        while col < row_length:
            if schema[col] is True:
                app.logger.debug(f' row: {row} column: {col} data: {row_data[col]}')
                target_row.append(row_data[col])
            else:
                app.logger.debug(f' row: {row} column: {col} ignoring column')
            col+=1
        target_array.append(target_row)
        row+=1

    app.logger.info(f'writing to {output} ...')

    output_file = open(output, 'w', newline='')
    ouput_file_writer = csv.writer(output_file, delimiter=delimiter, quotechar=quotechar)
    ouput_file_writer.writerows(target_array)

    app.logger.info('job finished')